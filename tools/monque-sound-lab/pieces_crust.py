"""『甲殻類にも都合があります。』 deep-sea orchestral BGM: 3 title themes + 3 deep-sea field themes.

Written for long listening: long loops (2-3 min), slow harmonic rhythm, space between phrases,
colour changes per section, no busy percussion, and sparse high 'bioluminescence' notes placed
differently in every bar (deterministic, seeded) so repeats do not feel mechanical.
Motif: the DESCENT figure 5-3-1-(low 5), answered by a rising Lydian #4.
"""
import random

from orchestrate import near

GONG, BOW_CYMBAL, SWELL, CRASH = 46, 102, 48, 49


def shimmer(a, part, sections, lo, hi, per_bar=1.2, vel=44, seed=0, dur=2.0, role='spk'):
    """Sparse high chord tones at seeded off-grid positions: never the same pattern two bars running."""
    rng = random.Random(seed)
    for bar, start, span, ch in a.chords_in(sections):
        count = int(per_bar) + (1 if rng.random() < per_bar % 1 else 0)
        slots = [i * 0.5 for i in range(int(span * 2))]
        for off in sorted(rng.sample(slots, min(count, len(slots)))):
            tones = [p for p in range(lo, hi + 1) if p % 12 in ch['pcs']]
            a.add(part, start + off, dur, rng.choice(tones), vel + rng.randint(-6, 6), role=role)


def hit(a, section, key, vel, beat=0.0, dur=4.0, bar=0):
    a.add('perc', a.bar_start(a.section_bars([section])[bar]) + beat, dur, key, vel, role='perc')


# ---------------------------------------------------------------- T1 深度五万メートルへ
def arr_t_dive(a, s):
    a.melody(['hn'], ['I', 'E'], vel=78)
    a.arpeggio('harp', ['I', 'E'], step=1, lo=50, hi=81, vel=50, shape='up')
    a.pad([('vla', 54, 66), ('vc', 43, 55)], ['I', 'E'], voices=2, vel=50)
    a.bass(['cb'], ['I', 'E', 'A', 'D'], 'pedal', center=38, vel=58)
    shimmer(a, 'glock', ['I', 'A', 'D', 'E'], 79, 93, per_bar=0.8, vel=40, seed=11)
    a.melody(['vc'], ['A'], vel=86)
    a.arpeggio('harp', ['A', 'B', 'C', 'D'], step=0.5, lo=50, hi=84, vel=54)
    a.pad([('vln2', 62, 76), ('vla', 55, 68)], ['A', 'D'], voices=3, vel=54)
    a.pad([('hn', 50, 64)], ['A'], voices=2, vel=44)
    a.melody(['vln1', 'fl'], ['B'], vel=86)
    a.counter('hn', ['B'], center=62, vel=66)
    a.pad([('vla', 55, 68), ('vc', 43, 57)], ['B'], voices=3, vel=58)
    a.bass(['cb'], ['B', 'C'], 'half', center=38, vel=72)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=43)
    a.swell_into(s['C'], vel=74)
    a.melody(['vln1', 'fl'], ['C'], vel=94)
    a.melody(['hn'], ['C'], octave=-12, vel=60)
    a.counter('tpt', ['C'], center=72, vel=66)
    a.pad([('tbn', 46, 62), ('tba', 33, 46)], ['C'], voices=3, vel=68)
    a.pad([('vln2', 64, 79), ('vla', 55, 69)], ['C'], voices=3, vel=64)
    a.timpani(['C'], beats=(0,), vel=70, center=43)
    hit(a, 'C', CRASH, 70)
    shimmer(a, 'glock', ['C'], 81, 96, per_bar=1.5, vel=48, seed=12)
    a.melody(['cl'], ['D'], vel=80)
    a.counter('fl', ['D'], center=79, vel=48, beats=4)


# ---------------------------------------------------------------- T2 沈んだ都の夜明け
def arr_t_city(a, s):
    a.melody(['fl'], ['A'], vel=82)
    a.bass(['cb_pizz'], ['A', 'B', 'A2'], 'whole', center=39, vel=78)
    a.bass(['vc_pizz'], ['A', 'B'], 'whole', center=51, vel=66)
    a.ostinato(['vla_pizz', 'vln2_pizz'], ['A', 'A2'], step=1, center=64, vel=50, pattern=(None, 1, 2))
    a.arpeggio('harp', ['A', 'B', 'A2', 'C'], step=0.5, lo=51, hi=82, vel=50, shape='up')
    shimmer(a, 'glock', ['A', 'A2'], 79, 94, per_bar=0.5, vel=40, seed=21, dur=1.5)
    a.melody(['vln1'], ['B'], vel=86)
    a.melody(['ob'], ['B'], octave=-12, vel=62)
    a.pad([('vla', 55, 68), ('vc', 44, 57)], ['B'], voices=3, vel=56, rearticulate=3)
    a.counter('hn', ['B'], center=62, vel=58, beats=3)
    a.melody(['vln1'], ['A2'], vel=82)
    a.melody(['cl'], ['A2'], octave=-12, vel=66)
    a.counter('fl', ['A2'], center=79, vel=50, beats=3)
    a.swell_into(s['C'], vel=70)
    a.melody(['vln1', 'fl'], ['C'], vel=92)
    a.melody(['hn'], ['C'], octave=-12, vel=62)
    a.pad([('vln2', 63, 79), ('vla', 55, 69), ('vc', 44, 57)], ['C'], voices=4, vel=64, rearticulate=3)
    a.pad([('tbn', 46, 60)], ['C'], voices=2, vel=56, rearticulate=3)
    a.bass(['cb'], ['C'], 'whole', center=38, vel=76)
    a.timpani(['C'], beats=(0,), vel=62, center=43)
    hit(a, 'C', CRASH, 60, dur=3)


# ---------------------------------------------------------------- T3 大いなる回遊
def arr_t_whale(a, s):
    hit(a, 'A', GONG, 70)
    a.melody(['tbn'], ['A', 'D'], vel=82)
    a.melody(['tba'], ['A', 'D'], octave=-12, vel=74)
    a.pad([('vln_trem', 66, 81)], ['A', 'D'], voices=2, vel=42)
    a.pad([('vla_trem', 54, 66)], ['A', 'D'], voices=2, vel=44)
    a.bass(['cb'], ['A', 'D'], 'pedal', center=35, vel=62)
    a.arpeggio('harp', ['A', 'D'], step=1, lo=40, hi=66, vel=48, shape='up')
    shimmer(a, 'glock', ['A', 'B', 'D'], 81, 93, per_bar=1.0, vel=38, seed=31)
    for b in (0, 4):  # soft timpani rumbles under the whale call
        a.add('timp_roll', a.bar_start(a.section_bars(['A'])[b]), 3, 47, 56, role='perc')
    a.melody(['vln1'], ['B'], vel=84)
    a.counter('vla', ['B'], center=60, vel=60)
    a.pad([('vln2', 62, 76), ('vc', 43, 57)], ['B'], voices=3, vel=54)
    a.pad([('hn', 50, 64)], ['B'], voices=2, vel=50)
    a.arpeggio('harp', ['B', 'C'], step=0.5, lo=50, hi=84, vel=52)
    a.bass(['cb'], ['B', 'C'], 'whole', center=36, vel=70)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=45)
    a.swell_into(s['C'], vel=80)
    hit(a, 'C', CRASH, 72)
    a.melody(['hn'], ['C'], vel=90)
    a.melody(['vln1'], ['C'], vel=84)
    a.melody(['fl'], ['C'], octave=12, vel=70)
    a.counter('tpt', ['C'], center=70, vel=62, beats=4)
    a.pad([('tbn', 46, 62), ('tba', 33, 46)], ['C'], voices=3, vel=70)
    a.pad([('vln2', 64, 79), ('vla', 55, 69), ('vc', 43, 57)], ['C'], voices=4, vel=62)
    a.timpani(['C'], beats=(0,), vel=72, center=45)
    hit(a, 'D', BOW_CYMBAL, 60, beat=1)


# ---------------------------------------------------------------- F1 深海峡谷 3,000m
def arr_f_canyon(a, s):
    S = ['A', 'B', 'C']
    a.bass(['cb'], S, 'pedal', center=38, vel=56)
    a.pad([('vc', 43, 55)], S, voices=1, vel=50)
    a.arpeggio('harp', S, step=1, lo=45, hi=74, vel=48, shape='up')
    shimmer(a, 'glock', S, 79, 93, per_bar=0.7, vel=36, seed=41)
    shimmer(a, 'harp', S, 74, 91, per_bar=0.8, vel=40, seed=42, dur=1.5)
    a.melody(['fl'], ['A'], vel=74)
    a.pad([('vla', 53, 66)], ['A'], voices=2, vel=46)
    a.melody(['hn'], ['B'], vel=70)
    a.pad([('vln2', 60, 74), ('vla', 53, 66)], ['B'], voices=3, vel=48)
    a.counter('cl', ['B'], center=64, vel=46, beats=4)
    a.melody(['vln1_q'], ['C'], vel=76)
    a.counter('fl', ['C'], center=79, vel=44, beats=4)
    a.pad([('vln_trem', 69, 84)], ['C'], voices=2, vel=36)
    a.pad([('hn', 50, 62)], ['C'], voices=2, vel=40)
    hit(a, 'A', BOW_CYMBAL, 50, beat=1)


# ---------------------------------------------------------------- F2 沈没都市 8,000m
def arr_f_city(a, s):
    S = ['A', 'B', 'C']
    a.ostinato(['marimba'], S, step=0.5, center=72, vel=56, pattern=(0, 2, 1, 2, 0, 1, 2, 1))
    a.bass(['cb'], S, 'whole', center=38, vel=60)
    a.pad([('vla', 55, 67)], S, voices=1, vel=48)
    a.pad([('vc', 43, 55)], S, voices=1, vel=48)
    shimmer(a, 'harp', S, 72, 91, per_bar=1.0, vel=42, seed=51, dur=1.5)
    a.melody(['ob'], ['A'], vel=76)
    a.melody(['cl'], ['B'], vel=78)
    a.pad([('hn_mute', 50, 64)], ['B'], voices=2, vel=52)
    a.melody(['vln1_q'], ['C'], vel=78)
    a.counter('fl', ['C'], center=79, vel=46, beats=4)
    a.pad([('vln_trem', 69, 81)], ['C'], voices=2, vel=36)
    for sec in S:
        for b in (0, 8):
            a.add('bells', a.bar_start(a.section_bars([sec])[b]) + 0.5, 6, 67 if sec != 'B' else 62, 50, role='spk')


# ---------------------------------------------------------------- F3 人類未踏の海溝 11,000m
def arr_f_trench(a, s):
    S = ['A', 'B']
    hit(a, 'A', GONG, 64)
    hit(a, 'B', BOW_CYMBAL, 58, beat=1)
    a.bass(['cb'], S, 'pedal', center=36, vel=58)
    a.pad([('vln_trem', 67, 79)], S, voices=2, vel=36)
    a.pad([('vla_trem', 53, 65)], S, voices=2, vel=40)
    a.melody(['tbn'], S, line='moan', vel=70, role='ctr')
    a.melody(['tba'], S, line='moan', octave=-12, vel=62, role='ctr')
    a.arpeggio('harp', S, step=2, lo=40, hi=64, vel=46, shape='up')
    shimmer(a, 'glock', S, 79, 91, per_bar=0.5, vel=34, seed=61, dur=2.5)
    a.melody(['vc'], ['A'], vel=80)
    a.melody(['vln1_q'], ['B'], vel=74)
    a.counter('bn', ['B'], center=52, vel=50, beats=4)


DIVE_A = ['A4:1.5 F#4:.5 D4:1 A3:1', 'B3:1 E4:1 G#4:2', 'F#4:1.5 E4:.5 D4:1 B3:1', 'D4:2 G4:1 B4:1',
          'A4:1.5 F#4:.5 D4:1 A4:1', 'B4:1 D5:1 G4:2', 'G4:1.5 F#4:.5 E4:1 D4:1', 'C#4:2 E4:1 A4:1']
CITY_A = ['Bb4:2 Eb5:1', 'G5:2 F5:1', 'Eb5:2 C5:1', 'Bb4:3', 'C5:2 Eb5:1', 'Ab5:2 G5:1', 'F5:2 D5:1', 'F5:3',
          'Bb4:2 Eb5:1', 'G5:2 Bb5:1', 'C6:2 Bb5:1', 'Ab5:2 F5:1', 'G5:2 Eb5:1', 'Eb5:1.5 D5:.5 C5:1', 'Ab5:1 G5:1 F5:1', 'F5:2 D5:1']
CITY_A_CH = 'Eb Eb Ab Eb Cm Ab Bb Bb Eb Gm Ab Fm Eb Cm Fm7 Bb'
CANYON_A = ['A4:2 D5:2', 'F5:3 r:1', 'D5:2 B4:2', 'r:4', 'A4:1 C5:1 D5:2', 'F5:2 A5:2', 'G5:3 E5:1', 'r:4',
            'F5:2 D5:2', 'Bb4:4', 'C5:2 E5:2', 'G5:4', 'A5:2 F5:2', 'D5:4', 'B4:2 D5:2', 'r:4']
CANYON_A_CH = 'Dm Dm G/D G/D Dm Dm C C Bb Bb C C Dm Dm G G'
SUNK_A = ['C5:2 E5:2', 'A5:4', 'B4:2 D5:2', 'G5:4', 'F5:2 E5:2', 'C5:4', 'B4:2 D5:2', 'E5:4',
          'F5:2 A5:2', 'C6:4', 'B5:2 G5:2', 'D5:4', 'E5:2 C5:2', 'A4:4', 'B4:2 D5:2', 'G4:4']
SUNK_A_CH = 'Fmaj7 Fmaj7 G/F G/F Fmaj7 Fmaj7 Em7 Em7 Dm7 Dm7 G G Fmaj7 Fmaj7 G/F G/F'
TRENCH_MOAN = ['r:4', 'r:4', 'Ab2:4', 'F2:4', 'r:4', 'r:4', 'C3:4', 'Eb3:4',
               'r:4', 'r:4', 'Ab2:4', 'F2:4', 'r:4', 'r:4', 'D3:4', 'B2:4']

PIECES = {
    'crust_title_dive': dict(
        title='タイトル1「深度五万メートルへ」', key='D major (Lydian)', bpm=80, group='タイトル', usage='タイトル画面（案1）',
        motifs=['潜行の動機'],
        form='序 ホルンの呼びかけとハープ → A チェロが潜行の動機（5-3-1-5）→ B バイオリン＋フルートが高く歌う → '
             'C 総奏、トランペットの対旋律とグロッケンのきらめき → D クラリネットで静まる → 序へ戻る',
        sections=[
            ('I', 'D E/D D E/D', ['r:4', 'A4:1.5 F#4:.5 D4:2', 'r:4', 'A4:1.5 B4:.5 G#4:2']),
            ('A', 'D E/D Bm G D/F# G Em7 A', DIVE_A),
            ('B', 'G A F#m Bm Gmaj7 A Bm A', [
                'B5:2 D6:1 B5:1', 'C#6:2 A5:1 E5:1', 'A5:1.5 G#5:.5 F#5:1 C#5:1', 'D5:2 F#5:1 B5:1',
                'F#5:2 D5:1 B4:1', 'E5:1 A5:1 C#6:2', 'D6:1.5 C#6:.5 B5:1 F#5:1', 'E5:2 C#5:1 A4:1']),
            ('C', 'D E/D Bm G D/F# G Em7|A D', [
                'A5:1.5 F#5:.5 D5:1 A4:1', 'B4:1 E5:1 G#5:2', 'F#5:1.5 E5:.5 D5:1 B4:1', 'D5:2 G5:1 B5:1',
                'A5:1.5 F#5:.5 D5:1 A5:1', 'B5:1 D6:1 G5:2', 'G5:1 F#5:1 E5:1 C#5:1', 'D5:4']),
            ('D', 'Bm G D A Bm G Em7 A', [
                'F#5:2 D5:1 B4:1', 'B4:2 D5:2', 'A4:1.5 F#4:.5 D4:2', 'C#5:2 E5:2',
                'D5:2 F#5:2', 'G5:1.5 F#5:.5 D5:2', 'E5:2 D5:2', 'C#5:4']),
            ('E', 'D E/D D E/D', ['r:4', 'A4:1.5 F#4:.5 D4:2', 'r:4', 'B4:2 G#4:2']),
        ], arrange=arr_t_dive),
    'crust_title_city': dict(
        title='タイトル2「沈んだ都の夜明け」', key='E♭ major', bpm=96, meter=3, group='タイトル', usage='タイトル画面（案2）',
        motifs=[],
        form='3拍子。A フルートのワルツ、ピチカートとハープ → B 第1バイオリン、ホルンの対旋律 → '
             'A2 バイオリン＋クラリネットで再び → C 夜明けの総奏、最後に属七で頭へ',
        sections=[
            ('A', CITY_A_CH, CITY_A),
            ('B', 'Ab Bb Gm Cm Fm Bb Eb Eb Ab Bb G Cm Ab Fm7 Bb Bb7', [
                'C6:2 Ab5:1', 'D6:2 Bb5:1', 'Bb5:2 G5:1', 'G5:2 Eb5:1', 'F5:1.5 G5:.5 Ab5:1', 'Bb5:2 D5:1', 'G5:3', 'Bb4:1 Eb5:1 G5:1',
                'C6:2 Eb5:1', 'D6:2 F5:1', 'B5:2 D5:1', 'C6:2 G5:1', 'Ab5:2 C6:1', 'C6:1 Ab5:1 Eb5:1', 'D5:1 F5:1 Bb5:1', 'Ab5:2 F5:1']),
            ('A2', CITY_A_CH, CITY_A),
            ('C', 'Cm Ab Eb Bb Cm Ab Bb Bb Ab Bb Gm Cm Ab Bb Eb Bb7', [
                'G5:2 C6:1', 'C6:2 Ab5:1', 'Bb5:2 G5:1', 'F5:2 D5:1', 'Eb5:1 G5:1 C6:1', 'C6:1.5 Bb5:.5 Ab5:1', 'Bb5:3', 'F5:1 Bb5:1 D6:1',
                'C6:3', 'Bb5:2 D6:1', 'D6:1.5 C6:.5 Bb5:1', 'G5:2 Eb5:1', 'Eb5:1 Ab5:1 C6:1', 'D6:2 Bb5:1', 'G5:3', 'F5:1 D5:1 Ab5:1']),
        ], arrange=arr_t_city),
    'crust_title_whale': dict(
        title='タイトル3「大いなる回遊」', key='B minor → D major', bpm=60, group='タイトル', usage='タイトル画面（案3）',
        motifs=['鯨の呼び声'],
        form='A ドラが鳴り、トロンボーン＋テューバの低い鯨の呼び声、弦のトレモロ → B 第1バイオリンの歌とビオラ → '
             'C ニ長調でホルン＋バイオリンが雄大に、フルートが上で重なる → D 再び深い呼び声、弓で擦るシンバル',
        sections=[
            ('A', 'Bm Bm G A Bm Em G F#', [
                'F#3:2 B2:2', 'D3:3 C#3:1', 'D3:2 G3:2', 'E3:3 C#3:1', 'F#3:2 B2:2', 'E3:2 G3:2', 'B3:2 D4:2', 'C#4:3 A#3:1']),
            ('B', 'G D/F# Em Bm G A F#m A', [
                'D5:2 G5:2', 'F#5:2 A5:2', 'G5:2 E5:2', 'D5:2 B4:1 F#5:1', 'B5:3 A5:1', 'A5:2 E5:2', 'F#5:2 C#6:2', 'E5:2 C#5:1 A5:1']),
            ('C', 'D D/F# G A Bm G Em7 A', [
                'A3:2 D4:1 E4:1', 'F#4:3 E4:1', 'G4:2 B4:2', 'A4:3 E4:1', 'B4:2 F#4:2', 'G4:2 D5:2', 'E5:2 D5:2', 'C#5:4']),
            ('D', 'Bm Bm G Em Bm G F# F#', [
                'F#3:2 B2:2', 'D3:3 C#3:1', 'B2:2 D3:2', 'E3:2 G3:2', 'F#3:2 B2:2', 'G2:2 B2:2', 'A#2:2 C#3:2', 'F#2:4']),
        ], arrange=arr_t_whale),
    'crust_deep_canyon': dict(
        title='深海1「深海峡谷 3,000m」', key='D Dorian', bpm=64, group='深海', usage='深海フィールド（案1）',
        motifs=[], form='ニのドリア旋法、2小節ごとにゆっくり和音が動く。A フルート → B ホルンとクラリネット → C 静かな第1バイオリンと高いフルート。'
                        'ハープとグロッケンの高音が毎小節ちがう位置で光る',
        sections=[
            ('A', CANYON_A_CH, CANYON_A),
            ('B', 'F F C C Bb Bb Am Am Gm Gm Dm Dm Em7 Em7 A A', [
                'A4:2 C5:2', 'F4:4', 'E4:2 G4:2', 'C5:3 r:1', 'D5:2 Bb4:2', 'F4:4', 'E4:2 A4:2', 'C5:4',
                'D5:2 Bb4:2', 'G4:4', 'F4:2 A4:2', 'D5:4', 'E4:2 G4:2', 'D5:4', 'E4:2 C#5:2', 'A4:3 r:1']),
            ('C', CANYON_A_CH, CANYON_A),
        ], arrange=arr_f_canyon),
    'crust_deep_city': dict(
        title='深海2「沈没都市 8,000m」', key='F Lydian', bpm=75, group='深海', usage='深海フィールド（案2）',
        motifs=[], form='ヘのリディア旋法。マリンバが水のように揺れ、遠くでチューブラーベル。A オーボエ → B ニ短調に翳ってクラリネット、弱音器付きホルン → '
                        'C 第1バイオリンと高いフルート、弦トレモロ',
        sections=[
            ('A', SUNK_A_CH, SUNK_A),
            ('B', 'Dm Dm Bb Bb Gm Gm A A Dm Dm Bb Bb Gm Gm C C', [
                'A4:2 D5:2', 'F5:4', 'D5:2 F5:2', 'Bb4:4', 'G4:2 Bb4:2', 'D5:4', 'C#5:2 E5:2', 'A4:4',
                'F4:2 A4:2', 'D5:4', 'F5:2 D5:2', 'Bb4:4', 'Bb4:2 D5:2', 'G5:4', 'E5:2 G5:2', 'C5:4']),
            ('C', SUNK_A_CH, SUNK_A),
        ], arrange=arr_f_city),
    'crust_deep_trench': dict(
        title='深海3「人類未踏の海溝 11,000m」', key='C minor', bpm=50, group='深海', usage='深海フィールド（案3）',
        motifs=['鯨の呼び声'], form='最も深く暗い曲。A チェロの旋律、トロンボーンとテューバが遠い鯨の声、弦トレモロとC音の持続 → '
                                  'B 上から差す光のような静かな高弦、ファゴット。ドラと弓で擦るシンバル',
        sections=[
            ('A', 'Cm Cm Db Db Cm Cm Ab Ab Fm Fm Db Db Cm Cm G G', [
                'G3:4', 'C4:2 Eb4:2', 'F4:4', 'Ab3:4', 'G3:2 C4:2', 'Eb4:4', 'C4:2 Eb4:2', 'Ab4:4',
                'Ab4:2 C5:2', 'F4:4', 'Db4:2 F4:2', 'Ab4:4', 'G4:2 Eb4:2', 'C4:4', 'B3:2 D4:2', 'G3:4'],
             {'moan': TRENCH_MOAN}),
            ('B', 'Ab Ab Fm Fm Db Db G G Cm Cm Ab Ab Db Db G G', [
                'C6:4', 'Ab5:4', 'F5:2 Ab5:2', 'C6:4', 'Db6:4', 'F5:4', 'D6:2 B5:2', 'G5:4',
                'C6:2 G5:2', 'Eb5:4', 'Ab5:2 C6:2', 'Eb5:4', 'F5:2 Ab5:2', 'Db6:4', 'B5:2 D6:2', 'G5:4'],
             {'moan': ['r:4', 'r:4', 'F2:4', 'Ab2:4', 'r:4', 'r:4', 'G2:4', 'B2:4',
                       'r:4', 'r:4', 'Eb3:4', 'C3:4', 'r:4', 'r:4', 'D3:4', 'G2:4']}),
        ], arrange=arr_f_trench),
}
