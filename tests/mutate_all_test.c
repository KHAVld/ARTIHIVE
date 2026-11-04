/* SPDX-License-Identifier: GPL-3.0-only */
#include <stdio.h>
#define DINGHY_HOST 1
#define BOOT_HOLD_MS 1
#define APP_VER "test"
#define main artihive_host_main
#include "../firmware/src/artihive.c"
#undef main
int main(void)
{
    uint32_t i; uint16_t before[NV]; uint8_t b8[NV];
    ui.page=PG_VOICE; for(i=0;i<NV;i++){p.tune[i]=16384;before[i]=p.tune[i];}
    mutate_control(0); for(i=0;i<NV;i++)if(p.tune[i]==before[i])return 1;
    for(i=0;i<NP;i++){p.mod[i]=64;b8[i]=p.mod[i];} mutate_control(3); for(i=0;i<NP;i++)if(p.mod[i]==b8[i])return 2;
    ui.page=PG_ENV; for(i=0;i<NV;i++){p.env_rel[i]=64;b8[i]=p.env_rel[i];} mutate_control(1); for(i=0;i<NV;i++)if(p.env_rel[i]==b8[i])return 3;
    for(i=0;i<NP;i++){p.env_hold[i]=64;b8[i]=p.env_hold[i];} mutate_control(2); for(i=0;i<NP;i++)if(p.env_hold[i]==b8[i])return 4;
    for(i=0;i<NV;i++){p.env_atk[i]=64;b8[i]=p.env_atk[i];} mutate_control(3); for(i=0;i<NV;i++)if(p.env_atk[i]==b8[i])return 5;
    puts("MUTATE: selected voice parameter type changes every voice/pair  ok"); return 0;
}
