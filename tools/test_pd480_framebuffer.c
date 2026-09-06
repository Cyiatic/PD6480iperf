#include <assert.h>
#include <stdio.h>
#include "pd480_framebuffer.h"

int main(void)
{
	unsigned int a = PD480_FB0;
	unsigned int b = PD480_FB1;
	unsigned int boot = PD480_FB1 - 64;
	unsigned int owner;
	unsigned int masks[] = {0, 0x20000000u, 0x80000000u};
	unsigned int i;

	assert(PD480_BUFFER_COUNT == 2);
	assert(PD480_IMAGE_BYTES == 614400);
	assert(a == 0x8036a000u && b == 0x8076a000u);
	assert(a + PD480_IMAGE_BYTES == 0x80400000u);
	assert(b + PD480_IMAGE_BYTES == 0x80800000u);

	for (i = 0; i < sizeof(masks) / sizeof(masks[0]); ++i) {
		owner = a ^ masks[i];
		assert(!pd480CanRender(a, owner, b, 0, 0));
		assert(!pd480CanRender(a, b, owner, 0, 0));
		assert(!pd480CanRender(a, b, b, owner, 0));
		assert(!pd480CanRender(a, b, b, 0, owner));
		assert(pd480CanRender(b, owner, owner, 0, 0));
	}

	/* Render B while A scans out, finish B, wait for VI to switch, render A. */
	assert(pd480CanRender(b, a, a, 0, 0));
	assert(!pd480CanRender(a, a, b, b, 0));
	assert(!pd480CanRender(b, a, b, b, 0));
	assert(pd480CanRender(a, b, b, 0, 0));
	assert(!pd480CanRender(b, b, a, a, 0));
	assert(pd480CanRender(b, a, a, 0, 0));
	assert(pd480CanRender(boot, boot, boot, boot, boot));
	puts("PASS: two-image bounds, aliases, all ownership slots, swap sequence, static boot texture");
	return 0;
}
