/* SPDX-License-Identifier: GPL-3.0-only */
#include <stdio.h>
#include <stdint.h>
#define DINGHY_HOST 1
#define BOOT_HOLD_MS 1
#define APP_VER "test"
#define main artihive_host_main
#include "../firmware/src/artihive.c"
#undef main

static int run_order(uint8_t order, const uint8_t *want, uint32_t n, uint8_t steps)
{
    uint32_t i, period;
    patch_set_bpm(&p,120); p.arp_steps=steps; p.arp_gate=32; p.arp_order=order;
    fm1_ms=100; arp_start(); period=arp_period();
    for(i=0;i<n;i++) {
        fm1_ms=100+i*period; arp_tick();
        if(arp_mask != (1u<<want[i])) return (int)(10+order*10+i);
    }
    arp_stop(); return arp_mask ? 100 : 0;
}
int main(void)
{
    static const uint8_t up[]={0,1,2,0}, down[]={2,1,0,2}, pend[]={0,1,2,1,0};
    static const uint8_t altup[]={0,2,4,1,3}, altdn[]={3,1,4,2,0};
    static const uint8_t outin[]={0,4,1,3,2}, inout[]={2,3,1,4,0};
    uint32_t i;
    int rc;
    if((rc=run_order(0,up,4,3)) || (rc=run_order(1,down,4,3)) ||
       (rc=run_order(2,pend,5,3)) || (rc=run_order(4,altup,5,5)) ||
       (rc=run_order(5,altdn,5,5)) || (rc=run_order(6,outin,5,5)) ||
       (rc=run_order(7,inout,5,5))) return rc;
    patch_set_bpm(&p,240); if(arp_period()!=250u) return 110;
    patch_set_bpm(&p,30); if(arp_period()!=2000u) return 111;
    patch_set_bpm(&p,10); if(arp_period()!=6000u) return 113;
    patch_set_bpm(&p,400); if(arp_period()!=150u) return 114;
    ui.page=PG_ARP; patch_set_bpm(&p,120); knob(0,1); if(patch_bpm(&p)!=121u)return 115;
    knob(0,4); if(patch_bpm(&p)!=141u)return 116; knob(0,-8); if(patch_bpm(&p)!=61u)return 117;
    patch_set_bpm(&p,399); knob(0,4); if(patch_bpm(&p)!=400u)return 118;
    patch_set_bpm(&p,137); p.arp_steps=8; p.arp_order=0; fm1_ms=0; arp_start();
    for(i=0;i<137;i++){ fm1_ms=arp_next_ms; arp_tick(); }
    if(arp_next_ms!=60000u) return 112; /* exact average: 137 steps in one minute */
    p.arp_steps=5; p.arp_order=3; p.arp_gate=64; fm1_ms=0; arp_start();
    for(i=0;i<32;i++){ fm1_ms=arp_next_ms; arp_tick(); if(!arp_mask || arp_mask&~31u) return 120; }
    p.arp_steps=3; p.arp_order=8; arp_learn_step=0; arp_learn_mask=0; arp_learn_active=0;
    arp_learn_note(5); arp_learn_note(1); arp_learn_commit();
    if(p.arp_pattern[0] != ((1u<<5)|(1u<<1)) || arp_learn_step != 1u) return 121;
    arp_learn_note(2); arp_learn_commit(); if(p.arp_pattern[1] != (1u<<2)) return 122;
    fm1_ms=0; arp_start(); arp_tick(); if(arp_mask != ((1u<<5)|(1u<<1)) || arp_display_step != 0u) return 123;
    fm1_ms=arp_next_ms; arp_tick(); if(arp_mask != (1u<<2) || arp_display_step != 1u) return 124;
    puts("arpeggiator: eight generated modes plus USER chords, exact BPM and stop state  ok");
    return 0;
}
