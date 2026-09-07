#include <ultra64.h>

OSThread __osThreadSave;

/* Diagnostic only: 16 event-drop counters, then last event/queue/thread/count.
 * Updated only on send_mesg's existing full-queue discard path. */
u32 g_PdEventDropTrace[20];
