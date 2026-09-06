#ifndef _IN_PD480_FRAMEBUFFER_H
#define _IN_PD480_FRAMEBUFFER_H

#include "video480i.h"

/* All aliases refer to the same RDRAM. The copyright screen uses a separate,
 * immutable CPU-filled texture and submits only synchronization commands. */
static int pd480CanRender(unsigned int framebuffer, unsigned int current,
		unsigned int next, unsigned int scheduled, unsigned int queued)
{
	unsigned int physical = framebuffer & 0x1fffffffu;

	if (physical != (PD480_FB0 & 0x1fffffffu)
			&& physical != (PD480_FB1 & 0x1fffffffu)) {
		return 1;
	}

	return physical != (current & 0x1fffffffu)
		&& physical != (next & 0x1fffffffu)
		&& physical != (scheduled & 0x1fffffffu)
		&& physical != (queued & 0x1fffffffu);
}

#endif
