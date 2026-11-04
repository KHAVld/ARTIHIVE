/* SPDX-License-Identifier: GPL-3.0-only */
#include <stdio.h>
#define DINGHY_HOST 1
#define BOOT_HOLD_MS 1
#define APP_VER "test"
#define main artihive_host_main
#include "../firmware/src/artihive.c"
#undef main
int main(void){uint32_t i;ui.page=PG_ENV;env_defaults(&p);for(i=0;i<NV;i++){p.env_fast[i]=0;p.env_rel[i]=60;p.env_atk[i]=60;}for(i=0;i<NP;i++)p.env_hold[i]=30;
 ui.voice=3;ui.pair=1;knob(0,1);knob(1,5);knob(3,7);if(!p.env_fast[3]||p.env_rel[3]!=65||p.env_atk[3]!=67)return 1;
 for(i=0;i<NV;i++)if(i!=3&&(p.env_fast[i]||p.env_rel[i]!=60||p.env_atk[i]!=60))return 2;
 knob(2,6);if(p.env_hold[1]!=36)return 3;for(i=0;i<NP;i++)if(i!=1&&p.env_hold[i]!=30)return 4;
 puts("envelope scope: FAST/REL/ATK selected voice; HOLD selected pair  ok");return 0;}
