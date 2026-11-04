/* SPDX-License-Identifier: GPL-3.0-only */
#include <stdio.h>
#include "fm1_flash_map.h"
int main(void)
{
    if (!FL_JEDEC_OK(0x856014u)) return 1; /* Puya P25Q80 */
    if (!FL_JEDEC_OK(0xB36014u)) return 2; /* UC25HQ80, newer FM-1 */
    if (FL_JEDEC_OK(0u) || FL_JEDEC_OK(0xFFFFFFu) || FL_JEDEC_OK(0xB36015u)) return 3;
    puts("FM-1 flash IDs: P25Q80 and UC25HQ80 accepted; unknown parts refused  ok");
    return 0;
}
