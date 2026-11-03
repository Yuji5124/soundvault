"""『甲殻類にも都合があります。』 scene BGM that follows the current depth plan and the opening-to-3,000 m scenes:
base (daily comedy), 500 m (the signal answers), the rapids cave (current / rescue), a farewell,
and the 12,000 m core (unknown physics).

The old 20,000 / 35,000 / 50,000 m depths are no longer on the route, so nothing here uses them.
"""
import random

from pieces_crust import BOW_CYMBAL, CRASH, GONG, hit, shimmer

TICK, TOCK = 76, 77  # VSCO 2 CE log drums


def ping(a, sections, every=2, vel=54, seed=0):
    """Sonar ping (glockenspiel) with the answer from the harp 2.5 beats later and a little higher."""
    rng = random.Random(seed)
    for i, bar in enumerate(a.section_bars(sections)):
        if i % every:
            continue
        t = a.bar_start(bar)
        pcs = bar['chords'][0][2]['pcs']
        high = rng.choice([p for p in range(79, 92) if p % 12 in pcs])
        a.add('glock', t, 1.5, high, vel, role='spk')
        reply = [p for p in range(high + 2, 99) if p % 12 in pcs] or [high]
        a.add('harp', t + 2.5, 1.5, reply[0], vel - 8, role='spk')


def drifting_ticks(a, sections, seed, vel=56):
    """Log-drum clock whose beat wanders: the time anomaly of the core."""
    rng = random.Random(seed)
    for sec in sections:
        bars = a.section_bars([sec])
        t, end, n = a.bar_start(bars[0]), a.bar_start(bars[-1]) + a.bpb, 0
        while t < end:
            a.add('perc', t, 0.5, TICK if n % 2 == 0 else TOCK, vel + rng.randint(-5, 5), role='perc')
            t += rng.choice([0.75, 1.0, 1.0, 1.25, 1.5, 1.75])
            n += 1


# ---------------------------------------------------------------- 海底基地「作戦室はいつも騒がしい」
def arr_base(a, s):
    everywhere = ['A', 'B', 'A2', 'C', 'D', 'A3']
    a.bass(['cb_pizz'], ['A', 'A2', 'C', 'D', 'A3'], 'root5', center=40, vel=76)
    a.bass(['vc_pizz'], ['A', 'A2', 'C', 'A3'], 'root5', center=50, vel=64)
    a.drums(['A', 'B', 'A2', 'C', 'A3'], 'town', vel=84, crash_first=False)
    a.arpeggio('harp', ['A', 'A2', 'D', 'A3'], step=0.5, lo=50, hi=81, vel=42)
    shimmer(a, 'glock', ['A', 'A2', 'A3'], 79, 93, per_bar=0.5, vel=40, seed=81, dur=1.0)
    # A: clarinet tune over pizzicato
    a.melody(['cl'], ['A'], vel=82)
    a.ostinato(['vla_pizz', 'vln2_pizz'], ['A', 'A2', 'A3'], step=1, center=62, vel=50, pattern=(None, 1, None, 2))
    # B: the lobster goes for the food (tuba and bassoon, xylophone giggles)
    a.melody(['cl'], ['B'], vel=78)
    a.melody(['bn'], ['B'], octave=-12, vel=84)
    a.melody(['xylo'], ['B'], octave=12, vel=54, legato=0.4, role='spk')
    a.bass(['tba'], ['B'], 'root5', center=38, vel=72)
    a.bass(['cb_pizz'], ['B'], 'root5', center=40, vel=62)
    a.pad([('hn', 52, 64)], ['B'], voices=2, vel=44)
    # A2: warmer, violins and flute
    a.melody(['vln1'], ['A2'], vel=80)
    a.melody(['fl'], ['A2'], vel=66)
    a.pad([('hn', 52, 66)], ['A2'], voices=2, vel=44)
    # C: everyone talks at once (the same figure enters in clarinet, flute and bassoon)
    a.swell_into(s['C'], vel=56)
    a.melody(['cl'], ['C'], vel=86)
    a.melody(['fl'], ['C'], line='b', vel=84, role='ctr')
    a.melody(['bn'], ['C'], line='c', vel=84, role='ctr')
    a.ostinato(['vla_pizz', 'vln2_pizz'], ['C'], step=0.5, center=62, vel=52, pattern=(None, 0, None, 1, None, 2, None, 1))
    a.timpani(['C'], beats=(), roll_last_bar=True, center=45)
    hit(a, 'C', CRASH, 54, dur=3)
    # D: a quiet moment, then back to the tune
    a.melody(['ob'], ['D'], vel=76)
    a.pad([('vla', 52, 66), ('vc', 43, 57)], ['D'], voices=2, vel=50)
    a.bass(['cb'], ['D'], 'whole', center=38, vel=62)
    a.melody(['ob'], ['A3'], vel=72)
    a.melody(['vln1_q'], ['A3'], vel=62)
    a.pad([('hn', 52, 66)], ['A3'], voices=2, vel=42)
    del everywhere


# ---------------------------------------------------------------- 水深500m「信号の返事」
def arr_signal(a, s):
    a.arpeggio('harp', ['A', 'B', 'A2', 'C', 'D', 'A3'], step=0.5, lo=50, hi=84, vel=46, shape='up')
    a.bass(['cb'], ['A', 'B', 'A2', 'C', 'D', 'A3'], 'whole', center=38, vel=62)
    ping(a, ['A', 'A2', 'D', 'A3'], every=2, vel=54, seed=91)
    ping(a, ['B', 'C'], every=4, vel=48, seed=92)
    a.melody(['fl'], ['A'], vel=80)
    a.ostinato(['marimba'], ['A', 'A2', 'A3'], step=0.5, center=72, vel=52, pattern=(0, 2, 1, 2, 0, 1, 2, 1))
    a.pad([('vla', 54, 66), ('vc', 43, 55)], ['A'], voices=2, vel=44)
    a.melody(['cl'], ['B'], vel=78)
    a.melody(['svln'], ['B'], vel=68)
    a.ostinato(['vla_pizz', 'vln2_pizz'], ['B'], step=1, center=62, vel=50, pattern=(None, 1, None, 2))
    a.pad([('hn_mute', 50, 64)], ['B'], voices=2, vel=48)
    a.melody(['vln1'], ['A2'], vel=80)
    a.melody(['fl'], ['A2'], vel=64)
    a.pad([('vla', 54, 66), ('vc', 43, 55)], ['A2'], voices=2, vel=46)
    a.swell_into(s['C'], vel=60)
    a.melody(['vln1'], ['C'], vel=90)
    a.melody(['hn'], ['C'], octave=-12, vel=64)
    a.melody(['fl'], ['C'], vel=66)
    a.pad([('vln2', 62, 77), ('vla', 55, 69), ('vc', 43, 57)], ['C'], voices=4, vel=62)
    a.timpani(['C'], beats=(0,), vel=60, center=43, roll_last_bar=True)
    a.melody(['svln'], ['D'], vel=76)
    a.pad([('vla', 54, 66), ('vc', 43, 55)], ['D'], voices=2, vel=44)
    a.melody(['fl'], ['A3'], vel=76)
    a.pad([('hn', 50, 64)], ['A3'], voices=2, vel=40)


# ---------------------------------------------------------------- 水深500〜3,000m「激流洞窟」
def arr_current(a, s):
    run = ['A', 'B', 'A2', 'B2']
    a.arpeggio('harp', ['A', 'B', 'C', 'A2', 'B2'], step=0.25, lo=52, hi=84, vel=48)
    a.ostinato(['vln2_spic', 'vla_spic'], run, step=0.5, center=62, vel=62, pattern=(0, 1, 2, 1, 0, 2, 1, 2))
    a.bass(['cb'], ['A', 'B', 'C', 'D', 'A2', 'B2'], 'synco', center=38, vel=78)
    a.bass(['vc'], run, 'synco', center=50, vel=68)
    a.drums(run, 'tom', vel=82, crash_first=False)
    a.timpani(['B', 'B2', 'C'], beats=(0, 2), vel=76, center=43)
    a.melody(['vln1', 'ob'], ['A', 'A2'], vel=88)
    a.pad([('hn', 50, 64)], ['A', 'A2'], voices=2, vel=46)
    a.melody(['tpt'], ['B', 'B2'], vel=86)
    a.melody(['vln1'], ['B', 'B2'], vel=78)
    a.melody(['hn'], ['B', 'B2'], octave=-12, vel=64)
    a.stabs([('tbn_stac', 46, 60)], ['B', 'B2'], rhythm=((0, 0.5), (2.5, 0.5)), voices=2, vel=74)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=43)
    a.swell_into(s['C'], vel=76)
    a.melody(['hn'], ['C'], octave=-12, vel=84)
    a.melody(['vln1'], ['C'], vel=92)
    a.counter('tpt', ['C'], center=72, vel=70, beats=4)
    a.pad([('tbn', 46, 60), ('tba', 33, 46)], ['C'], voices=3, vel=70)
    a.pad([('vln2', 62, 77), ('vla', 55, 69)], ['C'], voices=3, vel=60)
    hit(a, 'C', CRASH, 70)
    a.melody(['ob'], ['D'], vel=76)
    a.pad([('vla', 54, 66), ('vc', 43, 55)], ['D'], voices=2, vel=46)
    a.arpeggio('harp', ['D'], step=1, lo=50, hi=79, vel=44, shape='up')
    shimmer(a, 'glock', ['D', 'A', 'A2'], 81, 93, per_bar=0.6, vel=40, seed=93, dur=1.0)


# ---------------------------------------------------------------- 別れ「小さな殻をのこして」
def arr_farewell(a, s):
    a.melody(['cl'], ['A'], vel=78)
    a.arpeggio('harp', ['A', 'B', 'C', 'D', 'A2'], step=1, lo=46, hi=80, vel=48, shape='up')
    a.pad([('vla', 52, 66), ('vc', 41, 55)], ['A'], voices=2, vel=48)
    a.bass(['cb'], ['A', 'B', 'C', 'D', 'A2'], 'whole', center=34, vel=62)
    a.melody(['vln1', 'fl'], ['B'], vel=84)
    a.pad([('vln2', 62, 76), ('vla', 54, 68), ('vc', 43, 57)], ['B'], voices=3, vel=54)
    a.pad([('hn', 50, 64)], ['B'], voices=2, vel=46)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=44)
    a.swell_into(s['C'], vel=66)
    a.melody(['vln1', 'fl'], ['C'], vel=94)
    a.melody(['hn'], ['C'], octave=-12, vel=66)
    a.pad([('vln2', 62, 77), ('vla', 55, 69), ('vc', 43, 57)], ['C'], voices=4, vel=64)
    a.pad([('tbn', 46, 60)], ['C'], voices=2, vel=50)
    a.timpani(['C'], beats=(0,), vel=40, center=44)
    hit(a, 'C', CRASH, 56, dur=3)
    for bar in a.section_bars(['C'])[::2]:
        a.add('bells', a.bar_start(bar) + 0.5, 6, 68, 52, role='spk')
    a.melody(['vc'], ['D'], vel=82)
    a.pad([('vla', 52, 66)], ['D'], voices=1, vel=44)
    for bar in a.section_bars(['D'])[::4]:
        a.add('bells', a.bar_start(bar), 6, 72, 46, role='spk')
    a.melody(['svln'], ['A2'], vel=74)
    a.melody(['cl'], ['A2'], vel=60)
    a.pad([('vla', 52, 66), ('vc', 41, 55)], ['A2'], voices=2, vel=44)
    shimmer(a, 'glock', ['A2'], 81, 93, per_bar=0.5, vel=38, seed=94, dur=1.5)


# ---------------------------------------------------------------- 水深12,000m「謎の中心域」
def arr_core(a, s):
    everything = ['A', 'B', 'A2', 'C', 'B2', 'D']
    a.pad([('org', 50, 71)], everything, voices=3, vel=54, rearticulate=4)
    a.pad([('vla_trem', 53, 67)], ['A', 'B', 'A2', 'B2', 'D'], voices=2, vel=40)
    a.bass(['cb'], everything, 'pedal', center=34, vel=58)
    a.arpeggio('harp', ['A', 'A2', 'D'], step=2, lo=48, hi=84, vel=44, shape='up')
    shimmer(a, 'glock', ['A', 'A2', 'B2', 'D'], 79, 93, per_bar=0.7, vel=36, seed=95, dur=2.0)
    shimmer(a, 'harp', ['B', 'B2', 'D'], 72, 96, per_bar=0.7, vel=38, seed=96, dur=2.0)
    hit(a, 'A', GONG, 58)
    hit(a, 'C', GONG, 70)
    hit(a, 'B', BOW_CYMBAL, 54, beat=1)
    hit(a, 'B2', BOW_CYMBAL, 56, beat=1)
    a.melody(['svln'], ['A'], vel=76)
    a.melody(['ob'], ['A'], octave=-12, vel=54)
    a.melody(['cl'], ['B'], vel=72)
    a.pad([('hn_mute', 50, 64)], ['B', 'B2'], voices=2, vel=46)
    a.melody(['fl'], ['A2'], vel=76)
    a.melody(['svln'], ['A2'], vel=66)
    drifting_ticks(a, ['A2', 'B2'], seed=97, vel=54)
    a.swell_into(s['C'], vel=78)
    a.melody(['vln1', 'fl'], ['C'], vel=92)
    a.melody(['hn'], ['C'], octave=-12, vel=66)
    a.pad([('tbn', 46, 60), ('tba', 33, 46)], ['C'], voices=3, vel=66)
    a.pad([('vln2', 62, 77), ('vla', 55, 69)], ['C'], voices=3, vel=58)
    a.timpani(['C'], beats=(0, 2), vel=44, center=43, roll_last_bar=True)
    a.melody(['cl'], ['B2'], vel=70)
    a.melody(['vln1_q'], ['B2'], vel=56)
    a.melody(['fl'], ['D'], vel=72)


A_BASE = ['C5:.5 F5:.5 A5:1 C6:.5 A5:.5 r:1', 'D5:.5 F5:.5 A5:1 A5:.5 G5:.5 F5:1', 'Bb5:1 A5:.5 G5:.5 F5:1 D5:1', 'E5:.5 G5:.5 C6:1 r:1 G5:1',
          'C5:.5 F5:.5 A5:1 C6:.5 A5:.5 r:1', 'E5:.5 A5:.5 C6:1 A5:.5 B5:.5 E5:1', 'D5:1 F5:1 Bb5:1 A5:1', 'G5:1.5 E5:.5 C5:2']
A_BASE_CH = 'F Dm Bb C F Am Bb C7'

A_SIGNAL = ['D5:1 G5:1 B5:2', 'A5:1.5 G5:.5 E5:2', 'F#5:1 D5:1 B4:2', 'A4:1 D5:1 F#5:2',
            'G5:1 B5:1 D6:2', 'C#6:1.5 B5:.5 A5:2', 'G5:1 E5:1 B4:2', 'A4:1 D5:1 A5:2']
A_SIGNAL_CH = 'G A Bm D Em7 A Em7 D'

A_FAREWELL = ['Eb5:1.5 C5:.5 Ab4:2', 'G4:1 Bb4:1 Eb5:2', 'F4:1 Ab4:1 C5:2', 'Db5:3 Ab4:1',
              'C5:1.5 Eb5:.5 Ab5:2', 'F5:1 Db5:1 Ab4:2', 'Bb4:1 Db5:1 F5:2', 'G4:2 Bb4:2']
A_FAREWELL_CH = 'Ab Eb/G Fm Db Ab/C Db Bbm7 Eb'

A_CORE = ['G5:3 r:1', 'B5:2 E5:2', 'Bb5:3 r:1', 'G5:2 D5:2', 'C6:3 r:1', 'Eb5:2 G5:2', 'B5:3 r:1', 'G#5:2 D#5:2']
A_CORE_CH = 'Cmaj7 Cmaj7 Ebmaj7 Ebmaj7 Abmaj7 Abmaj7 Emaj7 Emaj7'
B_CORE = ['Ab4:2 F4:2', 'C5:3 r:1', 'A4:2 F4:2', 'E5:3 r:1', 'E5:2 C#5:2', 'G#4:3 r:1', 'F4:2 Ab4:2', 'C5:2 Ab4:2']
B_CORE_CH = 'Dbmaj7 Dbmaj7 Fmaj7 Fmaj7 Amaj7 Amaj7 Dbmaj7 Dbmaj7'

PIECES = {
    'crust_base_ops': dict(
        title='海底基地「作戦室はいつも騒がしい」', key='F major', bpm=100, group='基地', usage='海底基地（作戦室・日常。くだらなくシュールな会話の場面）',
        motifs=[],
        form='A クラリネットの弾む旋律、ピチカートとタンバリン → B チューバとファゴットの食いしん坊の低音、シロフォンのくすくす笑い → '
             'A2 バイオリン＋フルートでやさしく → C 5匹が一斉にしゃべり出す（クラリネット→フルート→ファゴットと同じ句が入りを変えて重なる）→ '
             'D 静かな一息、オーボエ → A3 小さく戻る',
        sections=[
            ('A', A_BASE_CH, A_BASE),
            ('B', 'Bb F/A Gm C Dm Bb C C7', [
                'Bb3:1 D4:.5 F4:.5 Bb4:1 A4:1', 'A3:1 C4:.5 F4:.5 A4:1 G4:1', 'G3:.5 Bb3:.5 D4:1 G4:1.5 F4:.5', 'E4:1 G4:1 C5:1 r:1',
                'D4:.5 F4:.5 A4:1 D5:1 C5:1', 'Bb4:1 D5:1 F5:1 D5:1', 'E5:1 C5:.5 E5:.5 G5:2', 'Bb4:1.5 G4:.5 E4:2']),
            ('A2', A_BASE_CH, A_BASE),
            ('C', 'F F Bb Bb Gm C F C', [
                'C5:.5 D5:.5 F5:1 A5:1 G5:1', 'A5:2 C6:1 F5:1', 'D5:.5 E5:.5 F5:1 Bb5:1 A5:1', 'F5:2 D5:2',
                'D5:.5 F5:.5 G5:1 Bb5:1 A5:1', 'G5:2 E5:2', 'C5:.5 D5:.5 F5:1 A5:1 G5:1', 'E5:1 D5:1 G5:2'],
             {'b': ['r:4', 'r:4', 'F5:.5 G5:.5 Bb5:1 D6:1 C6:1', 'Bb5:2 F5:2',
                    'G5:.5 A5:.5 Bb5:1 D6:1 C6:1', 'C6:2 G5:2', 'A5:.5 Bb5:.5 C6:1 F6:1 E6:1', 'E6:1 C6:1 G5:2'],
                 'c': ['r:4', 'r:4', 'r:4', 'r:4',
                       'G3:.5 A3:.5 Bb3:1 D4:1 C4:1', 'C4:2 E4:2', 'F3:.5 G3:.5 A3:1 C4:1 Bb3:1', 'G3:1 E3:1 C3:2']}),
            ('D', 'Dm Bb F/A C Dm Gm C C7', [
                'A4:2 D5:1 F5:1', 'F5:3 D5:1', 'C5:2 A4:1 C5:1', 'E5:3 r:1', 'D5:2 F5:1 A5:1', 'G5:1.5 F5:.5 D5:2', 'E5:2 G5:2', 'Bb4:3 r:1']),
            ('A3', A_BASE_CH, A_BASE),
        ], arrange=arr_base),
    'crust_area_signal': dict(
        title='水深500m「信号の返事」', key='G major (Lydian)', bpm=96, group='深海', usage='水深500m 訓練海域（サンゴと沈没船・遺物の信号）',
        motifs=['ソナーの「ピン」と答え'],
        form='A フルートの好奇心の旋律、マリンバとハープ、ソナーのピンにハープが少し遅れて答える → B クラリネットと第1バイオリン → '
             'A2 バイオリン＋フルート → C 弦が高く歌う（信号に気づく）→ D 独奏バイオリン → A3 フルートで静かに戻る',
        sections=[
            ('A', A_SIGNAL_CH, A_SIGNAL),
            ('B', 'Bm G D A Bm Em7 A D', [
                'F#5:2 D5:1 B4:1', 'B4:1 D5:1 G5:2', 'F#5:1.5 A5:.5 D6:2', 'C#6:2 A5:1 E5:1',
                'D6:1 B5:1 F#5:2', 'E5:1 G5:1 B5:1 D6:1', 'E6:2 C#6:1 A5:1', 'F#5:2 A5:2']),
            ('A2', A_SIGNAL_CH, A_SIGNAL),
            ('C', 'Em7 A D Bm G D/F# A A7', [
                'B5:2 G5:2', 'C#6:1.5 B5:.5 A5:2', 'D6:2 A5:1 F#5:1', 'D6:1 B5:1 F#5:2',
                'B5:1.5 D6:.5 B5:2', 'A5:1 F#5:1 D5:2', 'C#6:2 A5:2', 'G5:1 E5:1 C#5:2']),
            ('D', 'G D/F# Em7 A G A D D', [
                'B5:2 D6:2', 'A5:2 F#5:2', 'G5:2 B5:2', 'A5:3 r:1', 'B5:1 A5:1 G5:2', 'E5:2 A5:2', 'F#5:2 D5:2', 'D5:3 r:1']),
            ('A3', A_SIGNAL_CH, A_SIGNAL),
        ], arrange=arr_signal),
    'crust_area_current': dict(
        title='水深500〜3,000m「激流洞窟」', key='G minor', bpm=128, group='深海', usage='水深500〜3,000m 激流洞窟（海流・迷路・救助）',
        motifs=[],
        form='A 流れるハープと弦の上で第1バイオリン＋オーボエ → B 海流が強まりトランペットとホルン → C 救助、ホルンが立ち上がる → '
             'D 流れの淀み、オーボエとグロッケン → A2・B2 流れへ戻る',
        sections=[
            ('A', 'Gm Gm Eb Eb Bb F Cm D', [
                'D5:1 G5:1 Bb5:2', 'G5:1 F5:1 D5:2', 'Eb5:1 G5:1 Bb5:2', 'Bb5:1 C6:1 G5:2',
                'D6:1.5 C6:.5 Bb5:2', 'A5:1 C6:1 A5:2', 'G5:1 Eb5:1 C5:2', 'A5:1 F#5:1 D5:2']),
            ('B', 'Cm Gm/Bb Ab Eb Cm D7 Gm Gm', [
                'G5:2 Eb5:1 C5:1', 'D5:1 G5:1 Bb5:2', 'Eb5:1 Ab5:1 C6:2', 'Bb5:2 G5:1 Eb5:1',
                'C6:1.5 Bb5:.5 G5:2', 'F#5:1 A5:1 C6:2', 'Bb5:2 G5:2', 'D5:2 G5:2']),
            ('C', 'Eb Bb Cm Gm Ab Eb/G F F', [
                'G5:2 Bb5:2', 'F5:2 D6:2', 'C6:1 Bb5:1 G5:2', 'D6:2 Bb5:1 G5:1',
                'Ab5:1 C6:1 Ab5:2', 'Bb5:1 G5:1 Eb5:2', 'A5:1 C6:1 A5:2', 'C6:3 r:1']),
            ('D', 'Gm Cm Eb Bb Gm Cm D D', [
                'Bb5:2 G5:2', 'Eb5:2 G5:2', 'G5:3 Bb5:1', 'D6:2 F5:2', 'D5:1 G5:1 Bb5:2', 'C6:2 G5:2', 'A5:2 F#5:2', 'D5:3 r:1']),
            ('A2', 'Gm Gm Eb Eb Bb F Cm D', [
                'D5:1 G5:1 Bb5:2', 'G5:1 F5:1 D5:2', 'Eb5:1 G5:1 Bb5:2', 'Bb5:1 C6:1 G5:2',
                'D6:1.5 C6:.5 Bb5:2', 'A5:1 C6:1 A5:2', 'G5:1 Eb5:1 C5:2', 'A5:1 F#5:1 D5:2']),
            ('B2', 'Cm Gm/Bb Ab Eb Cm D7 Gm Gm', [
                'G5:2 Eb5:1 C5:1', 'D5:1 G5:1 Bb5:2', 'Eb5:1 Ab5:1 C6:2', 'Bb5:2 G5:1 Eb5:1',
                'C6:1.5 Bb5:.5 G5:2', 'F#5:1 A5:1 C6:2', 'Bb5:2 G5:2', 'D5:2 G5:2']),
        ], arrange=arr_current),
    'crust_farewell': dict(
        title='別れ「小さな殻をのこして」', key='A♭ major', bpm=64, group='場面', usage='ヤドカリが約3,500mで離脱する場面（死なず、基地に残る）',
        motifs=['潜行の動機（5-3-1）'],
        form='A クラリネットの静かな旋律、ハープとビオラ → B 第1バイオリン＋フルートが温かく → C ホルンとバイオリンが「また潜ろう」と立ち上がる、鐘 → '
             'D 独奏チェロと遠い鐘 → A2 独奏バイオリンで、ほほえむように',
        sections=[
            ('A', A_FAREWELL_CH, A_FAREWELL),
            ('B', 'Db Eb Cm Fm Bbm Eb Ab Eb', [
                'F5:2 Ab5:2', 'Bb5:2 G5:2', 'Eb5:1 G5:1 C6:2', 'Ab5:2 F5:2', 'Db6:2 Bb5:2', 'Bb5:1 G5:1 Eb5:2', 'C6:1.5 Ab5:.5 Eb5:2', 'G5:1 Bb5:1 G5:2']),
            ('C', 'Ab Eb/G Fm Db Ab/C Bbm Eb Eb7', [
                'C6:2 Ab5:2', 'Bb5:1 G5:1 Eb5:2', 'Ab5:2 C6:2', 'Db6:2 Ab5:2', 'Eb5:1 Ab5:1 C6:2', 'Db6:1 Bb5:1 F5:2', 'G5:2 Bb5:2', 'Db6:2 Bb5:1 G5:1']),
            ('D', 'Ab Fm Db Eb Ab Fm Bbm Eb', [
                'Eb4:2 Ab4:2', 'C5:2 Ab4:2', 'F4:2 Db5:2', 'Bb4:3 r:1', 'C5:2 Eb5:2', 'F5:2 C5:2', 'Db5:2 Bb4:2', 'G4:3 r:1']),
            ('A2', A_FAREWELL_CH, A_FAREWELL),
        ], arrange=arr_farewell),
    'crust_area_core': dict(
        title='水深12,000m「謎の中心域」', key='C (major thirds)', bpm=64, group='深海', usage='水深12,000m 海溝最深域・謎の中心域（未知の物理現象・最終海域）',
        motifs=['時を刻む音（乱れる）'],
        form='長3度ずつ回る和音（C→E♭→A♭→E）で重力のない感じを出し、2小節ごとにゆっくり動く。A 独奏バイオリン、ドラとオルガン → '
             'B クラリネットと弱音器付きホルン、弓で擦るシンバル → A2 フルート、時を刻む音が少しずつ乱れる → C 総奏の雄大な盛り上がり → '
             'B2 乱れた時計 → D フルートがハ長調へ静かに着地',
        sections=[
            ('A', A_CORE_CH, A_CORE),
            ('B', B_CORE_CH, B_CORE),
            ('A2', A_CORE_CH, A_CORE),
            ('C', 'Cmaj7 Ebmaj7 Abmaj7 Emaj7 Cmaj7 Ebmaj7 Abmaj7 Emaj7', [
                'G5:2 B5:2', 'Bb5:2 D6:2', 'G5:2 C6:2', 'B5:2 G#5:2', 'E5:2 G5:2', 'G5:2 Bb5:2', 'C6:2 Ab5:2', 'G#5:2 B5:2']),
            ('B2', B_CORE_CH, B_CORE),
            ('D', 'Cmaj7 Fmaj7 Cmaj7 Fmaj7 Am7 Dm7 G Cmaj7', [
                'G5:2 E5:2', 'A5:2 C6:2', 'B5:3 r:1', 'A5:2 F5:2', 'E5:2 G5:2', 'F5:2 A5:2', 'B5:3 r:1', 'G5:4']),
        ], arrange=arr_core),
}
