"""Towns, villages, castle, shrine (original melodies for MONQUE SOUND LAB)."""
import pretty_midi as pm

N = pm.note_name_to_number


def sparkle(a, sections, every=2, vel=54, up=12):
    for bar in a.section_bars(sections)[::every]:
        first = bar['melody'].split()[0].split(':')[0]
        if first != 'r':
            a.add('glock', a.bar_start(bar), 1, N(first) + up, vel, role='spk')


def arr_start_town(a, s):
    a.melody(['cl'], ['A'], vel=84)
    a.ostinato(['vla_pizz', 'vln2_pizz'], ['A', 'A2'], step=0.5, center=62, vel=58, pattern=(None, 0, None, 1, None, 2, None, 1))
    a.arpeggio('harp', ['A', 'B', 'A2'], step=0.5, lo=50, hi=81, vel=56)
    a.bass(['cb_pizz'], ['A', 'A2'], 'root5', center=40, vel=82)
    a.bass(['vc_pizz'], ['A', 'A2'], 'root5', center=50, vel=74)
    a.drums(['A', 'B', 'A2'], 'town', vel=92, crash_first=False)
    a.melody(['fl', 'ob'], ['B'], vel=82)
    a.pad([('vln2', 62, 76), ('vla', 55, 69), ('vc', 45, 60)], ['B'], voices=3, vel=56)
    a.bass(['cb'], ['B'], 'half', center=38, vel=74)
    a.counter('cl', ['B'], center=64, vel=56)
    a.melody(['vln1'], ['A2'], vel=88)
    a.melody(['fl'], ['A2'], vel=70)
    a.pad([('hn', 52, 67)], ['A2'], voices=2, vel=50)
    sparkle(a, ['A2'])


def arr_bie(a, s):
    a.melody(['ob'], ['A'], vel=82)
    a.bass(['cb_pizz'], ['A', 'B'], 'whole', center=40, vel=80)
    a.bass(['vc_pizz'], ['A', 'B'], 'whole', center=50, vel=70)
    a.ostinato(['vla_pizz', 'vln2_pizz'], ['A', 'B'], step=1, center=62, vel=56, pattern=(None, 1, 2))
    a.arpeggio('harp', ['A', 'B'], step=0.5, lo=50, hi=79, vel=52, shape='up')
    a.drums(['A', 'B'], 'waltz', vel=92, crash_first=False)
    a.counter('cl', ['A'], center=62, vel=52, beats=3)
    a.melody(['fl'], ['B'], vel=82)
    a.melody(['cl'], ['B'], octave=-12, vel=70)
    a.pad([('hn', 50, 65)], ['B'], voices=2, vel=48, rearticulate=3)
    sparkle(a, ['B'], every=4)


def arr_castletown(a, s):
    a.melody(['vln1', 'fl'], ['A', 'A2'], vel=88)
    a.ostinato(['vln2_spic', 'vla_spic'], ['A', 'B', 'A2'], step=0.5, center=64, vel=66, pattern=(0, 1, 2, 1))
    a.bass(['cb_pizz'], ['A', 'B', 'A2'], 'root5', center=38, vel=84)
    a.bass(['vc_pizz'], ['A', 'A2'], 'march', center=48, vel=70)
    a.drums(['A', 'B', 'A2'], 'town', vel=96, crash_first=False)
    a.drums(['A2'], 'march', vel=60, crash_first=True)
    a.melody(['ob', 'cl'], ['B'], vel=86)
    a.pad([('hn', 52, 67)], ['B', 'A2'], voices=3, vel=56)
    a.counter('tpt', ['A2'], center=70, vel=72)
    sparkle(a, ['A', 'A2'], every=4)


def arr_castle(a, s):
    a.melody(['tpt'], ['A'], vel=92)
    a.counter('hn', ['A'], center=62, vel=82)
    a.pad([('tbn', 46, 62), ('tba', 31, 46)], ['A'], voices=3, vel=76)
    a.pad([('vln2', 62, 77), ('vla', 55, 69), ('vc', 45, 60)], ['A', 'B'], voices=4, vel=62)
    a.bass(['cb'], ['A', 'B'], 'half', center=36, vel=80)
    a.timpani(['A'], beats=(0, 2), vel=82, center=43)
    a.drums(['A'], 'title', vel=80)
    a.melody(['vln1', 'ob'], ['B'], vel=88)
    a.arpeggio('harp', ['B'], step=0.5, lo=50, hi=82, vel=58)
    a.pad([('hn', 50, 65)], ['B'], voices=2, vel=56)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=43)


def arr_hidden(a, s):
    a.melody(['fl'], ['A', 'B'], vel=80)
    a.arpeggio('harp', ['A', 'B'], step=0.5, lo=45, hi=76, vel=58, shape='up')
    a.ostinato(['vla_pizz'], ['A', 'B'], step=1, center=57, vel=54, pattern=(0, None, 2, None))
    a.pad([('vc', 45, 57)], ['A', 'B'], voices=1, vel=50)
    a.bass(['cb'], ['A', 'B'], 'whole', center=33, vel=60)
    a.drums(['A', 'B'], 'tom', vel=80, crash_first=False)
    a.counter('ob', ['B'], center=69, vel=50, beats=4)
    for bar in (a.section_bars(['A'])[0], a.section_bars(['B'])[0]):
        a.add('perc', a.bar_start(bar), 3, 83, 66, role='perc')  # bell tree


def arr_port(a, s):
    a.melody(['cl'], ['A'], vel=86)
    a.counter('bn', ['A'], center=52, vel=62, beats=3)
    a.bass(['cb_pizz'], ['A', 'B'], 'whole', center=38, vel=84)
    a.ostinato(['vln2_pizz', 'vla_pizz'], ['A', 'B'], step=1, center=62, vel=58, pattern=(None, 1, 2))
    a.arpeggio('harp', ['A', 'B'], step=0.5, lo=50, hi=79, vel=52, shape='up')
    a.drums(['A', 'B'], 'waltz', vel=96, crash_first=False)
    a.melody(['vln1', 'fl'], ['B'], vel=88)
    a.pad([('hn', 50, 65)], ['B'], voices=2, vel=52, rearticulate=3)
    a.pad([('vc', 43, 57)], ['B'], voices=1, vel=56, rearticulate=3)
    sparkle(a, ['B'], every=4)


def arr_shrine(a, s):
    a.pad([('org', 53, 72)], ['A', 'B'], voices=4, vel=64)
    a.melody(['vln1_q'], ['A'], vel=74)
    a.pad([('vla', 50, 64), ('vc', 41, 55)], ['A', 'B'], voices=2, vel=52)
    a.bass(['cb'], ['A', 'B'], 'whole', center=34, vel=62)
    a.arpeggio('harp', ['A', 'B'], step=1, lo=48, hi=79, vel=50, shape='up')
    a.melody(['fl', 'vln1_q'], ['B'], vel=78)
    for sec in ('A', 'B'):
        bar = a.section_bars([sec])[0]
        a.add('bells', a.bar_start(bar), 4, 65, 70, role='spk')
        a.add('bells', a.bar_start(bar) + 2, 4, 72, 56, role='spk')


def arr_stone(a, s):
    a.melody(['svln'], ['A'], vel=70)
    a.pad([('vln_trem', 69, 84)], ['A', 'B'], voices=2, vel=44)
    a.bass(['cb'], ['A', 'B'], 'pedal', center=40, vel=56)
    a.bass(['vc'], ['A'], 'pedal', center=52, vel=50)
    a.arpeggio('harp', ['A', 'B'], step=1, lo=52, hi=76, vel=48, shape='up')
    a.melody(['glock'], ['B'], vel=64, role='spk')
    a.melody(['fl'], ['B'], vel=66)
    a.pad([('hn_mute', 50, 64)], ['B'], voices=2, vel=56)
    for sec in ('A', 'B'):
        bar = a.section_bars([sec])[0]
        a.add('perc', a.bar_start(bar), 4, 101, 70, role='perc')  # bowed cymbal


PIECES = {
    'mq_orch_start_town': dict(
        title='はじまりのまち', key='G major', bpm=120, group='町・村・城', usage='No.02 はじまりのまち',
        motifs=[], form='A クラリネットとピチカート、タンバリン → B フルートとオーボエ、IV-V-iii-viの進行 → A2 バイオリン＋フルート、グロッケン',
        sections=[
            ('A', 'G D/F# Em C G/B C Am7 D', [
                'D5:.5 G5:.5 B5:1 A5:.5 G5:.5 D5:1', 'F#5:1 A5:1 D6:2', 'G5:1 E5:1 B4:1.5 C5:.5', 'E5:2 C5:1 G4:1',
                'D5:.5 G5:.5 B5:1 C6:.5 B5:.5 G5:1', 'E5:1 C6:1 G5:1 E5:1', 'A5:1.5 G5:.5 E5:1 C5:1', 'D5:2 F#5:1 A5:1']),
            ('B', 'C D Bm Em Am D G/B Cmaj7|D', [
                'G5:1.5 E5:.5 C5:2', 'A5:1.5 F#5:.5 D5:2', 'B5:1 A5:.5 F#5:.5 D5:2', 'E5:1 G5:1 B5:2',
                'C6:1.5 B5:.5 A5:1 E5:1', 'F#5:1 A5:1 D6:2', 'B5:1 G5:1 D5:1 G5:1', 'E5:2 F#5:1 A5:1']),
            ('A2', 'G D/F# Em C G/B C Am7 D7', [
                'D5:.5 G5:.5 B5:1 A5:.5 G5:.5 D5:1', 'F#5:1 A5:1 D6:2', 'G5:1 E5:1 B4:1.5 C5:.5', 'E5:2 C5:1 G4:1',
                'D5:.5 G5:.5 B5:1 C6:.5 B5:.5 G5:1', 'E5:1 C6:1 G5:1 E5:1', 'A5:1.5 G5:.5 E5:1 C5:1', 'D5:1 F#5:1 A5:1 C6:1']),
        ], arrange=arr_start_town),
    'mq_orch_bie': dict(
        title='ビーエのむら', key='D major', bpm=120, meter=3, group='町・村・城', usage='No.04 ビーエのむら（山あいの村）',
        motifs=[], form='3拍子。A オーボエの牧歌、ピチカートの2・3拍目 → B フルート、借用のii-iv、ホルンの和音',
        sections=[
            ('A', 'D D G D Bm Em A7 A D D G Gm D/A A7 D D', [
                'F#5:2 A5:1', 'D6:1.5 C#6:.5 A5:1', 'B5:2 G5:1', 'A5:3', 'B5:1 A5:1 F#5:1', 'G5:2 E5:1', 'E5:1 F#5:1 G5:1', 'E5:3',
                'F#5:2 A5:1', 'D6:2 A5:1', 'B5:1.5 A5:.5 G5:1', 'Bb5:2 G5:1', 'A5:2 F#5:1', 'E5:1.5 F#5:.5 G5:1', 'D5:3', 'r:1 A4:1 D5:1']),
            ('B', 'G A F#m Bm G A D D Em A F#m Bm G A7 D A7', [
                'B5:2 D6:1', 'C#6:2 A5:1', 'A5:2 F#5:1', 'D5:2 B4:1', 'G5:1 B5:1 D6:1', 'C#6:1 B5:1 A5:1', 'F#5:3', 'A5:1 F#5:1 D5:1',
                'E5:2 G5:1', 'A5:2 C#6:1', 'C#6:1 B5:1 A5:1', 'B5:2 F#5:1', 'G5:1.5 A5:.5 B5:1', 'C#6:1 B5:1 G5:1', 'D6:3', 'E5:1 C#5:1 A4:1']),
        ], arrange=arr_bie),
    'mq_orch_castletown': dict(
        title='レインランドじょうかまち', key='B♭ major', bpm=125, group='町・村・城', usage='No.06 レインランドじょうかまち',
        motifs=[], form='A バイオリン＋フルートの快活な旋律、スピッカートとピチカート → B オーボエ＋クラリネット → A2 トランペットの対旋律と小太鼓',
        sections=[
            ('A', 'Bb F/A Gm Eb Bb/F Eb Cm7 F', [
                'F5:.5 F5:.5 Bb5:1 D6:1 C6:.5 Bb5:.5', 'A5:1 F5:1 C5:2', 'D5:.5 G5:.5 Bb5:1.5 A5:.5 G5:1', 'G5:2 Eb5:1 Bb4:1',
                'F5:.5 F5:.5 Bb5:1 D6:1 C6:.5 Bb5:.5', 'G5:1 Bb5:1 G5:1 Eb5:1', 'Eb5:1 G5:1 C6:1 Bb5:1', 'A5:2 F5:1 C5:1']),
            ('B', 'Eb F Dm Gm Cm F Bb F7', [
                'Bb5:1.5 G5:.5 Eb5:2', 'C6:1.5 A5:.5 F5:2', 'D6:1 A5:1 F5:1 D5:1', 'G5:2 Bb5:1 D6:1',
                'C6:1.5 Bb5:.5 G5:1 Eb5:1', 'F5:1 A5:1 C6:2', 'Bb5:2 D6:1 Bb5:1', 'A5:1 C6:1 A5:1 Eb5:1']),
            ('A2', 'Bb F/A Gm Eb Bb/F Eb Cm7 F7', [
                'F5:.5 F5:.5 Bb5:1 D6:1 C6:.5 Bb5:.5', 'A5:1 F5:1 C5:2', 'D5:.5 G5:.5 Bb5:1.5 A5:.5 G5:1', 'G5:2 Eb5:1 Bb4:1',
                'F5:.5 F5:.5 Bb5:1 D6:1 C6:.5 Bb5:.5', 'G5:1 Bb5:1 G5:1 Eb5:1', 'Eb5:1 G5:1 C6:1 Bb5:1', 'A5:1 F5:1 C5:1 Eb5:1']),
        ], arrange=arr_castletown),
    'mq_orch_castle': dict(
        title='レインランドじょう', key='E♭ major', bpm=80, group='町・村・城', usage='No.06 レインランドじょう（王の間）',
        motifs=[], form='A トランペットの儀礼的な旋律、ホルンと低音金管のコラール → B バイオリン＋オーボエ、ハープ',
        sections=[
            ('A', 'Eb Ab/Eb Eb Bb/D Cm Ab Fm7 Bb', [
                'Eb5:1.5 Bb4:.5 Eb5:1 G5:1', 'Ab5:2 C6:1 Ab5:1', 'G5:1.5 F5:.5 Eb5:1 Bb4:1', 'F5:3 D5:1',
                'Eb5:1.5 D5:.5 C5:1 G5:1', 'Ab5:1.5 G5:.5 Eb5:2', 'F5:1 Ab5:1 C6:1 Eb5:1', 'D5:2 F5:2']),
            ('B', 'Gm Cm Ab Eb/G Fm Bb Eb|Ab Bb7', [
                'D5:2 G5:1 Bb5:1', 'C6:2 G5:1 Eb5:1', 'Ab5:1.5 C6:.5 Eb5:2', 'G5:2 Bb5:1 G5:1',
                'Ab5:1.5 G5:.5 F5:1 C5:1', 'D5:1 F5:1 Bb5:2', 'G5:2 C6:2', 'Bb5:2 Ab5:1 F5:1']),
        ], arrange=arr_castle),
    'mq_orch_hidden': dict(
        title='かくれざと', key='A minor (pentatonic)', bpm=80, group='町・村・城', usage='No.10 かくれざと',
        motifs=[], form='五音音階の旋律をフルートで、ハープとピチカート、木の太鼓 → B オーボエが長い音で寄り添う',
        sections=[
            ('A', 'Am Am F G Am Em F G', [
                'E5:2 D5:1 C5:1', 'A4:3 C5:1', 'C5:1.5 D5:.5 A4:2', 'G4:1 A4:1 D5:2',
                'E5:1.5 G5:.5 A5:2', 'G5:2 E5:2', 'A5:2 C6:1 A5:1', 'G5:2 D5:2']),
            ('B', 'Dm7 Am F Em Dm7 Em F G', [
                'D5:1.5 E5:.5 C5:2', 'A4:2 C5:1 E5:1', 'A5:1.5 G5:.5 C5:2', 'E5:2 G5:2',
                'D5:1 C5:1 A4:2', 'G4:3 A4:1', 'C5:2 A4:2', 'D5:2 G4:1 A4:1']),
        ], arrange=arr_hidden),
    'mq_orch_port': dict(
        title='港町ダコハ', key='D major', bpm=125, meter=3, group='町・村・城', usage='No.12 港町ダコハ',
        motifs=[], form='3拍子の舟歌。A クラリネットとファゴット、ピチカート → B ロ短調に翳る、バイオリン＋フルート',
        sections=[
            ('A', 'D A D G D Bm E7 A D A Bm G D A7 D D', [
                'A4:1 D5:1 F#5:1', 'E5:2 C#5:1', 'D5:1 F#5:1 A5:1', 'B5:2 G5:1', 'A5:1.5 F#5:.5 D5:1', 'F#5:1 D5:1 B4:1', 'G#4:1 B4:1 D5:1', 'C#5:2 E5:1',
                'F#5:2 A5:1', 'E5:2 C#5:1', 'D5:1 F#5:1 B5:1', 'B5:1.5 A5:.5 G5:1', 'F#5:1 A5:1 D6:1', 'C#6:1 A5:1 G5:1', 'F#5:3', 'D5:1 E5:1 F#5:1']),
            ('B', 'Bm Bm G A Bm F#m G F# Bm Bm Em A D G A A7', [
                'F#5:2 D5:1', 'B4:2 D5:1', 'G5:1 B5:1 G5:1', 'A5:2 E5:1', 'F#5:1.5 E5:.5 D5:1', 'C#5:2 A4:1', 'B4:1 D5:1 G5:1', 'A#4:2 C#5:1',
                'D5:1 F#5:1 B5:1', 'B5:2 F#5:1', 'G5:1.5 F#5:.5 E5:1', 'C#5:2 E5:1', 'F#5:2 D5:1', 'G5:1 B5:1 D6:1', 'C#6:2 A5:1', 'G5:1 E5:1 C#5:1']),
        ], arrange=arr_port),
    'mq_orch_shrine': dict(
        title='ふっかつのほこら', key='F major', bpm=64, group='町・村・城', usage='No.15 ふっかつのほこら',
        motifs=[], form='オルガンと弦のコラール、ハープ、各区間の頭に鐘 → B フルートが加わる',
        sections=[
            ('A', 'F C/E Dm Bb F/A Gm7 C C', [
                'A5:2 C6:2', 'G5:2 E5:2', 'F5:2 A5:1 D6:1', 'D6:2 F5:2', 'C6:2 A5:2', 'Bb5:2 F5:1 G5:1', 'E5:2 G5:2', 'C5:4']),
            ('B', 'Bb F/A Gm Dm Bb F/C Gm7 C7', [
                'D5:2 F5:2', 'A5:2 C6:2', 'Bb5:2 G5:2', 'A5:2 F5:2', 'F5:1 Bb5:1 D6:2', 'C6:2 A5:2', 'Bb5:2 F5:2', 'E5:2 G5:1 Bb5:1']),
        ], arrange=arr_shrine),
    'mq_orch_stone': dict(
        title='いしのまち', key='E minor', bpm=75, group='町・村・城', usage='No.18 いしのまち（石になった町）',
        motifs=['世界の異常の動機'], form='独奏バイオリンが異常の動機をぽつりと、弦トレモロとE音の持続 → B グロッケンとフルート、弱音器付きホルン、弓で擦るシンバル',
        sections=[
            ('A', 'Em Em C B Em Em Fmaj7 B7', [
                'E5:1 F5:1 E5:1 A#4:1', 'B4:3 r:1', 'C5:1 E5:1 G5:2', 'F#5:3 D#5:1',
                'E5:1 F5:1 E5:1 A#4:1', 'G4:3 r:1', 'A4:1 C5:1 E5:2', 'D#5:2 F#5:1 A5:1']),
            ('B', 'Am Em F B Am C F B7', [
                'A5:2 E5:2', 'B4:2 G4:2', 'A4:1 C5:1 F5:2', 'F#5:2 D#5:2',
                'C6:2 A5:2', 'G5:2 E5:2', 'F5:1 A5:1 C6:2', 'B5:2 A5:1 F#5:1']),
        ], arrange=arr_stone),
}
