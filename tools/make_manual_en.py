#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Build the English ARTIHIVE 1.9.0 PDF manual.
Usage: python3 tools/make_manual_en.py [screens-dir] [output.pdf]
"""
from pathlib import Path
import sys
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, Image, KeepTogether, Flowable)

SHOTS=Path(sys.argv[1] if len(sys.argv)>1 else '/home/user/artihive-theme')
OUT=Path(sys.argv[2] if len(sys.argv)>2 else '/home/user/artihive-delivery/artihive-manual-en.pdf')
FD=Path('/usr/share/fonts/truetype/dejavu')
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(FD/f)))
BLUE=colors.HexColor('#822A46'); DEEP=colors.HexColor('#5E1937'); INK=colors.HexColor('#16181C')
PALE=colors.HexColor('#FCE8EE'); RULE=colors.HexColor('#E8B8C7'); GRAY=colors.HexColor('#5A636E')
PW,PH=A4; LM=RM=20*mm; TM=19*mm; BM=18*mm; CW=PW-LM-RM
B=ParagraphStyle('body',fontName='DV',fontSize=9.2,leading=14,textColor=INK,spaceAfter=6)
LEAD=ParagraphStyle('lead',parent=B,fontSize=10.4,leading=16,textColor=DEEP,spaceAfter=10)
H1S=ParagraphStyle('h1',fontName='DVB',fontSize=19,leading=24,textColor=DEEP,spaceAfter=10)
H2S=ParagraphStyle('h2',fontName='DVB',fontSize=12,leading=16,textColor=DEEP,spaceBefore=9,spaceAfter=5)
CAP=ParagraphStyle('cap',fontName='DV',fontSize=7.7,leading=10.5,textColor=GRAY,spaceAfter=6)
TD=ParagraphStyle('td',fontName='DV',fontSize=7.9,leading=10.7,textColor=INK)
TH=ParagraphStyle('th',fontName='DVB',fontSize=8,leading=10.5,textColor=colors.white)
BUL=ParagraphStyle('bul',parent=B,leftIndent=11,bulletIndent=1,spaceAfter=3)
TITLE=ParagraphStyle('title',fontName='DVB',fontSize=33,leading=38,textColor=colors.HexColor('#FFF0F4'),alignment=TA_CENTER)
SUB=ParagraphStyle('sub',fontName='DV',fontSize=12,leading=18,textColor=colors.HexColor('#F7CBD7'),alignment=TA_CENTER)

def P(x,style=B): return Paragraph(x,style)
def H1(x): return Paragraph(x,H1S)
def H2(x): return Paragraph(x,H2S)
def bullet(x): return Paragraph('• '+x,BUL)
def table(head,rows,widths):
    data=[[Paragraph(x,TH) for x in head]]+[[Paragraph(str(x),TD) for x in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),DEEP),('GRID',(0,0),(-1,-1),.35,RULE),
      ('BACKGROUND',(0,1),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),
      ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
      ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return t

def shot(name,caption,w=66*mm):
    p=SHOTS/name
    if not p.exists(): return P('<i>Screenshot unavailable in this build.</i>',CAP)
    return KeepTogether([Image(str(p),width=w,height=w),P(caption,CAP)])

class FullMark(Flowable):
    def __init__(self, size=76*mm):
        super().__init__(); self.width=size; self.height=size; self.hAlign='CENTER'
    def draw(self):
        c=self.canv; r=self.width*.39; cx=self.width/2; cy=self.height/2
        import math
        pts=[(cx+r*math.cos(math.pi/2-k*math.pi/4),cy+r*math.sin(math.pi/2-k*math.pi/4)) for k in range(8)]
        c.setStrokeColor(colors.HexColor('#F1A9BD')); c.setLineWidth(1.5)
        for start in (0,1):
            p=c.beginPath(); p.moveTo(*pts[start])
            for k in (2,4,6): p.lineTo(*pts[(start+k)%8])
            p.close(); c.drawPath(p,stroke=1,fill=0)
        p=c.beginPath(); p.moveTo(*pts[0])
        for k in range(1,8): p.lineTo(*pts[k])
        p.close(); c.drawPath(p,stroke=1,fill=0)
        for x,y in pts:
            p=c.beginPath(); p.moveTo(cx,cy); p.lineTo(x,y); c.drawPath(p,stroke=1,fill=0)
        c.setFillColor(colors.HexColor('#FFF0F4'))
        for x,y in pts: c.circle(x,y,4,stroke=0,fill=1)
        c.circle(cx,cy,4,stroke=0,fill=1)

class Doc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=A4,leftMargin=LM,rightMargin=RM,topMargin=TM,bottomMargin=BM,
                         title='ARTIHIVE 2.0.0 — English Manual',author='KHAV with Arena.ai Agent Mode')
        self._bookmark_index = 0
        self.addPageTemplates(PageTemplate('body',Frame(LM,BM,CW,PH-TM-BM,id='f'),onPage=self.page))
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'h1':
            key = f'chapter-{self._bookmark_index}'
            self._bookmark_index += 1
            title = flowable.getPlainText()
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=0, closed=False)
    def page(self,c,d):
        if d.page == 1:
            c.saveState(); c.setFillColor(colors.HexColor('#822A46')); c.rect(0,0,PW,PH,stroke=0,fill=1); c.restoreState()
        if d.page>1:
            c.saveState(); c.setStrokeColor(RULE); c.line(LM,13*mm,PW-RM,13*mm)
            c.setFont('DV',7.5); c.setFillColor(GRAY)
            c.drawString(LM,8.5*mm,'ARTIHIVE 2.0.0 · FM-1_9620')
            c.drawRightString(PW-RM,8.5*mm,str(d.page)); c.restoreState()

st=[]
# Cover
st += [Spacer(1,22*mm),P('ARTIHIVE',TITLE),P('Firmware 2.0.0 for M-Vave FM-1',SUB),Spacer(1,5*mm),FullMark(76*mm),Spacer(1,5*mm)]
st += [P('<b>Eight voices. Four interacting pairs. One nonlinear feedback network.</b>',SUB),
       P('Created by <b>KHAV</b> with the assistance of <b>Arena.ai Agent Mode</b>.',SUB),
       Spacer(1,9*mm),P('English user and technical manual · November 2026',SUB),PageBreak()]

st += [H1('Contents'),table(['Chapter','Subject'],[
['1','Purpose, status and safety'],['2','Installation and first boot'],['3','Panel and performance controls'],
['4','Voice and FM architecture'],['5','Envelope and Hyper LFO'],['6','Modulation delay'],
['7','Output, CPU and Signal Web'],['8','Presets and storage'],['9','MIDI implementation'],
['10','Colourways'],['11','Troubleshooting and recovery'],['12','Technical notes'],
['13','Licensing, authorship and acknowledgements'],['Appendix','Complete parameter map']], [25*mm,CW-25*mm]),
P('This manual describes ARTIHIVE 2.0.0. ARTIHIVE 1.9.0 and the final ARTIHIVE 2.0.0 have successfully booted on a physical FM-1. For 2.0.0 this confirms real-device startup, not a complete long-duration functional test.',CAP),PageBreak()]

st += [H1('1. Purpose, status and safety'),P('ARTIHIVE is an experimental eight-voice drone synthesizer for the M-Vave FM-1. It was made to explore how far the device can be pushed as a sound instrument, a small real-time DSP platform and a graphic interface.' ,LEAD),
H2('What has been physically confirmed'),P('Version 1.1.4 was installed on a physical FM-1 by an independent tester. Sound, display output and encoder response were confirmed, and the tester successfully returned the unit to factory firmware. This is valuable evidence for the platform and update chain, but it was not a complete functional test. ARTIHIVE 1.9.0 and the final ARTIHIVE 2.0.0 have now successfully booted on a physical FM-1. The 2.0.0 result confirms real-device startup, but is not represented as a complete long-duration functional validation.'),
H2('Install responsibly'),bullet('Use a reliable data-capable USB cable and stable power.'),bullet('Do not disconnect power or USB while flash writing is in progress.'),bullet('Keep a known-good factory firmware package available.'),bullet('Begin audio testing at low volume, especially with short TIME and high feedback.'),
P('<b>No absolute no-brick guarantee is possible.</b> Interrupted writing remains the principal avoidable risk.',CAP),PageBreak()]

st += [H1('2. Installation and first boot'),H2('WebMIDI installation'),P('Open the supplied self-contained <b>install.html</b> in a Chromium-based browser, connect the FM-1 by USB, choose the device and select <b>artihive-2.0.0.fwsc</b>. Keep the connection untouched until verification is complete.'),
H2('Boot sequence'),table(['Stage','Expected result'],[['Logo','Version at upper left, centred ARTIHIVE logo, and byKHAV in the saved colourway'],['Validation','Progress and status while all stored parameters are checked'],['READY','The interface opens after the staged boot hold'],['Before PLAY','Exact output silence; a preset is visible but not started'],['PLAY','The selected preset begins sounding']], [35*mm,CW-35*mm]),
H2('Update mode'),P('Holding <b>OCT−</b> while powering on enters the hardware update path on supported FM-1 units. Recovery behaviour can vary by hardware revision; do not experiment with recovery unless ordinary installation or rollback has failed.'),PageBreak()]

st += [H1('3. Panel and performance controls'),shot('voice.png','VOICE page: one voice is selected while pair and global parameters remain visible.'),
table(['Control','Action'],[['HOME','DRONE page'],['EDIT','FM ROUTE page'],['BACK','ENVELOPE page'],['LFO','HYPER LFO; press again for LFO SPACE'],['FX','MOD DEL page'],['SCL','Toggle delay FREEZE'],['ARP (short)','Open the ARPEGGIO page'],['ARP (>0.7 s)','Select the next of 12 colourways'],['SEQ (short)','Mutate one parameter type across all voices or pairs'],['SEQ (>0.7 s)','Mutate all four controls on the current page'],['SAVE + SEQ','Undo the last mutation'],['PLAY on ARP','Run / stop the arpeggiator'],['SAVE (short)','Select user slot'],['SAVE (>0.7 s)','Write current patch to selected user slot'],['SELECT encoder','Select voice 1–8'],['ALGORITHM encoder','Select pair 12, 34, 56 or 78'],['PRESETS encoder','Select factory 1–16 or user U1–U8'],['KNOB 1–4','Edit the four parameters on the current page']], [42*mm,CW-42*mm]),
H2('Context MUTATE and one-level UNDO'),P('MUTATE is assigned to SEQ. A short press changes one parameter type on the visible page; on DRONE, FM ROUTE and ENVELOPE it changes that type independently across all eight voices or all four pairs. Holding SEQ for more than 0.7 seconds processes all four page controls.'),P('Before mutation, one 120-byte patch copy is retained. Hold SAVE and tap SEQ to restore it. The status messages are MUTATE ALL plus the parameter name, PAGE MUTATED, and MUTATE UNDONE. Manual editing or preset loading invalidates the undo point. FREEZE, LATCH, colourway, transpose, MIDI state and preset number are protected.'),
H2('ARPEGGIO page and USER learning'),shot('arp.png','USER step 1 triggers voices 2+6: the upper cursor shows the step while the lower contacts show sounding voices.'),P('Short ARP opens this page; holding ARP for more than 0.7 seconds changes colourway. BPM is an exact integer 10–400 with fractional-period compensation, STEPS selects 1–8 steps, GATE is 1–100% of a step, and ORDER offers UP, DOWN, PEND, RND, ALT UP, ALT DN, OUT-IN, IN-OUT and USER.'),P('With USER selected and ARP stopped, hold one or more lower sensor keys and release them together. That chord is stored in the current step and the LEARN cursor advances. Voice numbers are printed under each step. During RUN the keys cannot overwrite the pattern. The upper cursor always advances by step; the lower contacts independently show the voices actually sounding.'),
H2('Keys and octagonal contacts'),P('The first eight white keys trigger envelopes for voices 1–8; they do not determine pitch. The next eight white keys toggle the same voices as latches. Each voice keeps its own TUNE value.'),
P('Each voice has one compact metal octagon with no backing pad. Its envelope appears at the centre and expands symmetrically towards all eight sides. The separate envelope bar and the former second contact are removed.'),
H2('VOICE oscilloscope and vertical layout'),P('DRONE places a real 128-sample output oscilloscope at the top. Its high-gain trace may escape the nominal amplitude field, but a protected gap prevents it from covering the four compact SHARP forms. Smaller knobs sit below; contacts remain at the bottom. Other pages use the larger field for enlarged LFO, routing, envelope, delay and Signal Web diagrams.'),
P('Graph ink adapts to the panel: black on Blush Vein and light themes, light on the remaining dark themes. Secondary lines use a separate intensity so overlapping modulation remains readable.'),PageBreak()]

st += [H1('4. Voice and FM architecture'),shot('fm.png','FM ROUTE shows pair source, structure and total-feedback state.'),
P('Eight oscillators are arranged as four permanent pairs: <b>12, 34, 56 and 78</b>. TUNE and FINE belong to individual voices. SHARP, MOD and modulation routing belong to pairs.'),
table(['Parameter','Scope','Meaning'],[['TUNE','Voice','MIDI-note pitch, independently stored'],['FINE','Voice','Fine tuning up to approximately 98 cents'],['SHARP','Pair','Triangle-to-square waveshape'],['MOD','Pair','Frequency-modulation depth'],['SOURCE','Pair','OFF, another FM pair, or Hyper LFO'],['STRUCT','Global','Two loops or one four-pair ring'],['TOT FB','Global','Return total output into the modulation network']], [27*mm,22*mm,CW-49*mm]),
P('Strong modulation and total feedback intentionally create unstable, non-linear behaviour. Treat the instrument as an exploratory feedback system rather than a precision polysynth.',LEAD),PageBreak()]

st += [H1('5. Envelope and Hyper LFO'),shot('env.png','ENVELOPE: FAST, REL and ATK follow the selected voice; HOLD follows its pair.'),
table(['Parameter','Meaning'],[['FAST','Per voice: selects the fast or slow release range'],['REL','Per voice, inverted: larger values produce a shorter decay'],['HOLD','Per pair: quadratic amplitude floor; high settings make that pair a drone'],['ATK','Per voice: attack approximately 2–743 ms']], [43*mm,CW-43*mm]),
shot('lfo.png','HYPER LFO combines two low-frequency oscillators.'),
table(['Parameter','Meaning'],[['FREQ A / B','Approximately 0.08–21.6 Hz'],['MODE','OR for a broader contour; AND for gated intersections'],['LINK','A increasingly influences the rate of B']], [43*mm,CW-43*mm]),
H2('LFO SPACE'),shot('lfospace.png','Press LFO again: pair motion is added to the existing stereo side signal.'),
table(['Parameter','Meaning'],[['WIDTH','0–127; zero is byte-identical to 1.3.3'],['SOURCE','LFO A, LFO B or combined OUT'],['DIR','Clockwise or counter-clockwise'],['MODE','ALL together, PAIR quarter-cycle offsets, or alternating ALT']], [43*mm,CW-43*mm]),P('Four full-width horizontal L/R lanes represent pairs 12, 34, 56 and 78 from top to bottom. Pair-number labels are deliberately omitted; every lane spans the safe x=8…231 field. Each joined double marker uses the actual audio pan coefficient and a small arrow shows direction. ALL aligns the lanes, PAIR applies quarter-cycle offsets and ALT mirrors adjacent pairs. No solid plate is drawn, so the procedural theme remains visible.'),PageBreak()]

st += [H1('6. Modulation delay'),shot('delay.png','MOD DEL: two cross-feedback delay lines.'),
H2('SCL delay FREEZE'),P('SCL stops writes to both delay rings while their read position keeps moving, looping the captured material without another buffer. The SCL LED and the persistent FREEZE status show the state. Loading a preset clears FREEZE.'),
P('Version 1.3.3 introduced the retained quadratic TIME law. The bottom of the knob is expanded for comb filtering and resonator effects, while the former 2039.4 ms maximum is retained.'),
table(['TIME value','Approximate delay'],[['0','1 sample = 0.0227 ms'],['32','129 ms'],['64','518 ms'],['96','1165 ms'],['127','2039 ms']], [38*mm,CW-38*mm]),
P('All sixteen factory presets were migrated to preserve their previous physical delay times, with no more than roughly 14 ms error. User slots remain structurally intact, but their saved numerical TIME values now follow the new curve.'),
H2('Feedback caution'),P('One-sample delay with high FB can become a loud high-frequency resonator. Start with FB and MIX low. Negative modulation is calculated as a signed value and safely clamped at one sample, so it can no longer wrap to the maximum end of the buffer.'),
shot('delaymod.png','DELAY / MOD chooses modulation source, depth and wave shape.'),PageBreak()]

st += [H1('7. Output, CPU and Signal Web'),shot('out.png','OUTPUT: drive, distortion mix, drift, pressure response and the Signal Web.'),
table(['Parameter','Meaning'],[['DRIVE','Gain into soft saturation, up to approximately 6.9×'],['D MIX','Blend between cleaner and distorted paths'],['DRIFT','Slow pitch instability, up to approximately ±5 cents'],['PRESS','Response level for panel-key sensor events']], [38*mm,CW-38*mm]),
H2('Signal Web'),P('Eight activity-sensitive nodes represent the voices. Fixed pair colours are amber 12, cyan 34, magenta 56 and green 78. Inner links show modulation relationships, the outer ring shows TOTAL FB, and the retained bar displays output level.'),
H2('CPU indicator'),P('CPU 0–100% appears only in OUTPUT status. It is the smoothed audio-interrupt execution time divided by the full audio-block deadline. 100% means no processing budget remains. The host emulator reports 0% because it does not expose the JieLi hardware timer.'),PageBreak()]

st += [H1('OUT COMP'),P('Press <b>GLO</b> again on OUTPUT to open OUT COMP and switch between Signal Web and the lightweight stereo-linked compressor.'),table(['Control','Range'],[['THRESH','−48…0 dB'],['RATIO','1:1…20:1'],['ATTACK','1…100 ms'],['RELEASE','20…2000 ms']],[45*mm,100*mm]),P('IN, OUT and GR show the input, compressed output and gain reduction. One linked gain preserves the stereo image. At 1:1 the audio path is bypassed exactly.'),PageBreak()]
st += [H1('8. POLY mode in ARTIHIVE 2.0'),
P('Press HOME a second time on DRONE to enter POLY; press HOME again to return to DRONE. All 27 physical keys play chromatically, including the black-key semitones. The default span is C3–D5.'),
table(['Control','Action'],[['ROOT','Chromatic root C through B'],['SHARP','One waveform-shape value for all eight voices'],['DETUNE','Voice spread; zero is equal temperament'],['MOD','One modulation-send value for all eight voices'],['OCT− / OCT+','Move POLY by octaves 1–7; DRONE retains semitone transpose']], [42*mm,CW-42*mm]),
P('Eight voices can sound together. A ninth note steals the oldest active voice. Note level and outgoing velocity are fixed at 127. POLY has no drones, latches, PLAY drones or HOLD floor.'),
H2('Global and held-voice envelopes'),P('With no held key, FAST, RELEASE and ATTACK set all eight voices together. While notes are held, the controls edit only the newest still-held voice. HOLD displays OFF and remains inactive.'),
H2('Display and textured themes'),P('The eight voice contacts label only currently held notes. Voice numbers and permanent tuning labels are omitted. BLUSH VEIN uses white text and logos with black outlines; the four light vein themes use black text and logos with white outlines.'),
H2('POLY 2.0 boundaries'),P('POLY settings are not stored in presets. Incoming MIDI retains the compatible DRONE voice-address mapping; chromatic POLY allocation applies to the physical keyboard. Outgoing POLY key events use their true note numbers with velocity 127.'),PageBreak()]

st += [H1('9. Presets and storage'),P('There are sixteen factory presets and eight user slots. Loading never starts sound automatically after boot: press PLAY deliberately.'),
table(['Operation','Result'],[['Turn PRESETS','Choose one of 24 positions'],['Program Change 0–15','Load factory preset 1–16'],['Program Change 16–23','Load user slot U1–U8'],['Short SAVE','Choose a user destination'],['Hold SAVE >0.7 s','Write the current patch']], [48*mm,CW-48*mm]),
P('Stored parameters are validated during boot. Out-of-range values are repaired before use. The saved colourway is also used by the startup screen. Transpose is a performance state and is not part of a patch.'),
H2('Factory sound preservation in 1.9.0'),P('Legacy presets preserve their sound: each old pair FAST/REL value is copied to both voices, global ATK is copied to all eight voices, and each old four-voice HOLD value is copied to its two pairs. The inverted REL meaning is unchanged.'),PageBreak()]

st += [H1('9. MIDI implementation'),table(['Message','Action'],[['Note On, velocity 1–127','Latch voice (note mod 8)+1; velocity sets level'],['Note Off / Note On velocity 0','Release that voice latch'],['Program Change 0–15','Factory presets 1–16'],['Program Change 16–23','User slots U1–U8'],['CC 1','MOD for all four pairs'],['CC 20–23','MOD for pairs 1–4'],['CC 24–27','SHARP for pairs 1–4'],['CC 28 / 29','HOLD groups 1–4 / 5–8'],['CC 30 / 31','FREQ A / FREQ B'],['CC 32 / 33','Delay FB / MIX'],['CC 34 / 35','TIME 1 / TIME 2'],['CC 36 / 37','DRIVE / D MIX'],['CC 38 / 39','DRIFT / vibrato'],['CC 64','≥64 latch all; <64 release all'],['CC 120 / 123','Release all latches']], [52*mm,CW-52*mm]),
P('Reception is OMNI. Panel sensor events transmit Note On/Off for notes 60–67 on MIDI channel 1. Other unsupported messages are ignored.'),PageBreak()]

st += [H1('10. Colourways'),P('The interface includes twelve original ARTIHIVE colourways. Every screen element follows the selected theme; sensor contacts remain consistently metallic.'),
table(['Colourway','Character'],[['Blush Vein','Dark wine-red panel with flowing pink veins; factory default'],['Deep Blue','Blue industrial panel'],['Porcelain','High-contrast light panel'],['Rose','Warm light panel'],['Toxic Green','Acid green / dark contrast'],['Ember','Dense warm industrial palette'],['Carbon','Restrained dark panel'],['Oxide','Strong continuous full-panel patina'],['Lavender','Pastel violet with independent lilac veins'],['Lime Veil','Pastel lime with bent green veins'],['Vanilla','Warm cream with milk-and-gold veins'],['Pearl Grey','Pearl grey with a dense multi-direction steel vein field']], [38*mm,CW-38*mm])]
for n in ['blush-vein','deep-blue','porcelain','rose','toxic-green','ember','carbon','oxide','lavender','lime-veil','vanilla','pearl-grey']:
    p=SHOTS/'colours'/f'{n}.png'
    if p.exists(): st += [KeepTogether([Image(str(p),43*mm,43*mm),P(n.title(),CAP)])]
st += [PageBreak()]

st += [H1('11. Troubleshooting and recovery'),table(['Symptom','First checks'],[['No sound','Press PLAY; confirm MIX/output level; trigger or latch a voice'],['Sound only while holding a key','Raise HOLD or use the second bank of white keys as latches'],['Very bright whistle at TIME=0','Lower FB, MIX and output volume; this can be expected resonator behaviour'],['Screen appears but controls do not react','Reconnect power and test encoders before attempting another flash'],['Installation interrupted','Do not repeatedly write blindly; first check whether normal USB/update mode still enumerates'],['Need factory firmware','Use the same known-good rollback procedure that has already worked on the tested FM-1']], [49*mm,CW-49*mm]),
P('Physical confirmation covers successful startup of ARTIHIVE 1.9.0 and final ARTIHIVE 2.0.0 on a physical FM-1. Earlier 1.1.4 testing also confirmed sound, display, encoders and a successful return to factory firmware. These results do not prove every FM-1 hardware revision or recovery path.',CAP),PageBreak()]

st += [H1('12. Technical notes'),table(['Item','Value'],[['Target','JieLi AC791N / FM-1_9620'],['Audio','44.1 kHz, integer real-time DSP'],['Voices','8 oscillators in 4 pairs'],['Delay storage','Two packed 12-bit lines, 96,000 frames each'],['Delay capacity','2.1769 s per line; base TIME capped at 2.0394 s'],['Application size','173,040 bytes'],['RAM .data + .bss','18,704 bytes'],['Delay pool','330,240 of 344,064 bytes'],['Package','612,230 bytes'],['Firmware license','GPL-3.0-only']], [43*mm,CW-43*mm]),
H2('Build and verification'),P('The release is built with the restored JieLi toolchain. Host DSP tests, OTA/package tests, layout audit, FM-1 compilation and SMK-37 pro/elite/mke compilations pass. The source-archive rebuild is byte-identical to the delivered .fwsc.'),
P('Automated verification reduces software risk but does not replace listening, thermal observation and long-duration testing on physical hardware.'),PageBreak()]

st += [H1('13. Licensing, authorship and acknowledgements'),P('<b>ARTIHIVE was created by KHAV with the assistance of Arena.ai Agent Mode.</b>',LEAD),
P('The firmware was made for the experiment itself: to discover the sonic, visual and computational possibilities hidden in a small inexpensive device, and to learn what kind of instrument can emerge when feedback, instability and interface design are treated as one system.'),
P('KHAV is grateful to <b>SOMA Laboratory</b> for its aesthetics, its fearless approach to sound, and its culture of instruments that invite exploration rather than prescribe results. LYRA-8 provided the architectural and philosophical inspiration; ARTIHIVE is not a SOMA Laboratory product and is not endorsed by SOMA.'),
P('KHAV is also grateful to <b>Mike Moreno</b> for making his code accessible. The ability to read open work makes independent learning and experimentation possible. Mike Moreno’s code was not copied into ARTIHIVE.'),
table(['Project / person','Contribution or acknowledgement'],[['Dinghy / zvenson','Base firmware template'],['Felucca / Leo Kuroshita / Hügelton Instruments','Platform layer and WebMIDI update transport'],['felucca-bsp','Hardware support layer, MPL-2.0'],['SLOOP / isod89','Carrier of the platform layer'],['SOMA Laboratory','Aesthetic, sound approach and LYRA-8 architectural inspiration'],['Mike Moreno','Thanks for openness and accessible code as learning material'],['Arena.ai Agent Mode','Assistance to KHAV with design, implementation, testing and documentation']], [56*mm,CW-56*mm]),
P('No SOMA code, samples or firmware are included. LYRA-8, M-Vave and FM-1 are names of their respective owners and are mentioned only to identify inspiration and compatibility.'),PageBreak()]

st += [H1('Appendix — Complete parameter map'),table(['Parameter','Page','Scope','Range / meaning'],[
['TUNE','DRONE','Voice','MIDI note 8–127'],['FINE','DRONE','Voice','0–99, fine pitch'],['SHARP','DRONE','Pair','0–127, triangle → square'],['MOD','DRONE / FM','Pair','0–127'],['SOURCE','FM ROUTE','Pair','OFF / FM / LFO'],['STRUCT','FM ROUTE','Global','2 LOOP / RING'],['TOT FB','FM ROUTE','Global','OFF / ON'],['FAST','ENVELOPE','Voice','SLOW / FAST'],['REL','ENVELOPE','Voice','0–127, inverted'],['HOLD','ENVELOPE','Pair','0–127, quadratic floor'],['ATK','ENVELOPE','Voice','≈2–743 ms'],['FREQ A/B','HYPER LFO','Global','≈0.08–21.6 Hz'],['MODE','HYPER LFO','Global','OR / AND'],['LINK','HYPER LFO','Global','0–127'],['WIDTH','LFO SPACE','Global','0–127'],['SOURCE','LFO SPACE','Global','A / B / OUT'],['DIR','LFO SPACE','Global','CW / CCW'],['MODE','LFO SPACE','Global','ALL / PAIR / ALT'],['TIME 1/2','MOD DEL','Global','0–127, 0.023–2039 ms quadratic'],['FB','MOD DEL','Global','0–127; unity near 109'],['MIX','MOD DEL','Global','0–127'],['MOD 1/2','DELAY / MOD','Global','0–127, up to ±92 ms'],['SOURCE','DELAY / MOD','Global','LFO / SELF'],['WAVE','DELAY / MOD','Global','TRI / SQR'],['BPM','ARPEGGIO','Global','10–400 exact integer BPM'],['STEPS','ARPEGGIO','Global','1–8'],['GATE','ARPEGGIO','Global','1–100%'],['ORDER','ARPEGGIO','Global','9 modes including USER'],['DRIVE','OUTPUT','Global','0–127'],['D MIX','OUTPUT','Global','0–127'],['DRIFT','OUTPUT','Global','0–127, up to ≈±5 cents'],['PRESS','OUTPUT','Global','1–127']], [28*mm,29*mm,20*mm,CW-77*mm]),
Spacer(1,10),P('End of manual · ARTIHIVE 2.0.0 · FM-1_9620 · GPL-3.0-only',CAP)]

OUT.parent.mkdir(parents=True,exist_ok=True)
Doc(OUT).multiBuild(st)
print(f'{OUT}  {OUT.stat().st_size} bytes')
