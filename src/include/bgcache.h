#ifndef PD_BGCACHE_H
#define PD_BGCACHE_H
typedef __UINTPTR_TYPE__ bgcacheaddr;

struct bgcacheroom {
	u32 loadsize; /* Original inflate/GBI workspace, not the shrunken resident size. */
	u32 lastuse;
	u32 expectedbatches;
	u32 warmed;
};

/* A private, non-moving room heap. Free-list nodes live in free bytes only;
 * no allocation can include the gap between the onboard and expansion banks.
 * Callers retain each allocation's 16-byte-rounded size. */
struct bgcacheblock {
	struct bgcacheblock *next;
	u32 size;
};

struct bgcacheheap {
	struct bgcacheblock *free;
	u8 *start[2];
	u32 size[2];
	u32 banks;
	u32 faults;
};

static void bgcacheReset(struct bgcacheheap *heap)
{
	heap->free = NULL;
	heap->banks = 0;
	heap->faults = 0;
	heap->start[0] = heap->start[1] = NULL;
	heap->size[0] = heap->size[1] = 0;
}

static bool bgcacheFree(struct bgcacheheap *heap, void *ptr, u32 size)
{
	struct bgcacheblock **link = &heap->free;
	struct bgcacheblock *prev = NULL;
	struct bgcacheblock *block;
	bgcacheaddr addr = (bgcacheaddr)ptr;
	u32 i;
	bool owned = false;

	if (!size) {
		return true;
	}
	for (i = 0; i < heap->banks; i++) {
		bgcacheaddr start = (bgcacheaddr)heap->start[i];
		if (addr >= start && addr - start <= heap->size[i]
				&& size <= heap->size[i] - (addr - start)) {
			owned = true;
		}
	}
	if (!owned || (addr & 15) || (size & 15)) {
		heap->faults++;
		return false;
	}
	while (*link && (bgcacheaddr)*link < addr) {
		prev = *link;
		link = &prev->next;
	}
	if ((prev && (bgcacheaddr)prev + prev->size > addr)
			|| (*link && addr + size > (bgcacheaddr)*link)) {
		heap->faults++;
		return false;
	}
	block = ptr;
	block->size = size;
	block->next = *link;
	*link = block;
	if (block->next && addr + size == (bgcacheaddr)block->next) {
		block->size += block->next->size;
		block->next = block->next->next;
	}
	if (prev && (bgcacheaddr)prev + prev->size == addr) {
		prev->size += block->size;
		prev->next = block->next;
	}
	return true;
}

static bool bgcacheAddBank(struct bgcacheheap *heap, void *ptr, u32 size)
{
	u32 i;
	bgcacheaddr addr = (bgcacheaddr)ptr;
	if (!ptr || !size || (addr & 15) || (size & 15) || heap->banks == 2) {
		heap->faults++;
		return false;
	}
	for (i = 0; i < heap->banks; i++) {
		if (addr < (bgcacheaddr)heap->start[i] + heap->size[i]
				&& (bgcacheaddr)heap->start[i] < addr + size) {
			heap->faults++;
			return false;
		}
	}
	heap->start[heap->banks] = ptr;
	heap->size[heap->banks++] = size;
	return bgcacheFree(heap, ptr, size);
}

static void *bgcacheAlloc(struct bgcacheheap *heap, u32 size)
{
	struct bgcacheblock **link = &heap->free;
	struct bgcacheblock *block;
	struct bgcacheblock *next;
	if (!size || (size & 15)) {
		heap->faults++;
		return NULL;
	}
	while (*link && (*link)->size < size) {
		link = &(*link)->next;
	}
	block = *link;
	if (!block) {
		return NULL;
	}
	next = block->next;
	if (block->size > size) {
		struct bgcacheblock *tail = (struct bgcacheblock *)((u8 *)block + size);
		tail->size = block->size - size;
		tail->next = next;
		*link = tail;
	} else {
		*link = next;
	}
	return block;
}

/* mainTick submits exactly one graphics task per epoch and allows at most
 * two outstanding tasks. Keep the current epoch and two predecessors pinned.
 * This is independent of pause/time dilation and of per-player portal ticks. */
static bool bgcacheCanEvict(u32 epoch, u32 lastuse)
{
	return (u32)(epoch - lastuse) >= 3;
}
#endif
