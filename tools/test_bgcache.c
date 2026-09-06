/* Compile with the host C compiler and -iquote src/include. This tests the actual
 * runtime allocator/pinning header, not a separate Python implementation. */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint32_t u32;
typedef uint8_t u8;
#include "bgcache.h"

static _Alignas(16) u8 arena[262144 + 4096];
static u32 randomstate = 11;
static u32 random32(void) { randomstate = randomstate * 1664525 + 1013904223; return randomstate; }

int main(void)
{
	struct bgcacheheap heap;
	void *ptr[256] = {0};
	u32 size[256] = {0};
	u32 i, j;
	bgcacheReset(&heap);
	memset(arena, 0xa5, sizeof(arena));
	assert(bgcacheAddBank(&heap, arena, 131072));
	assert(bgcacheAddBank(&heap, arena + 131072 + 4096, 131072));
	assert(!bgcacheAlloc(&heap, 131088)); /* Cannot span the excluded gap. */
	ptr[0] = bgcacheAlloc(&heap, 131072);
	ptr[1] = bgcacheAlloc(&heap, 131072);
	assert(ptr[0] == arena && ptr[1] == arena + 135168);
	assert(!bgcacheAlloc(&heap, 16));
	assert(bgcacheFree(&heap, ptr[1], 131072));
	assert(bgcacheFree(&heap, ptr[0], 131072));
	assert(!bgcacheFree(&heap, ptr[0], 16)); /* Double/overlapping free rejected. */
	assert(!bgcacheFree(&heap, arena + 131072, 16)); /* Not an owned bank. */
	assert(heap.faults == 2);
	heap.faults = 0;
	memset(ptr, 0, sizeof(ptr));
	for (i = 0; i < 100000; i++) {
		u32 slot = random32() >> 24;
		if (ptr[slot]) {
			for (j = 0; j < size[slot]; j++) assert(((u8 *)ptr[slot])[j] == (u8)slot);
			assert(bgcacheFree(&heap, ptr[slot], size[slot]));
			ptr[slot] = NULL;
		} else {
			size[slot] = ((random32() >> 22) + 1) * 16;
			ptr[slot] = bgcacheAlloc(&heap, size[slot]);
			if (ptr[slot]) {
				assert(((size_t)ptr[slot] & 15) == 0);
				for (j = 0; j < 256; j++) {
					if (j != slot && ptr[j]) {
						assert((u8 *)ptr[slot] + size[slot] <= (u8 *)ptr[j]
								|| (u8 *)ptr[j] + size[j] <= (u8 *)ptr[slot]);
					}
				}
				memset(ptr[slot], (u8)slot, size[slot]);
			}
		}
	}
	for (i = 0; i < 256; i++) if (ptr[i]) assert(bgcacheFree(&heap, ptr[i], size[i]));
	assert(heap.faults == 0);
	assert(bgcacheAlloc(&heap, 131072) == arena);
	assert(bgcacheAlloc(&heap, 131072) == arena + 135168);
	for (i = 131072; i < 135168; i++) assert(arena[i] == 0xa5);
	assert(!bgcacheCanEvict(0, 0));
	assert(!bgcacheCanEvict(10, 10));
	assert(!bgcacheCanEvict(10, 9));
	assert(!bgcacheCanEvict(10, 8));
	assert(bgcacheCanEvict(10, 7));
	assert(!bgcacheCanEvict(0, UINT32_MAX));
	assert(bgcacheCanEvict(0, UINT32_MAX - 2));
	puts("PASS: actual cache allocator, gap guards, overlap rejection, 100000 fragmentation operations, task epoch pinning");
	return 0;
}
