"""Fields and dungeons (original melodies for MONQUE SOUND LAB)."""
from pieces_places import sparkle


def arr_forest(a, s):
    a.melody(['ob'], ['A'], vel=82)
    a.arpeggio('harp', ['A', 'B', 'A2'], step=0.5, lo=50, hi=81, vel=56)
    a.ostinato(['vla_pizz', 'vln2_pizz'], ['A', 'A2'], step=0.5, center=64, vel=54, pattern=(None, 0, None, 1, None, 2, None, 1))
    a.bass(['cb_pizz'], ['A', 'A2'], 'root5', center=40, vel=80)
    a.counter('cl', ['A'], center=62, vel=54)
    a.drums(['A', 'B', 'A2'], 'town', vel=84, crash_first=False)
    a.melody(['fl', 'cl'], ['B'], vel=82)
    a.pad([('vln2', 62, 76), ('vla', 55, 69), ('vc', 45, 60)], ['B'], voices=3, vel=56)
    a.bass(['cb'], ['B'], 'half', center=38, vel=72)
    a.melody(['vln1'], ['A2'], vel=86)
    a.melody(['fl'], ['A2'], octave=12, vel=68)
    a.pad([('hn', 52, 67)], ['A2'], voices=2, vel=48)
    sparkle(a, ['A2'])


def arr_lake(a, s):
    a.melody(['cl'], ['A'], vel=84)
    a.bass(['cb'], ['A', 'B'], 'whole', center=36, vel=66)
    a.ostinato(['vla_pizz'], ['A'], step=1, center=60, vel=52, pattern=(None, 1, 2))
    a.arpeggio('harp', ['A', 'B'], step=0.5, lo=46, hi=74, vel=52, shape='up')
    a.pad([('vc', 43, 57)], ['A'], voices=1, vel=52, rearticulate=3)
    a.melody(['vln1'], ['B'], vel=86)
    a.counter('ob', ['B'], center=67, vel=56, beats=3)
    a.pad([('vla', 53, 67), ('vc', 43, 57)], ['B'], voices=2, vel=56, rearticulate=3)
    a.pad([('hn', 50, 62)], ['B'], voices=2, vel=46, rearticulate=3)


def arr_tower(a, s):
    S = ['A', 'B', 'C']
    a.ostinato(['vln2_spic', 'vla_spic'], S, step=0.5, center=60, vel=70, pattern=(0, 1, 2, 1, 0, 2, 1, 2))
    a.bass(['cb'], S, 'whole', center=36, vel=80)
    a.timpani(S, beats=(0, 2), vel=78, center=43)
    a.melody(['hn', 'cl'], ['A'], vel=88)
    a.pad([('vc', 43, 57)], ['A'], voices=1, vel=60)
    a.melody(['vln1'], ['B'], vel=90)
    a.melody(['ob'], ['B'], vel=72)
    a.pad([('hn', 50, 65)], ['B'], voices=2, vel=62)
    a.drums(['B'], 'tom', vel=86, crash_first=False)
    a.swell_into(s['C'], vel=84)
    a.melody(['vln1', 'ob'], ['C'], vel=96)
    a.counter('tpt', ['C'], center=70, vel=86)
    a.pad([('tbn', 43, 60)], ['C'], voices=3, vel=76)
    a.drums(['C'], 'title', vel=86)
    a.timpani(['C'], beats=(), roll_last_bar=True, center=43)


def arr_iwayama(a, s):
    S = ['A', 'B', 'A2', 'B2']
    a.ostinato(['vln2_spic', 'vla_spic'], S, step=0.5, center=64, vel=74, pattern=(0, 1, 2, 1))
    a.bass(['cb_spic'], S, 'drive8', center=36, vel=94)
    a.bass(['vc_spic'], S, 'drive8', center=48, vel=86)
    a.drums(S, 'boss', vel=88)
    a.timpani(S, beats=(0, 2.5), vel=88, center=43)
    a.melody(['vln1', 'fl'], ['A', 'A2'], vel=94)
    a.melody(['vln1'], ['B', 'B2'], vel=94)
    a.melody(['hn'], ['B', 'B2'], octave=-12, vel=78)
    a.stabs([('tpt_stac', 64, 79)], ['B', 'B2'], rhythm=((0, 0.5), (1.5, 0.5), (3, 0.5)), vel=86)
    a.counter('tpt', ['A2'], center=72, vel=80)
    a.pad([('tbn', 45, 60), ('tba', 33, 45)], ['B2'], voices=3, vel=78)
    for bar in (a.section_bars(['A2'])[0],):
        a.add('perc', a.bar_start(bar), 4, 49, 96, role='perc')


def arr_orochi_road(a, s):
    S = ['A', 'B', 'C']
    a.drums(S, 'march', vel=70, crash_first=False)
    a.bass(['cb'], S, 'march', center=36, vel=86)
    a.timpani(S, beats=(0, 2), vel=82, center=44)
    a.melody(['bn', 'vc'], ['A'], vel=90)
    a.pad([('hn', 48, 62)], ['A'], voices=2, vel=60)
    a.pad([('vla_trem', 55, 67)], ['A', 'B'], voices=2, vel=56)
    a.melody(['vln1'], ['B'], vel=92)
    a.melody(['hn'], ['B'], octave=-12, vel=76)
    a.swell_into(s['C'], vel=86)
    a.add('perc', a.bar_start(a.section_bars(['C'])[0]), 4, 46, 90, role='perc')  # gong
    a.melody(['tpt'], ['C'], vel=96)
    a.counter('vln1', ['C'], center=72, vel=74)
    a.pad([('tbn', 43, 60), ('tba', 31, 43)], ['C'], voices=3, vel=82)


PIECES = {
    'mq_orch_forest': dict(
        title='ビーエのもり', key='G major', bpm=120, group='フィールド・ダンジョン', usage='No.03 ビーエのもり／はじまりのもり',
        motifs=[], form='A オーボエとハープ、ピチカートの裏拍 → B フルート＋クラリネット、弦の和音 → A2 バイオリン＋フルート、グロッケン',
        sections=[
            ('A', 'G Am7 Bm7 C G/B Am7 D D7', [
                'D5:1 G5:1 B5:1.5 A5:.5', 'G5:1 E5:1 C5:2', 'D5:1 F#5:1 A5:2', 'G5:1.5 E5:.5 C5:2',
                'B4:1 D5:1 G5:1.5 F#5:.5', 'E5:1 G5:1 C6:1.5 B5:.5', 'A5:2 F#5:1 D5:1', 'C5:1 D5:1 F#5:1 A5:1']),
            ('B', 'Em C G D Em C Am7 D', [
                'B5:2 G5:1 E5:1', 'E5:1 G5:1 C6:2', 'B5:1.5 A5:.5 G5:1 D5:1', 'F#5:2 A5:2',
                'G5:1 B5:1 E5:2', 'C6:1.5 B5:.5 G5:1 E5:1', 'A5:1 C6:1 E5:1 G5:1', 'F#5:2 D5:1 A4:1']),
            ('A2', 'G Am7 Bm7 C G/B Am7 D D7', [
                'D5:1 G5:1 B5:1.5 A5:.5', 'G5:1 E5:1 C5:2', 'D5:1 F#5:1 A5:2', 'G5:1.5 E5:.5 C5:2',
                'B4:1 D5:1 G5:1.5 F#5:.5', 'E5:1 G5:1 C6:1.5 B5:.5', 'A5:2 F#5:1 D5:1', 'A5:2 F#5:1 D5:1']),
        ], arrange=arr_forest),
    'mq_orch_lake': dict(
        title='みずうみの古城', key='G minor', bpm=96, meter=3, group='フィールド・ダンジョン', usage='No.11 みずうみの古城',
        motifs=[], form='3拍子の哀しいワルツ。A クラリネット、チェロ、ハープ → B 第1バイオリンとオーボエの対旋律、変ホ長調へ',
        sections=[
            ('A', 'Gm Gm Cm D Gm Eb Am7b5 D7 Gm Gm Cm F Bb Eb Am7b5 D', [
                'D5:2 Bb4:1', 'G5:2 D5:1', 'Eb5:1.5 D5:.5 C5:1', 'F#5:2 A5:1', 'G5:2 Bb5:1', 'G5:1.5 F5:.5 Eb5:1', 'C5:1 Eb5:1 G5:1', 'F#5:2 D5:1',
                'D5:2 G5:1', 'Bb5:2 A5:.5 G5:.5', 'G5:1.5 F5:.5 Eb5:1', 'F5:2 C5:1', 'D5:1 F5:1 Bb5:1', 'G5:2 Eb5:1', 'Eb5:1 C5:1 A4:1', 'D5:3']),
            ('B', 'Eb Bb/D Cm Gm/Bb Ab Eb/G F7 Bb Eb D/F# Gm Cm Am7b5 D Gm D7', [
                'Bb5:2 G5:1', 'F5:2 D5:1', 'Eb5:1.5 G5:.5 C6:1', 'Bb5:2 G5:1', 'C6:2 Ab5:1', 'G5:2 Bb5:1', 'A5:1 C6:1 Eb5:1', 'D5:2 F5:1',
                'G5:2 Bb5:1', 'A5:2 F#5:1', 'G5:1.5 A5:.5 Bb5:1', 'C6:2 G5:1', 'C6:1 A5:1 Eb5:1', 'D5:2 F#5:1', 'G5:2 D5:1', 'F#5:1 A5:1 C6:1']),
        ], arrange=arr_lake),
    'mq_orch_tower': dict(
        title='デーマスのとう', key='C minor', bpm=120, group='フィールド・ダンジョン', usage='No.16 デーマスのとう',
        motifs=[], form='A 刻み続ける弦の上でホルン＋ファゴット → B 第1バイオリン、木の太鼓 → C トランペット、♭IIの和音で緊張',
        sections=[
            ('A', 'Cm Cm Ab Ab Fm Fm G G7', [
                'C4:2 Eb4:1 G4:1', 'C5:3 Bb4:.5 G4:.5', 'Ab4:2 C5:1 Eb5:1', 'Eb5:2 C5:2',
                'F4:2 Ab4:1 C5:1', 'F5:2 Eb5:1 C5:1', 'D5:2 B4:1 G4:1', 'B4:2 D5:1 F5:1']),
            ('B', 'Cm Bb Ab G Fm Eb Dm7b5 G', [
                'G5:2 C6:2', 'D6:2 Bb5:1 F5:1', 'C6:1.5 Bb5:.5 Ab5:1 Eb5:1', 'B5:2 G5:2',
                'Ab5:1.5 G5:.5 F5:1 C6:1', 'G5:2 Bb5:2', 'Ab5:1 F5:1 D5:1 C6:1', 'B5:2 D6:1 G5:1']),
            ('C', 'Cm Db Cm Db Ab Bbm G G7', [
                'C5:1 Eb5:1 G5:2', 'Ab5:2 F5:1 Db5:1', 'G5:1 Eb5:1 C5:2', 'Db5:2 F5:1 Ab5:1',
                'C6:2 Ab5:1 Eb5:1', 'Db6:2 Bb5:1 F5:1', 'B5:2 G5:1 D5:1', 'F5:2 D5:1 B4:1']),
        ], arrange=arr_tower),
    'mq_orch_iwayama': dict(
        title='いわやま崩落', key='A minor', bpm=150, group='フィールド・ダンジョン', usage='No.09 いわやまのどうくつ（崩落シューティング）',
        motifs=[], form='A バイオリン＋フルートの速い旋律、スピッカートと8分の低音 → B ホルン重ね、トランペットの打ち込み → A2・B2 総奏',
        sections=[
            ('A', 'Am F G Am Am F G E', [
                'A5:.5 E5:.5 A5:.5 B5:.5 C6:1 B5:.5 A5:.5', 'A5:1 F5:.5 C5:.5 F5:1 A5:1', 'G5:.5 D5:.5 G5:.5 A5:.5 B5:1 D6:1', 'C6:1.5 B5:.5 A5:2',
                'E5:.5 A5:.5 C6:1 B5:.5 A5:.5 E5:1', 'F5:1 A5:1 C6:1 A5:1', 'B5:1 G5:1 D5:1 G5:1', 'G#5:2 B5:1 E5:1']),
            ('B', 'F G Em Am Dm E F E7', [
                'C6:1.5 A5:.5 F5:2', 'D6:1.5 B5:.5 G5:2', 'B5:1 G5:1 E5:1 G5:1', 'A5:2 C6:1 E5:1',
                'D6:1 A5:1 F5:1 A5:1', 'G#5:1 B5:1 G#5:1 E5:1', 'A5:1 C6:1 F5:1 A5:1', 'B5:1 G#5:1 D6:1 B5:1']),
            ('A2', 'Am F G Am Am F G E', [
                'A5:.5 E5:.5 A5:.5 B5:.5 C6:1 B5:.5 A5:.5', 'A5:1 F5:.5 C5:.5 F5:1 A5:1', 'G5:.5 D5:.5 G5:.5 A5:.5 B5:1 D6:1', 'C6:1.5 B5:.5 A5:2',
                'E5:.5 A5:.5 C6:1 B5:.5 A5:.5 E5:1', 'F5:1 A5:1 C6:1 A5:1', 'B5:1 G5:1 D5:1 G5:1', 'G#5:2 B5:1 E5:1']),
            ('B2', 'F G Em Am Dm E F E7', [
                'C6:1.5 A5:.5 F5:2', 'D6:1.5 B5:.5 G5:2', 'B5:1 G5:1 E5:1 G5:1', 'A5:2 C6:1 E5:1',
                'D6:1 A5:1 F5:1 A5:1', 'G#5:1 B5:1 G#5:1 E5:1', 'A5:1 C6:1 F5:1 A5:1', 'B5:1 G#5:1 D6:1 B5:1']),
        ], arrange=arr_iwayama),
    'mq_orch_orochi_road': dict(
        title='オロチへの道', key='F minor', bpm=100, group='フィールド・ダンジョン', usage='No.20 オロチへの道',
        motifs=['主人公の主題（短調）', '世界の異常の動機'], form='A 重い行進、ファゴット＋チェロが短調の主題、♭IIの和音 → B 第1バイオリン＋ホルン → C ドラが鳴り、トランペットが異常の動機',
        sections=[
            ('A', 'Fm Fm Db C Fm Bbm Gb C', [
                'C4:.5 F4:.5 G4:.5 Ab4:2.5', 'G4:1 F4:1 C4:2', 'Db4:1 F4:1 Ab4:2', 'G4:2 E4:1 C4:1',
                'C4:.5 F4:.5 G4:.5 Ab4:2.5', 'Bb4:1 Db5:1 F4:2', 'Gb4:2 Bb4:1 Db5:1', 'C5:2 G4:1 E4:1']),
            ('B', 'Db Eb Cm Fm Bbm Gb C C7', [
                'F5:2 Ab5:1 Db6:1', 'G5:2 Bb5:1 Eb5:1', 'G5:1.5 Eb5:.5 C5:2', 'Ab5:2 F5:1 C5:1',
                'Db6:1.5 C6:.5 Bb5:1 F5:1', 'Gb5:2 Bb5:1 Db6:1', 'C6:2 G5:1 E5:1', 'Bb5:2 G5:1 E5:1']),
            ('C', 'Fm Gb/F Fm Bdim Fm Gb Db C', [
                'F4:.5 Gb4:.5 F4:.5 B4:1.5 C5:1', 'Db5:2 Bb4:1 Gb4:1', 'Ab4:1 C5:1 F5:2', 'F5:2 D5:1 B4:1',
                'C5:.5 F5:.5 G5:.5 Ab5:2.5', 'Gb5:2 Db5:1 Bb4:1', 'F5:1.5 Eb5:.5 Db5:1 Ab4:1', 'E5:2 G5:1 C5:1']),
        ], arrange=arr_orochi_road),
}
