/* SPDX-License-Identifier: GPL-3.0-only */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#define DINGHY_HOST 1
#define BOOT_HOLD_MS 1
#define APP_VER "test"
#define main artihive_host_main
#include "../firmware/src/artihive.c"
#undef main
int main(void)
{
    uint8_t old[PATCH_V13_SIZE];
    uint8_t old15[PATCH_V15_SIZE], old16[PATCH_V16_SIZE];
    patch_t q;
    uint32_t i;
    for (i = 0; i < sizeof old; i++) old[i] = (uint8_t)(i * 37u + 11u);
    for (i = 0; i < sizeof old15; i++) old15[i] = (uint8_t)(i * 19u + 7u);
    for (i = 0; i < sizeof old16; i++) old16[i] = (uint8_t)(i * 13u + 5u);
    patch_from_v13(&q, old);
    if (sizeof(patch_t) != 120u || sizeof(settings_v13_t) != 84u || sizeof(settings_v15_t) != 92u || sizeof(settings_v16_t) != 96u || sizeof(settings_v17_t) != 104u || sizeof(settings_v181_t) != 108u || sizeof(settings_v182_t) != 108u || sizeof(settings_t) != 136u) return 1;
    if (memcmp(&q, old, sizeof old)) return 2;
    if (q.space_width || q.space_src || q.space_dir || q.space_mode) return 3;
    if (q.arp_rate != 120u || q.arp_steps != 8u || q.arp_gate != 64u || q.arp_order) return 4;
    for(i=0;i<8u;i++)if(q.arp_pattern[i]!=(1u<<i))return 7;
    patch_from_v15(&q, old15);
    if (memcmp(&q, old15, sizeof old15)) return 5;
    if (q.arp_rate != 120u || q.arp_steps != 8u || q.arp_gate != 64u || q.arp_order) return 6;
    patch_from_v16(&q, old16); if(memcmp(&q,old16,sizeof old16))return 8;
    for(i=0;i<8u;i++)if(q.arp_pattern[i]!=(1u<<i))return 9;
    puts("1.3.3/1.5 patches -> arpeggiator patch: old bytes preserved, safe defaults  ok");
    return 0;
}
