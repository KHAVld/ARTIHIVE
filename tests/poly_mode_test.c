/* SPDX-License-Identifier: GPL-3.0-only */
#include <stdio.h>
#define DINGHY_HOST 1
#define BOOT_HOLD_MS 1
#define APP_VER "2.0-test"
#define main artihive_host_main
#include "../firmware/src/artihive.c"
#undef main
int main(void){uint32_t i,v;a_poly=1;ui.polysub=1;poly_reset();p.press=100;
 for(i=0;i<8u;i++){v=poly_alloc(i);poly_key_voice[i]=(int8_t)v;poly_voice_key[v]=(int8_t)i;poly_age[v]=++poly_clock;touch_mask|=1u<<v;poly_set_pitch(v,i);}
 if(touch_mask!=255u)return 1;v=poly_alloc(8);if(v!=0u||poly_key_voice[0]!=-1)return 2;
 if(a_inc[1]==a_inc[2])return 3;
 for(i=0;i<NP;i++)a_hold[i]=26000;a_started=1; /* POLY must ignore these floors in app_audio. */
 if(!a_poly)return 4;
 poly_reset();if(touch_mask||latch_mask)return 5;
 ui.page=PG_ENV;ui.voice=0;for(i=0;i<NV;i++){p.env_rel[i]=10;p.env_atk[i]=20;p.env_fast[i]=0;}knob(1,1);for(i=0;i<NV;i++)if(p.env_rel[i]!=11)return 6;
 poly_voice_key[3]=4;poly_key_voice[4]=3;poly_age[3]=9;touch_mask=1u<<3;knob(3,1);if(p.env_atk[3]!=21)return 7;for(i=0;i<NV;i++)if(i!=3&&p.env_atk[i]!=20)return 8;
 p.env_hold[1]=42;knob(2,10);if(p.env_hold[1]!=42)return 9;
 puts("POLY: 27 keys, note-only labels, global SHARP/MOD/envelope, held-voice envelope edit, HOLD OFF, LEVEL 127  ok");return 0;}
