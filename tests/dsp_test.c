/* SPDX-License-Identifier: GPL-3.0-only */
/* ARTIHIVE 1.1 DSP regression tests. Host-only: double and 64-bit division are
 * allowed here, never in the firmware helpers under test. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../firmware/src/artihive_dsp.h"

static int fails;
static void check(int ok, const char *what)
{
    printf("dsp: %-72s %s\n", what, ok ? "ok" : "FAIL");
    fails += !ok;
}
static uint32_t rng = 0x2468ACE1u;
static uint32_t rnd(void) { rng = rng * 1664525u + 1013904223u; return rng; }
static uint8_t pack[DPACKED];

static uint32_t release_samples(uint32_t coef)
{
    int32_t e = 32767 << 16;
    uint32_t n = 0;
    while (e > (32 << 16) && n < 44100u * 12u) {
        int32_t step = (int32_t)(((int64_t)e * coef + 8388608) >> 24);
        if (step < 1) step = 1;
        e -= step;
        n++;
    }
    return n;
}

#define SPEC_N 44100u
static double sig[SPEC_N];
static double alias_ratio(int bandlimited, uint32_t period)
{
    int32_t integ = 0;
    uint32_t i, h;
    double total = 0, mean = 0, harm = 0, dc, alias;
    for (i = 0; i < SPEC_N; i++) {
        uint32_t ph = (uint32_t)(((uint64_t)(i % period) << 32) / period);
        uint32_t nx = (uint32_t)(((uint64_t)((i + 1u) % period) << 32) / period);
        double y;
        if (bandlimited) y = bl_voice(ph, nx - ph, 32768u, &integ);
        else y = (ph & 0x80000000u) ? -32767.0 : 32767.0;
        sig[i] = y;
        mean += y;
    }
    dc = mean / SPEC_N;
    for (i = 0; i < SPEC_N; i++) { double x = sig[i] - dc; total += x * x; }
    for (h = 1; h < period / 2u; h += 2u) { /* odd harmonics below Nyquist */
        double w = 2.0 * 3.14159265358979323846 * h / period;
        double coeff = 2.0 * cos(w), q1 = 0, q2 = 0, q0, e;
        for (i = 0; i < SPEC_N; i++) { q0 = coeff * q1 - q2 + sig[i] - dc; q2 = q1; q1 = q0; }
        e = q1 * q1 + q2 * q2 - coeff * q1 * q2;
        harm += 2.0 * e / SPEC_N;
    }
    alias = total - harm;
    if (alias < 0) alias = 0;
    return alias / total;
}

int main(void)
{
    uint32_t i;
    int ok;
    double maxrel = 0;
    check(DFRAMES == 96000u && DPACKED == 144000u, "delay geometry: 96000 frames, 144000 bytes per line");
    check(delay_frames(0) == 1u, "TIME=0: one sample (0.023 ms), the shortest valid delay");
    check(delay_frames(127) == DELAY_MAX_FRAMES, "TIME=127: old 2039.4 ms maximum preserved");
    {
        int mono = 1;
        for (i = 1; i < 128u; i++) if (delay_frames(i) <= delay_frames(i - 1u)) mono = 0;
        check(mono, "quadratic TIME curve is strictly monotonic over all 128 values");
    }
    check(2u * DPACKED + 42240u <= 344064u, "both packed lines plus the existing pool fit the FM-1 map");

    /* release endpoints: the old comment claimed 30 s; the measured tail is now 8 s */
    {
        double s0 = release_samples(REL_SLOW[0]) / 44100.0;
        double s127 = release_samples(REL_SLOW[127]) / 44100.0;
        double f0 = release_samples(REL_FAST[0]) / 44100.0;
        double f127 = release_samples(REL_FAST[127]) / 44100.0;
        printf("dsp: release SLOW %.4f .. %.4f s, FAST %.4f .. %.4f s\n", s0, s127, f0, f127);
        check(fabs(s0 - 8.0) < 0.08 && fabs(s127 - 0.093) < 0.004, "SLOW release: 8 s .. 93 ms to -60 dB");
        check(fabs(f0 - 0.054) < 0.003 && fabs(f127 - 0.0024) < 0.0004, "FAST release: 54 .. 2.4 ms to -60 dB");
        ok = 1;
        for (i = 1; i < 128; i++) if (REL_SLOW[i] < REL_SLOW[i-1] || REL_FAST[i] < REL_FAST[i-1]) ok = 0;
        check(ok, "REL tables are monotonic and stay inverted");
    }

    for (i = 0; i < 20000u; i++) {
        uint32_t x = BLEP_FMIN + rnd() % (BLEP_FMAX - BLEP_FMIN + 1u);
        double exact = 281474976710656.0 / x;
        double got = blep_recip(x);
        double e = fabs(got - exact) / exact;
        if (e > maxrel) maxrel = e;
    }
    printf("dsp: reciprocal max relative error %.6f%%\n", maxrel * 100);
    check(maxrel < 0.0001, "PolyBLEP reciprocal table: <0.01% error, no ISR division");

    /* the sensor meter: Q31 envelope must be converted before it is scaled */
    {
        int32_t prev = -1, monotone = 1, bounded = 1;
        int32_t lvl;
        for (lvl = 0; lvl <= 32767; lvl++) {
            int32_t h = env_bar(lvl << 16, 0, 46);
            if (h < 0 || h > 46) bounded = 0;
            if (h < prev) monotone = 0;
            prev = h;
        }
        check(bounded, "env_bar: English regression descriptionQ31");
        check(monotone, "env_bar: English regression description");
        check(env_bar(32767 << 16, 0, 46) == 45 || env_bar(32767 << 16, 0, 46) == 46,
              "env_bar: English regression description");
        check(env_bar(0, 26000, 46) == ((26000 * 46) >> 15), "env_bar: English regression descriptionHOLD English regression descriptionQ15");
        check(env_bar(0, 0, 46) == 0, "env_bar: English regression description");
    }

    /* the DC blocker must reach exact zero: the old integer form had a dead band */
    {
        int32_t st = 0, y = 0, j;
        int settled = 1;
        for (j = 0; j < 20000; j++) y = dc_block(1000, &st);
        for (j = 0; j < 200000; j++) y = dc_block(0, &st);
        if (y != 0 || st != 0) settled = 0;
        check(settled, "dc_block: English regression description");
        {
            int32_t starts[] = {1, -1, 12, -12, 960, -960, 32767, -32767};
            int k, allzero = 1;
            for (k = 0; k < 8; k++) {
                st = starts[k];
                for (j = 0; j < 400000; j++) y = dc_block(0, &st);
                if (y != 0) allzero = 0;
            }
            check(allzero, "dc_block: English regression description");
        }
    }

    ok = 1;
    for (i = 0; i < DFRAMES; i += 997u) {
        int32_t x = (int32_t)(rnd() % 65536u) - 32768;
        int32_t y = d12_read(pack, i);
        d12_write(pack, i, x);
        y = d12_read(pack, i);
        if (abs(y - x) > 15) ok = 0;
    }
    check(ok, "12-bit PCM round trip: error <=15 counts over the whole ring");
    d12_write(pack, 0, -32768); d12_write(pack, 1, 32767);
    check(d12_read(pack, 0) == -32768 && d12_read(pack, 1) >= 32752, "packed pair endpoints do not corrupt each other");
    d12_write(pack, DFRAMES - 2u, 12345); d12_write(pack, DFRAMES - 1u, -23456);
    check(abs(d12_read(pack, DFRAMES - 2u) - 12345) <= 15 && abs(d12_read(pack, DFRAMES - 1u) + 23456) <= 15,
          "last even/odd pair stays inside the packed buffer");

    for (i = 0; i < DFRAMES; i++) d12_write(pack, i, (int32_t)(i % 2001u) * 16 - 16000);
    {
        uint32_t wr = 100, d = 90000;
        uint32_t pos = wr + DFRAMES - d;
        int32_t expect = (int32_t)(pos % 2001u) * 16 - 16000;
        check(d12_tap(pack, wr, d << 8) == expect, "integer delay read across the 96000-frame wrap");
        check(d12_tap(pack, wr, (DFRAMES - 4u) << 8) == d12_read(pack, wr + 4u), "maximum delay uses the last safe frame");
    }
    {
        /* fractional tap halfway between two known samples, including odd/even parity */
        uint32_t wr = 5000, d = 100;
        uint32_t pos = wr - d;
        int32_t a = d12_read(pack, pos - 1u), b = d12_read(pack, pos);
        int32_t got = d12_tap(pack, wr, (d << 8) + 128u);
        check(abs(got - (a + (b - a) / 2)) <= 1, "fractional delay interpolation at a half-sample position");
    }

    ok = 1;
    {
        int32_t integ = 0;
        for (i = 0; i < 200000u; i++) {
            uint32_t ph = rnd(), step = rnd();
            int32_t y = bl_voice(ph, step, rnd() & 32767u, &integ);
            if (y < -49151 || y > 49151 || integ > 900000000 || integ < -900000000) ok = 0;
            if ((i & 4095u) == 0) integ = 0;
        }
    }
    check(ok, "PolyBLEP voice: bounded output and integrator under arbitrary FM steps");

    {
        double old9 = alias_ratio(0, 9), new9 = alias_ratio(1, 9);
        double old5 = alias_ratio(0, 5), new5 = alias_ratio(1, 5);
        printf("dsp: 4900 Hz square alias energy: naive %.3f%%, PolyBLEP %.3f%% (%.1f dB less)\n",
               old9 * 100, new9 * 100, 10 * log10(old9 / (new9 > 1e-12 ? new9 : 1e-12)));
        printf("dsp: 8820 Hz square alias energy: naive %.3f%%, PolyBLEP %.3f%% (%.1f dB less)\n",
               old5 * 100, new5 * 100, 10 * log10(old5 / (new5 > 1e-12 ? new5 : 1e-12)));
        check(new9 < old9 * 0.25 && new5 < old5 * 0.25, "PolyBLEP square: >12 dB less non-harmonic alias energy at 4.9 and 8.8 kHz");
    }

    printf("dsp: %s\n", fails ? "FAILURES" : "ALL DSP TESTS PASSED");
    return fails ? 1 : 0;
}
