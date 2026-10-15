"""Battles, card games, story scenes, victory jingle (original melodies for MONQUE SOUND LAB)."""
from pieces_places import sparkle


def arr_battle(a, s):
    S = ['A', 'B', 'A2', 'B2']
    a.ostinato(['vln2_spic', 'vla_spic'], S, step=0.5, center=62, vel=76, pattern=(0, 1, 2, 1, 0, 2, 1, 2))
    a.bass(['cb_spic'], S, 'synco', center=38, vel=80)
    a.bass(['vc_spic'], S, 'drive8', center=48, vel=84)
    a.drums(S, 'battle', vel=92)
    a.timpani(S, beats=(0, 2.5), vel=90, center=43)
    a.melody(['tpt', 'vln1'], ['A', 'A2'], vel=96)
    a.stabs([('hn_stac', 55, 70)], ['A', 'A2'], rhythm=((0, 0.5), (1.5, 0.5), (3, 0.5)), vel=88)
    a.melody(['vln1', 'fl'], ['B', 'B2'], vel=96)
    a.melody(['hn'], ['B', 'B2'], octave=-12, vel=76)
    a.stabs([('tpt_stac', 64, 79), ('tbn_stac', 45, 60)], ['B2'], rhythm=((0, 0.5), (3.5, 0.5)), vel=88)
    a.melody(['fl'], ['A2'], octave=12, vel=80)


def arr_card(a, s):
    a.melody(['xylo'], ['A', 'A2'], vel=86, legato=0.5)
    a.melody(['fl'], ['A', 'A2'], vel=72, legato=0.6)
    a.bass(['bn'], ['A', 'B', 'A2'], 'root5', center=45, vel=80)
    a.bass(['cb_pizz'], ['A', 'B', 'A2'], 'root5', center=36, vel=80)
    a.ostinato(['vln2_pizz', 'vla_pizz'], ['A', 'B', 'A2'], step=0.5, center=64, vel=60, pattern=(None, 0, None, 1, None, 2, None, 1))
    a.drums(['A', 'B', 'A2'], 'tom', vel=80, crash_first=False)
    a.drums(['A', 'B', 'A2'], 'town', vel=86, crash_first=False)
    a.melody(['cl'], ['B'], vel=84, legato=0.7)
    a.melody(['glock'], ['B'], vel=62, role='spk', legato=0.6)
    a.stabs([('hn_stac', 55, 67)], ['A2'], rhythm=((1, 0.25), (3, 0.25)), voices=2, vel=74)


def arr_gacha(a, s):
    a.melody(['glock'], ['A', 'A2'], vel=74, role='spk')
    a.melody(['fl'], ['A', 'A2'], vel=78)
    a.arpeggio('harp', ['A', 'B', 'A2'], step=0.25, lo=60, hi=91, vel=52, shape='up')
    a.ostinato(['vln2_pizz'], ['A', 'B', 'A2'], step=0.5, center=67, vel=56, pattern=(None, 0, None, 1, None, 2, None, 1))
    a.bass(['cb_pizz'], ['A', 'B', 'A2'], 'root5', center=40, vel=80)
    a.drums(['A', 'B', 'A2'], 'town', vel=90, crash_first=False)
    a.melody(['vln1'], ['B'], octave=-12, vel=86)
    a.melody(['fl'], ['B'], vel=72)
    a.pad([('vla', 55, 69)], ['B'], voices=2, vel=50)
    for sec in ('A', 'B', 'A2'):
        a.add('perc', a.bar_start(a.section_bars([sec])[0]), 3, 83, 70, role='perc')  # bell tree


def arr_bond(a, s):
    a.melody(['hn'], ['A'], vel=86)
    a.arpeggio('harp', ['A', 'B'], step=0.5, lo=44, hi=80, vel=56)
    a.pad([('vln2', 60, 75), ('vla', 53, 67), ('vc', 43, 57)], ['A'], voices=3, vel=54)
    a.bass(['cb'], ['A', 'B'], 'whole', center=34, vel=68)
    a.melody(['vln1', 'fl'], ['B'], vel=88)
    a.counter('hn', ['B'], center=62, vel=70)
    a.pad([('vla', 53, 67), ('vc', 43, 57)], ['B'], voices=2, vel=60)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=44)


def arr_sorrow(a, s):
    a.melody(['ob'], ['A'], vel=78)
    a.pad([('vln1_q', 65, 79), ('vla', 55, 67), ('vc', 43, 57)], ['A', 'B'], voices=3, vel=50)
    a.bass(['cb'], ['A', 'B'], 'whole', center=36, vel=56)
    a.arpeggio('harp', ['A', 'B'], step=1, lo=50, hi=77, vel=46, shape='up')
    a.melody(['svln'], ['B'], vel=78)
    a.counter('vc', ['B'], center=55, vel=58, beats=4)


def arr_anomaly(a, s):
    a.melody(['bn', 'vc'], ['A'], octave=-12, vel=82)
    a.pad([('vln_trem', 66, 82)], ['A', 'B'], voices=2, vel=48)
    a.pad([('vla_trem', 53, 65)], ['A', 'B'], voices=2, vel=46)
    a.bass(['cb'], ['A', 'B'], 'pedal', center=37, vel=60)
    a.arpeggio('harp', ['A', 'B'], step=1, lo=40, hi=64, vel=50, shape='up')
    a.melody(['glock'], ['A'], octave=12, vel=50, role='spk')
    a.melody(['svln'], ['B'], vel=74)
    a.pad([('hn_mute', 50, 64)], ['B'], voices=2, vel=56)
    a.add('perc', 0, 4, 46, 76, role='perc')  # gong
    for sec in ('A', 'B'):
        a.add('perc', a.bar_start(a.section_bars([sec])[0]) + 1, 4, 103, 72, role='perc')  # bowed cymbal
    a.timpani(['B'], beats=(), roll_last_bar=True, center=44)


def arr_choice(a, s):
    a.melody(['vc'], ['A'], vel=88)
    a.arpeggio('harp', ['A', 'B'], step=0.5, lo=48, hi=79, vel=52, shape='up')
    a.pad([('vln1_q', 64, 79), ('vla', 55, 67)], ['A'], voices=3, vel=50)
    a.bass(['cb'], ['A', 'B'], 'whole', center=33, vel=62)
    a.swell_into(s['B'], vel=74)
    a.melody(['vln1', 'fl'], ['B'], vel=90)
    a.melody(['hn'], ['B'], octave=-12, vel=72)
    a.pad([('vla', 55, 69), ('vc', 43, 57)], ['B'], voices=3, vel=62)
    a.pad([('tbn', 46, 60)], ['B'], voices=2, vel=54)
    a.timpani(['B'], beats=(0,), vel=70, center=43, roll_last_bar=True)


def arr_victory(a, s):
    a.melody(['tpt'], ['A'], vel=104)
    a.melody(['vln1'], ['A'], vel=90)
    a.counter('hn', ['A'], center=62, vel=92, beats=4)
    a.pad([('tbn', 46, 62), ('tba', 34, 46)], ['A'], voices=3, vel=88)
    a.pad([('vln2', 62, 77), ('vla', 55, 69), ('vc', 43, 57)], ['A'], voices=4, vel=72)
    a.bass(['cb'], ['A'], 'whole', center=34, vel=86)
    a.arpeggio('harp', ['A'], step=0.25, lo=58, hi=94, vel=60, shape='up')
    a.timpani(['A'], beats=(0, 1, 2, 3), vel=96, center=46)
    a.add('perc', 12, 4, 49, 104, role='perc')  # crash on the final chord
    a.add('perc', 8, 4, 39, 70, role='perc')  # snare roll into it


PIECES = {
    'mq_orch_battle': dict(
        title='通常戦闘', key='G minor', bpm=150, group='戦闘', usage='通常戦闘',
        motifs=[], form='A トランペット＋バイオリン、ホルンの刻み、シンコペーションするコントラバス → B バイオリン＋フルートとホルン → A2・B2 さらに厚く',
        sections=[
            ('A', 'Gm Gm Eb F Gm Gm Eb D', [
                'G5:1 D5:.5 G5:.5 Bb5:1 A5:1', 'G5:.5 F5:.5 D5:1 r:1 D5:.5 F5:.5', 'G5:1 Bb5:1 G5:.5 F5:.5 Eb5:1', 'F5:1.5 C5:.5 A4:1 C5:1',
                'G5:1 D5:.5 G5:.5 Bb5:1 C6:1', 'Bb5:1.5 A5:.5 G5:1 D5:1', 'Eb5:1 G5:1 Bb5:1 G5:1', 'F#5:2 A5:1 D5:1']),
            ('B', 'Cm D Gm Eb Cm D Eb D7', [
                'Eb5:1.5 G5:.5 C6:2', 'A5:1.5 F#5:.5 D5:2', 'Bb5:1 G5:1 D5:1 G5:1', 'G5:2 Eb5:1 Bb4:1',
                'C6:1 G5:1 Eb5:1 G5:1', 'F#5:1 A5:1 D5:2', 'Eb5:1 G5:1 Bb5:2', 'A5:2 F#5:1 D5:1']),
            ('A2', 'Gm Gm Eb F Gm Gm Eb D', [
                'G5:1 D5:.5 G5:.5 Bb5:1 A5:1', 'G5:.5 F5:.5 D5:1 r:1 D5:.5 F5:.5', 'G5:1 Bb5:1 G5:.5 F5:.5 Eb5:1', 'F5:1.5 C5:.5 A4:1 C5:1',
                'G5:1 D5:.5 G5:.5 Bb5:1 C6:1', 'Bb5:1.5 A5:.5 G5:1 D5:1', 'Eb5:1 G5:1 Bb5:1 G5:1', 'F#5:2 A5:1 D5:1']),
            ('B2', 'Cm D Gm Eb Cm D Eb D7', [
                'Eb5:1.5 G5:.5 C6:2', 'A5:1.5 F#5:.5 D5:2', 'Bb5:1 G5:1 D5:1 G5:1', 'G5:2 Eb5:1 Bb4:1',
                'C6:1 G5:1 Eb5:1 G5:1', 'F#5:1 A5:1 D5:2', 'Eb5:1 G5:1 Bb5:2', 'A5:2 F#5:1 D5:1']),
        ], arrange=arr_battle),
    'mq_orch_card': dict(
        title='ジャンカード対戦', key='C major', bpm=125, group='戦闘', usage='ジャンカード対戦（サブゲーム）',
        motifs=[], form='A シロフォン＋フルートの跳ねる旋律、ファゴットとピチカート → B クラリネットとグロッケン → A2 ホルンの合いの手',
        sections=[
            ('A', 'C Am Dm7 G7 C A7 Dm7 G7', [
                'E5:.5 G5:.5 C6:.5 r:.5 G5:.5 E5:.5 C5:1', 'A5:.5 r:.5 C6:.5 A5:.5 E5:1 r:1', 'F5:.5 A5:.5 C6:.5 r:.5 A5:1 F5:1', 'G5:1 F5:.5 D5:.5 B4:1 r:1',
                'E5:.5 G5:.5 C6:.5 r:.5 G5:.5 E5:.5 C5:1', 'C#6:.5 r:.5 A5:.5 G5:.5 E5:1 r:1', 'D6:.5 C6:.5 A5:.5 F5:.5 D5:1 r:1', 'B4:.5 D5:.5 F5:.5 G5:.5 B5:1 r:1']),
            ('B', 'F G Em Am Dm G C G7', [
                'A5:1 r:.5 F5:.5 C6:1 A5:1', 'B5:1 r:.5 G5:.5 D6:1 B5:1', 'G5:.5 E5:.5 B4:.5 E5:.5 G5:1 B5:1', 'C6:2 A5:1 r:1',
                'F5:.5 A5:.5 D6:.5 r:.5 A5:1 F5:1', 'G5:.5 B5:.5 D6:.5 r:.5 B5:1 G5:1', 'E5:1 G5:1 C6:1 r:1', 'B5:.5 A5:.5 G5:.5 F5:.5 D5:1 B4:1']),
            ('A2', 'C Am Dm7 G7 C A7 Dm7 G7', [
                'E5:.5 G5:.5 C6:.5 r:.5 G5:.5 E5:.5 C5:1', 'A5:.5 r:.5 C6:.5 A5:.5 E5:1 r:1', 'F5:.5 A5:.5 C6:.5 r:.5 A5:1 F5:1', 'G5:1 F5:.5 D5:.5 B4:1 r:1',
                'E5:.5 G5:.5 C6:.5 r:.5 G5:.5 E5:.5 C5:1', 'C#6:.5 r:.5 A5:.5 G5:.5 E5:1 r:1', 'D6:.5 C6:.5 A5:.5 F5:.5 D5:1 r:1', 'B4:.5 D5:.5 F5:.5 G5:.5 B5:1 r:1']),
        ], arrange=arr_card),
    'mq_orch_gacha': dict(
        title='ジャンカードガチャ', key='F major', bpm=120, group='戦闘', usage='ジャンカードガチャ',
        motifs=[], form='A グロッケン＋フルート、16分のハープのきらめき → B 第1バイオリン＋クラリネット → A2 くり返し、鈴の木',
        sections=[
            ('A', 'F Dm Bb C F Dm Gm7 C7', [
                'C6:.5 A5:.5 F5:.5 A5:.5 C6:1 A5:1', 'D6:1 A5:.5 F5:.5 D5:1 F5:1', 'F5:.5 Bb5:.5 D6:.5 Bb5:.5 F6:1 D6:1', 'E6:2 C6:1 G5:1',
                'A5:.5 C6:.5 F6:.5 C6:.5 A5:1 F5:1', 'F5:.5 A5:.5 D6:.5 A5:.5 F5:1 D5:1', 'Bb5:1 D6:1 F6:1 D6:1', 'E6:1 C6:1 Bb5:1 G5:1']),
            ('B', 'Bb C Am Dm Gm7 C F C7', [
                'D6:1.5 C6:.5 Bb5:2', 'C6:1.5 Bb5:.5 G5:2', 'A5:1 C6:1 E6:2', 'D6:2 F6:1 D6:1',
                'F6:1 D6:1 Bb5:1 G5:1', 'G5:1 C6:1 E6:2', 'F6:2 C6:1 A5:1', 'G5:1 Bb5:1 C6:1 E6:1']),
            ('A2', 'F Dm Bb C F Dm Gm7 C7', [
                'C6:.5 A5:.5 F5:.5 A5:.5 C6:1 A5:1', 'D6:1 A5:.5 F5:.5 D5:1 F5:1', 'F5:.5 Bb5:.5 D6:.5 Bb5:.5 F6:1 D6:1', 'E6:2 C6:1 G5:1',
                'A5:.5 C6:.5 F6:.5 C6:.5 A5:1 F5:1', 'F5:.5 A5:.5 D6:.5 A5:.5 F5:1 D5:1', 'Bb5:1 D6:1 F6:1 D6:1', 'E6:1 C6:1 Bb5:1 G5:1']),
        ], arrange=arr_gacha),
    'mq_orch_bond': dict(
        title='仲間', key='A♭ major', bpm=80, group='物語の場面', usage='仲間加入・絆の場面',
        motifs=['主人公の主題'], form='A ホルン独奏の主人公の主題、ハープと弦 → B バイオリン＋フルート、ホルンの対旋律',
        sections=[
            ('A', 'Ab Eb/G Fm Db Ab/C Db Bbm7 Eb', [
                'Eb4:.5 Ab4:.5 Bb4:.5 C5:2.5', 'Bb4:1 G4:1 Eb4:2', 'F4:1 Ab4:1 C5:2', 'F4:2 Ab4:1 Db5:1',
                'Eb4:.5 Ab4:.5 Bb4:.5 C5:2.5', 'Db5:1 F5:1 Ab4:2', 'Db5:1.5 C5:.5 Bb4:1 Ab4:1', 'G4:2 Bb4:1 Eb5:1']),
            ('B', 'Db Eb Cm7 Fm Bbm7 Eb Ab Eb7', [
                'F5:1.5 Ab5:.5 Db6:2', 'Bb5:1.5 G5:.5 Eb5:2', 'G5:1 Bb5:1 Eb5:2', 'Ab5:2 C6:1 F5:1',
                'Db6:1 Bb5:1 F5:1 Ab5:1', 'G5:2 Bb5:2', 'C6:1.5 Bb5:.5 Ab5:2', 'G5:1 Bb5:1 Db6:1 Bb5:1']),
        ], arrange=arr_bond),
    'mq_orch_sorrow': dict(
        title='悲しみ', key='D minor', bpm=64, group='物語の場面', usage='悲しみの場面',
        motifs=['焚き火の動機（短調）'], form='A オーボエが短調の焚き火の動機、弦の和音とハープ → B 独奏バイオリン、チェロの対旋律',
        sections=[
            ('A', 'Dm Bb Gm A Dm Gm/Bb Em7b5 A7', [
                'F5:1.5 E5:.5 D5:1 A4:1', 'Bb4:1 D5:1 F5:2', 'G5:2 F5:1 D5:1', 'E5:3 C#5:1',
                'F5:1.5 E5:.5 D5:1 A4:1', 'D5:1 G5:1 Bb5:2', 'Bb5:1 G5:1 E5:1 D5:1', 'C#5:3 r:1']),
            ('B', 'F C/E Dm Bb Gm Dm/F Em7b5 A', [
                'A5:2 C6:1 A5:1', 'G5:2 E5:2', 'F5:1.5 E5:.5 D5:1 A4:1', 'D5:2 F5:2',
                'Bb5:1.5 A5:.5 G5:1 D5:1', 'A5:2 F5:2', 'G5:1 E5:1 D5:2', 'C#5:2 E5:1 A4:1']),
        ], arrange=arr_sorrow),
    'mq_orch_anomaly': dict(
        title='世界の異常', key='C# minor', bpm=75, group='物語の場面', usage='不穏・世界の異常の場面',
        motifs=['世界の異常の動機'], form='A 低いファゴット＋チェロが異常の動機、トレモロとドラ → B 独奏バイオリン、弱音器付きホルン、弓で擦るシンバル',
        sections=[
            ('A', 'C#m D/C# C#m G C#m D Bbdim G#7', [
                'C#5:1 D5:1 C#5:1 G4:1', 'A4:2 F#4:2', 'E5:1 G#4:1 C#5:2', 'D5:2 B4:1 G4:1',
                'C#5:1 D5:1 C#5:1 G4:1', 'F#5:2 A4:2', 'E5:2 C#5:1 Bb4:1', 'G#4:2 C5:1 D#5:1']),
            ('B', 'F E Fm E Dm C#m D G#', [
                'A5:2 F5:1 C5:1', 'G#5:2 E5:1 B4:1', 'Ab5:2 F5:1 C5:1', 'G#5:3 r:1',
                'F5:1 A5:1 D6:2', 'C#6:1 D6:1 C#6:1 G5:1', 'F#5:2 D5:2', 'C6:2 G#5:1 D#5:1']),
        ], arrange=arr_anomaly),
    'mq_orch_choice': dict(
        title='主人公の選択', key='C major / A minor', bpm=80, group='物語の場面', usage='主人公の選択（ここに のこる／もとの せかいへ かえる）',
        motifs=['焚き火の動機', '主人公の主題'], form='A チェロ独奏の焚き火の動機（イ短調） → シンバルの膨らみ → B ハ長調で主人公の主題、バイオリン＋フルート＋ホルン',
        sections=[
            ('A', 'Am F C G Am F Dm7 E', [
                'E4:1.5 D4:.5 C4:1 A3:1', 'A3:1 C4:1 F4:2', 'E4:2 G4:2', 'D4:3 B3:1',
                'E4:1.5 D4:.5 C4:1 G3:1', 'A3:1 C4:1 A4:2', 'F4:1.5 E4:.5 D4:1 C4:1', 'B3:2 G#3:1 E4:1']),
            ('B', 'C G/B Am Em F C/E Dm7 G', [
                'G4:.5 C5:.5 D5:.5 E5:2.5', 'D5:1 B4:1 G4:2', 'A4:.5 C5:.5 E5:1 A5:2', 'G5:2 E5:1 B4:1',
                'A5:1.5 G5:.5 F5:1 C5:1', 'E5:1 G5:1 C6:2', 'C6:1 A5:1 F5:1 D5:1', 'D5:2 B4:1 G4:1']),
        ], arrange=arr_choice),
    'mq_orch_victory': dict(
        title='勝利ファンファーレ', key='B♭ major', bpm=120, loop=False, group='ジングル', usage='戦闘勝利（1回再生）',
        motifs=['主人公の主題（ファンファーレ）'], form='トランペットの三連打から主音へ、最後の和音にシンバル。約12秒、ループなし',
        sections=[
            ('A', 'Bb Eb F Bb Bb', [
                'F5:.5 F5:.5 F5:.5 Bb5:2.5', 'G5:.5 G5:.5 G5:.5 C6:1.5 Bb5:1', 'A5:1 C6:1 F5:1 A5:1', 'Bb5:4', 'r:4']),
        ], arrange=arr_victory),
}
