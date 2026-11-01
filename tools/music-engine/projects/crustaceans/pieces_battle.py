"""『甲殻類にも都合があります。』 battle BGM: robot swarm, giant-creature hunt, ancient guardian.

Serious, cool SF combat that still sounds like the deep sea. Battles can run for minutes, so
percussion comes and goes by section, and every piece has a calmer colour section.
"""
from pieces_crust import CRASH, GONG, hit, shimmer

TICK, TOCK = 76, 77  # VSCO 2 CE log drums


# ---------------------------------------------------------------- 群れを蹴散らせ
def arr_swarm(a, s):
    drive = ['A', 'B', 'A2', 'D']
    a.ostinato(['vln2_spic', 'vla_spic'], drive, step=0.5, center=62, vel=76, pattern=(0, 1, 2, 1, 0, 2, 1, 2))
    a.bass(['cb_spic'], drive, 'drive8', center=36, vel=86)
    a.bass(['vc_spic'], drive, 'synco', center=48, vel=84)
    a.drums(['A', 'A2', 'D'], 'battle', vel=86)
    a.timpani(['A', 'A2', 'D'], beats=(0, 2.5), vel=86, center=45)
    a.melody(['vln1', 'fl'], ['A', 'A2', 'D'], vel=94)
    a.counter('tpt', ['A', 'A2'], center=72, vel=78)
    a.stabs([('hn_stac', 55, 70), ('tbn_stac', 45, 60)], ['A2', 'D'], rhythm=((0, 0.5), (1.5, 0.5), (3, 0.5)), vel=80)
    a.melody(['hn'], ['B'], vel=92)
    a.melody(['vc'], ['B'], vel=82)
    a.pad([('vln2', 62, 77), ('vla', 55, 69)], ['B'], voices=3, vel=64)
    a.drums(['B'], 'march', vel=74, crash_first=False)
    # mechanical swarm: staccato xylophone + flute over pizzicato and marimba, no drums
    a.melody(['xylo'], ['C'], vel=80, legato=0.45)
    a.melody(['fl'], ['C'], vel=70, legato=0.5)
    a.ostinato(['marimba'], ['C'], step=0.5, center=60, vel=60, pattern=(0, 2, 1, 2))
    a.ostinato(['vln2_pizz', 'vla_pizz'], ['C'], step=0.5, center=62, vel=56, pattern=(None, 0, None, 1))
    a.bass(['cb_pizz'], ['C'], 'root5', center=40, vel=78)
    for bar in a.section_bars(['C']):
        t = a.bar_start(bar)
        for beat in range(4):
            a.add('perc', t + beat, 0.5, TICK if beat % 2 == 0 else TOCK, 64, role='perc')
    a.timpani(['C'], beats=(), roll_last_bar=True, center=45)
    a.swell_into(s['A2'], vel=80)
    a.melody(['hn'], ['D'], octave=-12, vel=70)
    a.pad([('tbn', 45, 60), ('tba', 33, 45)], ['D'], voices=3, vel=72)
    shimmer(a, 'glock', ['A', 'A2'], 81, 93, per_bar=0.6, vel=44, seed=71, dur=1)


# ---------------------------------------------------------------- 巨大生物ハント
def arr_hunt(a, s):
    hit(a, 'A', GONG, 80)
    a.melody(['hn'], ['A'], vel=92)
    a.melody(['tbn'], ['A'], octave=-12, vel=80)
    a.pad([('vln_trem', 62, 77)], ['A', 'D'], voices=2, vel=56)
    a.bass(['cb'], ['A', 'B', 'C', 'D'], 'synco', center=38, vel=88)
    a.drums(['A', 'C'], 'tom', vel=92, crash_first=False)
    a.timpani(['A', 'C', 'D'], beats=(0, 1.5, 2.5), vel=90, center=43)
    a.melody(['vln1'], ['B'], vel=92)
    a.melody(['ob'], ['B'], vel=72)
    a.ostinato(['vla_spic', 'vc_spic'], ['B', 'C', 'D'], step=0.5, center=55, vel=74, pattern=(0, 1, 0, 2))
    a.pad([('hn', 50, 65)], ['B'], voices=3, vel=64)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=43)
    a.swell_into(s['C'], vel=86)
    a.melody(['vln1', 'fl'], ['C'], vel=96)
    a.melody(['hn'], ['C'], octave=-12, vel=70)
    a.counter('tpt', ['C'], center=72, vel=78)
    a.pad([('tbn', 45, 60), ('tba', 33, 45)], ['C'], voices=3, vel=76)
    hit(a, 'C', CRASH, 80)
    a.melody(['bn', 'vc'], ['D'], vel=90)
    a.stabs([('tbn_stac', 45, 60), ('hn_stac', 55, 67)], ['D'], rhythm=((0, 0.5), (0.75, 0.25), (2.5, 0.5)), vel=84)
    a.drums(['D'], 'boss', vel=82, crash_first=False)
    shimmer(a, 'harp', ['A', 'D'], 72, 88, per_bar=0.8, vel=46, seed=72, dur=1)


# ---------------------------------------------------------------- 古代の守護者
def arr_guardian(a, s):
    drive = ['A', 'A2', 'C']
    a.ostinato(['vln2_spic', 'vla_spic'], ['A', 'B', 'A2', 'C'], step=0.5, center=62, vel=74, pattern=(0, 1, 2, 1, 2, 1))
    a.bass(['cb_spic'], ['A', 'B', 'A2', 'C'], 'drive8', center=36, vel=72)
    a.drums(drive, 'battle3', vel=84, crash_first=False)
    a.timpani(drive, beats=(0,), vel=86, center=45)
    a.melody(['vln1'], ['A', 'A2'], vel=104)
    a.melody(['ob'], ['A', 'A2'], vel=84)
    a.pad([('org', 54, 71)], ['A', 'A2'], voices=3, vel=58, rearticulate=3)
    a.counter('tpt', ['A2'], center=72, vel=78, beats=3)
    a.melody(['hn'], ['B'], vel=92)
    a.melody(['tbn'], ['B'], octave=-12, vel=74)
    a.pad([('vln2', 62, 77), ('vla', 55, 69)], ['B'], voices=3, vel=62, rearticulate=3)
    a.drums(['B'], 'waltz', vel=96, crash_first=False)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=45)
    a.swell_into(s['C'], vel=86)
    a.melody(['vln1', 'fl'], ['C'], vel=96)
    a.melody(['hn'], ['C'], octave=-12, vel=70)
    a.pad([('tbn', 45, 60), ('tba', 33, 45)], ['C'], voices=3, vel=76, rearticulate=3)
    a.pad([('org', 54, 71)], ['C'], voices=3, vel=60, rearticulate=3)
    hit(a, 'C', CRASH, 80)
    for sec in ('A', 'B', 'A2', 'C'):
        bar = a.section_bars([sec])[0]
        a.add('bells', a.bar_start(bar), 6, 71 if sec != 'B' else 66, 64, role='spk')
    shimmer(a, 'glock', ['A', 'A2'], 81, 93, per_bar=0.5, vel=44, seed=73, dur=1)


GUARD_A = ['F#5:1 B5:1 D6:1', 'B5:2 F#5:1', 'G5:1 B5:1 D6:1', 'D6:2 B5:1', 'E5:1 G5:1 B5:1', 'G5:2 E5:1', 'F#5:1 A#5:1 C#6:1', 'A#5:2 F#5:1',
           'D5:1 F#5:1 B5:1', 'D6:2 B5:1', 'A5:1 F#5:1 D5:1', 'F#5:2 A5:1', 'B5:1 G5:1 E5:1', 'D6:2 B5:1', 'C#6:2 A#5:1', 'F#5:3']
GUARD_A_CH = 'Bm Bm G G Em Em F# F# Bm Bm D D Em G F# F#'
SWARM_A = ['E5:.5 C5:.5 A4:1 E5:1 A5:1', 'A5:.5 G5:.5 E5:1 r:1 C5:.5 D5:.5', 'F5:1 A5:1 C6:1.5 A5:.5', 'B5:1.5 G5:.5 D5:2',
           'E5:.5 C5:.5 A4:1 E5:1 A5:1', 'C6:1 B5:.5 A5:.5 E5:2', 'F#5:1 A5:1 D6:1 A5:1', 'G#5:2 B5:1 E5:1']
SWARM_A_CH = 'Am Am F G Am Am D E'

PIECES = {
    'crust_battle_swarm': dict(
        title='戦闘1「群れを蹴散らせ」', key='A Dorian', bpm=150, group='戦闘', usage='通常戦闘（敵ロボットの群れ）',
        motifs=[], form='A 疾走する弦の刻みの上でバイオリン＋フルート、トランペットの対旋律 → B ホルンとチェロの英雄的な旋律 → '
                        'C 打楽器を抜き、シロフォン＋フルートのスタッカートとマリンバで機械の群れ → A2 金管の打ち込みを加えて再び → D 総奏で頭へ',
        sections=[
            ('A', SWARM_A_CH, SWARM_A),
            ('B', 'F G Em Am F G E E7', [
                'C4:.5 F4:.5 A4:1 C5:2', 'B4:1.5 D5:.5 G4:2', 'E4:.5 G4:.5 B4:1 E5:2', 'C5:1.5 B4:.5 A4:2',
                'A4:1 C5:1 F5:2', 'D5:1.5 B4:.5 G4:2', 'G#4:1 B4:1 E5:2', 'D5:2 B4:1 G#4:1']),
            ('C', 'Fmaj7 Fmaj7 Em7 Em7 Dm7 Dm7 E E', [
                'A5:.5 r:.5 C6:.5 r:.5 E6:.5 r:.5 C6:.5 A5:.5', 'F5:.5 r:.5 A5:.5 r:.5 C6:1 E5:1',
                'G5:.5 r:.5 B5:.5 r:.5 D6:.5 r:.5 B5:.5 G5:.5', 'E5:.5 r:.5 G5:.5 r:.5 B5:1 D5:1',
                'F5:.5 r:.5 A5:.5 r:.5 C6:.5 r:.5 A5:.5 F5:.5', 'D5:.5 r:.5 F5:.5 r:.5 A5:1 C6:1',
                'G#5:.5 r:.5 B5:.5 r:.5 E6:1 B5:1', 'E5:2 G#5:1 B5:1']),
            ('A2', SWARM_A_CH, SWARM_A),
            ('D', 'Am G F E Am G F E7', [
                'A5:1 C6:1 E5:1 A5:1', 'B5:1 D6:1 G5:2', 'C6:1.5 A5:.5 F5:2', 'G#5:2 E5:1 B4:1',
                'E5:.5 A5:.5 C6:1.5 B5:.5 A5:1', 'G5:1 B5:1 D6:2', 'A5:1 F5:1 C5:2', 'B5:1 G#5:1 D5:1 E5:1']),
        ], arrange=arr_swarm),
    'crust_battle_hunt': dict(
        title='戦闘2「巨大生物ハント」', key='D minor (Phrygian ♭II)', bpm=125, group='戦闘', usage='巨大生物ハント（ボス級の生物）',
        motifs=['潜行の動機（短調）'], form='A ドラが鳴り、ホルン＋トロンボーンの重い狩りの主題、木の太鼓とティンパニ、♭IIの和音 → '
                                      'B 第1バイオリンが追い上げ、刻むビオラとチェロ → C 総奏の狩りの主題、トランペットの対旋律 → D ファゴット＋チェロのフリギアの動き、金管の打ち込み',
        sections=[
            ('A', 'Dm Eb/D Dm Eb/D Bb C Gm A', [
                'D4:1.5 A3:.5 D4:1 F4:1', 'G4:1.5 Eb4:.5 Bb3:2', 'A4:1.5 F4:.5 D4:1 A4:1', 'Bb4:3 G4:1',
                'F4:1 Bb4:1 D5:2', 'E5:1.5 C5:.5 G4:2', 'D5:1 Bb4:1 G4:2', 'C#5:2 A4:1 E4:1']),
            ('B', 'Gm A Dm Bb Gm A Bb A7', [
                'G5:1 Bb5:1 D6:2', 'C#6:1.5 A5:.5 E5:2', 'F5:1 A5:1 D6:2', 'D6:1.5 Bb5:.5 F5:2',
                'Bb5:1 G5:1 D5:2', 'E5:1 A5:1 C#6:2', 'D6:2 Bb5:1 F5:1', 'E5:1 G5:1 C#6:2']),
            ('C', 'Dm Bb Gm A Dm Bb Eb A', [
                'A4:.5 D5:.5 E5:.5 F5:1 A5:1.5', 'Bb5:1 A5:.5 F5:.5 D5:2', 'G5:.5 Bb5:.5 D6:1.5 C6:.5 Bb5:1', 'A5:2 E5:1 C#5:1',
                'A4:.5 D5:.5 E5:.5 F5:1 A5:1.5', 'D6:1 Bb5:1 F5:2', 'G5:1 Bb5:1 Eb5:2', 'E5:1 A5:1 C#6:2']),
            ('D', 'Dm Eb Dm Eb Bbm A Gm A7', [
                'D4:.5 Eb4:.5 D4:.5 A3:1.5 D4:1', 'G4:1 Bb4:1 Eb4:2', 'F4:.5 E4:.5 D4:1 A3:2', 'Eb4:1.5 G4:.5 Bb4:2',
                'Db4:1 F4:1 Bb4:2', 'C#4:1 E4:1 A4:2', 'Bb4:1.5 A4:.5 G4:2', 'G4:1 E4:1 C#4:1 A3:1']),
        ], arrange=arr_hunt),
    'crust_battle_guardian': dict(
        title='戦闘3「古代の守護者」', key='B minor', bpm=160, meter=3, group='戦闘', usage='ボス戦（古代文明の守護者）',
        motifs=[], form='3拍子で突き進む戦い。A 神殿のオルガンと鐘、バイオリン＋オーボエの旋律 → B ホルン＋トロンボーンの長い英雄的な旋律 → '
                        'A2 トランペットの対旋律を加えて再び → C 総奏のクライマックス、オルガンと低音金管',
        sections=[
            ('A', GUARD_A_CH, GUARD_A),
            ('B', 'G G A A F#m F#m Bm Bm G G A A Em Em F# F#7', [
                'D4:2 G4:1', 'B4:3', 'C#5:2 A4:1', 'E5:3', 'C#5:2 A4:1', 'F#4:3', 'D5:2 B4:1', 'F#4:3',
                'B4:2 D5:1', 'G4:3', 'A4:2 C#5:1', 'E5:3', 'G4:2 B4:1', 'E5:3', 'C#5:2 A#4:1', 'E4:1 A#4:1 C#5:1']),
            ('A2', GUARD_A_CH, GUARD_A),
            ('C', 'Bm G D A Bm G Em F# Bm G D A G Em F# F#', [
                'B5:2 F#5:1', 'G5:1 B5:1 D6:1', 'A5:2 F#5:1', 'E5:1 A5:1 C#6:1', 'D6:2 B5:1', 'B5:2 G5:1', 'G5:1 E5:1 B4:1', 'A#4:1 C#5:1 F#5:1',
                'B5:2 D6:1', 'D6:1 B5:1 G5:1', 'F#5:2 A5:1', 'C#6:2 A5:1', 'B5:1 D6:1 B5:1', 'G5:2 E5:1', 'F#5:1 A#5:1 C#6:1', 'F#5:2 C#5:1']),
        ], arrange=arr_guardian),
}
