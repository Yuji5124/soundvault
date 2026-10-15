"""Title B, final battle, ending, 'もういちど' (original melodies for MONQUE SOUND LAB).

Motifs: HERO 5-1-2-3 / CAMPFIRE 3-2-1-5(low) 6(low)-1-2 / ANOMALY 1-b2-1-#4
"""


def arr_title_b(a, s):
    S = ['A', 'B', 'C', 'D']
    a.ostinato(['vln2_spic', 'vla_spic'], S, step=0.5, center=62, vel=74, pattern=(0, 1, 2, 1, 0, 2, 1, 2))
    a.bass(['cb_spic'], ['A', 'D'], 'drive8', center=38, vel=94)
    a.timpani(['A', 'D'], beats=(0, 2.5), vel=96, center=43)
    a.drums(['A', 'D'], 'title', vel=92)
    a.melody(['hn'], ['A', 'D'], vel=92)
    a.melody(['vc'], ['A', 'D'], vel=96)
    a.melody(['bn'], ['A'], vel=80)
    a.stabs([('tpt_stac', 62, 79), ('tbn_stac', 46, 62)], ['D'], rhythm=((0, 0.5), (1.5, 0.5), (3, 0.5)), vel=90)
    a.melody(['vln1', 'fl'], ['B'], vel=92)
    a.pad([('hn', 50, 67)], ['B'], voices=3, vel=66)
    a.pad([('tbn', 43, 60)], ['B'], voices=2, vel=62)
    a.arpeggio('harp', ['B'], step=0.5, lo=50, hi=84, vel=62)
    a.bass(['cb', 'tba'], ['B', 'C'], 'synco', center=38, vel=90)
    a.timpani(['B'], beats=(0,), vel=86, center=43, roll_last_bar=True)
    a.swell_into(s['C'], vel=90)
    a.melody(['vln1', 'fl'], ['C'], vel=100)
    a.melody(['hn'], ['C'], octave=-12, vel=80)
    a.counter('tpt', ['C'], center=72, vel=88)
    a.pad([('tbn', 46, 62)], ['C'], voices=3, vel=80)
    a.drums(['C'], 'march', vel=84)
    a.timpani(['C'], beats=(0, 2), vel=92, center=43)
    for bar in a.section_bars(['C']):
        first = bar['melody'].split()[0].split(':')[0]
        a.add('glock', a.bar_start(bar), 1, a_note(first) + 12, 62, role='spk')


def arr_final(a, s):
    S = ['A', 'B', 'C', 'D']
    a.ostinato(['vln2_spic', 'vla_spic'], S, step=0.5, center=60, vel=82, pattern=(0, 1, 2, 1, 0, 2, 1, 2))
    a.bass(['cb_spic'], S, 'drive8', center=36, vel=82)
    a.drums(S, 'boss', vel=94)
    a.timpani(['A', 'C', 'D'], beats=(0, 2, 2.5), vel=100, center=43)
    a.melody(['hn', 'vc', 'bn'], ['A'], vel=100)
    a.stabs([('tbn_stac', 41, 58)], ['A', 'C'], rhythm=((0, 0.5), (0.75, 0.25), (2.5, 0.5)), vel=96)
    a.melody(['vln1'], ['B'], vel=96)
    a.melody(['fl'], ['B'], vel=84)
    a.pad([('vla_trem', 55, 69)], ['B'], voices=2, vel=70)
    a.pad([('hn', 50, 65)], ['B'], voices=3, vel=72)
    a.stabs([('tpt_stac', 64, 79)], ['B'], rhythm=((0, 0.5), (3.5, 0.5)), vel=90)
    a.timpani(['B'], beats=(0,), vel=92, center=43, roll_last_bar=True)
    a.swell_into(s['C'], vel=94)
    a.melody(['tpt', 'vln1'], ['C'], vel=102)
    a.counter('hn', ['C'], center=62, vel=92)
    a.pad([('tbn', 43, 60), ('tba', 31, 43)], ['C'], voices=3, vel=86)
    a.add('perc', a.bar_start(a.section_bars(['D'])[0]), 4, 46, 96, role='perc')  # gong
    a.melody(['vln1', 'fl'], ['D'], vel=100)
    a.melody(['hn'], ['D'], octave=-12, vel=82)
    a.pad([('vln_trem', 62, 77)], ['D'], voices=2, vel=74)
    a.timpani(['D'], beats=(), roll_last_bar=True)


def arr_ending(a, s):
    a.melody(['fl'], ['A'], vel=80)
    a.melody(['vln1'], ['A'], vel=74)
    a.arpeggio('harp', ['A', 'B', 'C'], step=0.5, lo=46, hi=82, vel=58)
    a.pad([('vla', 55, 69), ('vc', 43, 60)], ['A', 'B'], voices=3, vel=58)
    a.bass(['cb'], ['A', 'B', 'C'], 'whole', center=36, vel=70)
    a.counter('cl', ['A'], center=63, vel=56)
    a.melody(['hn'], ['B'], vel=84)
    a.counter('vln1_q', ['B'], center=72, vel=58)
    a.counter('ob', ['B'], center=70, vel=54, beats=4)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=43)
    a.swell_into(s['C'], vel=72)
    a.melody(['vln1', 'fl'], ['C'], vel=90)
    a.melody(['hn'], ['C'], line='ctr', vel=64, role='ctr')
    a.pad([('vln2', 62, 77), ('vla', 55, 69), ('vc', 43, 60)], ['C'], voices=4, vel=68)
    a.pad([('tbn', 46, 60)], ['C'], voices=2, vel=56)
    a.timpani(['C'], beats=(0,), vel=70, center=43)
    for bar in a.section_bars(['C'])[::2]:
        first = bar['melody'].split()[0].split(':')[0]
        a.add('glock', a.bar_start(bar), 1, a_note(first) + 12, 54, role='spk')


def arr_again(a, s):
    a.melody(['svln'], ['A'], vel=76)
    a.arpeggio('harp', ['A', 'B'], step=0.5, lo=45, hi=79, vel=56, shape='up')
    a.pad([('vla', 55, 67), ('vc', 43, 57)], ['A', 'B'], voices=2, vel=50)
    a.bass(['cb'], ['A', 'B'], 'whole', center=33, vel=58)
    a.melody(['fl'], ['B'], vel=72)
    a.melody(['svln'], ['B'], octave=-12, vel=66)
    a.counter('cl', ['B'], center=62, vel=50)
    for bar in a.section_bars(['A', 'B'])[::4]:
        first = bar['melody'].split()[0].split(':')[0]
        a.add('glock', a.bar_start(bar), 1, a_note(first) + 12, 44, role='spk')


def a_note(name):
    import pretty_midi as pm
    return pm.note_name_to_number(name)


PIECES = {
    'mq_orch_title_b': dict(
        title='タイトルB「黎明の剣」', key='D minor', bpm=120, group='正式8枠', usage='BGM01 タイトル / オープニング（B案）',
        motifs=['主人公の主題（短調）'], form='A 低弦とホルンが短調の主題、刻む弦とティンパニ → B ヘ長調へ開ける歌 → C 総奏の主題、トランペット対旋律 → D 金管の打ち込みと♭IIの劇的な終止',
        sections=[
            ('A', 'Dm Dm Bb C Dm Dm Gm A', [
                'A3:.5 D4:.5 E4:.5 F4:2.5', 'E4:.5 D4:.5 C4:1 D4:2', 'D4:.5 F4:.5 Bb4:1.5 A4:.5 F4:1', 'G4:1.5 E4:.5 C4:2',
                'A3:.5 D4:.5 E4:.5 F4:1.5 A4:1', 'G4:.5 F4:.5 E4:1 D4:1 F4:1', 'Bb4:1.5 A4:.5 G4:1 D4:1', 'C#4:2 E4:1 A4:1']),
            ('B', 'Bb C Am Dm Bb C Dm A', [
                'F5:1.5 D5:.5 Bb4:1 D5:1', 'E5:1.5 G5:.5 C6:2', 'C6:1 A5:1 E5:1 A5:1', 'F5:3 E5:.5 D5:.5',
                'D5:1 F5:1 Bb5:1.5 A5:.5', 'G5:1 E5:1 C5:1 G5:1', 'A5:2 F5:1 A5:1', 'C#6:2 E5:1 A5:1']),
            ('C', 'F C/E Dm Bb Gm C Bb A', [
                'C5:.5 F5:.5 G5:.5 A5:2.5', 'G5:.5 F5:.5 E5:1 C5:1 G5:1', 'F5:1 A5:1 D6:1.5 C6:.5', 'Bb5:2 F5:1 D5:1',
                'G5:1 Bb5:1 D6:1 Bb5:1', 'C6:2 G5:1 E5:1', 'F5:1 D5:.5 F5:.5 Bb5:1 A5:1', 'A5:2 C#5:1 E5:1']),
            ('D', 'Dm Bb/D Dm C/D Bb Gm Eb A', [
                'D4:1 F4:1 A4:1.5 G4:.5', 'F4:2 D4:1 Bb3:1', 'A3:.5 D4:.5 E4:.5 F4:2.5', 'E4:1 G4:1 C5:2',
                'D5:1.5 C5:.5 Bb4:1 F4:1', 'G4:1 Bb4:1 D5:2', 'Eb5:1.5 D5:.5 Bb4:1 G4:1', 'A4:2 C#5:1 E5:1']),
        ], arrange=arr_title_b),
    'mq_orch_final': dict(
        title='最終戦「オロチ」', key='C minor', bpm=160, group='正式8枠', usage='BGM06 最終戦',
        motifs=['世界の異常の動機', '主人公の主題（短調）'], form='A 異常の動機を低音総出で → B 高弦の悲劇的な歌 → C 主人公の主題が短調で総奏 → D 半音で崩れていく和声、ドラ',
        sections=[
            ('A', 'Cm Db/C Cm Ab Fm Db G G7', [
                'C4:.5 Db4:.5 C4:.5 F#4:1.5 G4:1', 'Ab4:1 F4:1 Db4:1 C4:1', 'Eb4:.5 D4:.5 C4:1 G4:1 C5:1', 'Eb5:2 C5:1 Ab4:1',
                'F4:1 Ab4:1 C5:1.5 Bb4:.5', 'Ab4:2 F4:1 Db4:1', 'B3:1 D4:1 G4:1 B4:1', 'D5:2 B4:1 F4:1']),
            ('B', 'Cm Ab Eb Bb Fm Ab Dm7b5 G7', [
                'G5:2 Eb5:1 C5:1', 'C6:2 Ab5:1 Eb5:1', 'Bb5:1.5 G5:.5 Eb5:1 G5:1', 'F5:2 D5:1 Bb4:1',
                'Ab5:1 C6:1 F5:1 Ab5:1', 'C6:2 Eb5:1 Ab5:1', 'C6:1 Ab5:1 F5:1 D5:1', 'B4:1 D5:1 F5:1 G5:1']),
            ('C', 'Cm Bb Ab G Cm Bb Ab G7', [
                'G4:.5 C5:.5 D5:.5 Eb5:2.5', 'D5:.5 C5:.5 Bb4:1 F4:1 D5:1', 'C5:1 Eb5:1 Ab5:1.5 G5:.5', 'G5:2 D5:1 B4:1',
                'G4:.5 C5:.5 D5:.5 Eb5:2.5', 'F5:1 D5:1 Bb4:1 D5:1', 'Eb5:1 C5:1 Ab4:1 C5:1', 'B4:1 D5:1 F5:1 G5:1']),
            ('D', 'Cm Bdim Bbm A Ab G Ab G', [
                'C6:.5 Db6:.5 C6:.5 F#5:1.5 G5:1', 'F5:1 D5:1 B4:1 D5:1', 'Db6:1 Bb5:1 F5:1 Db5:1', 'C#6:1 A5:1 E5:1 C#5:1',
                'C6:2 Ab5:1 Eb5:1', 'B5:2 G5:1 D5:1', 'Ab5:1 C6:1 Ab5:1 Eb5:1', 'G5:1 B5:1 D6:1 B5:1']),
        ], arrange=arr_final),
    'mq_orch_ending': dict(
        title='エンディング', key='E♭ major', bpm=80, group='正式8枠', usage='BGM07 エンディング',
        motifs=['焚き火の動機', '主人公の主題'], form='A フルートとバイオリンが焚き火の動機 → B ホルン独奏で主人公の主題 → C 二つの動機を重ねた総奏',
        sections=[
            ('A', 'Eb Bb/D Cm Ab Eb/G Ab Fm7 Bb', [
                'G5:1.5 F5:.5 Eb5:2', 'Bb4:2 D5:1 F5:1', 'C5:1 Eb5:1 G5:1.5 F5:.5', 'Eb5:3 C5:1',
                'G5:1.5 F5:.5 Eb5:1 Bb4:1', 'C5:1 Eb5:1 Ab5:2', 'Ab5:1 G5:.5 F5:.5 Eb5:2', 'F5:3 r:1']),
            ('B', 'Eb Bb/D Cm Gm/Bb Ab Eb/G Fm7 Bb7', [
                'Bb3:.5 Eb4:.5 F4:.5 G4:2.5', 'F4:1 D4:1 Bb3:2', 'C4:.5 Eb4:.5 G4:1 C5:2', 'Bb4:2 G4:1 D4:1',
                'C5:1.5 Bb4:.5 Ab4:1 Eb4:1', 'G4:1.5 Ab4:.5 Bb4:2', 'Ab4:1 C5:1 Eb5:1 C5:1', 'D5:2 Ab4:1 F4:1']),
            ('C', 'Eb Bb/D Cm Ab Eb/G Ab Fm7 Bb', [
                'G5:1.5 F5:.5 Eb5:2', 'Bb4:2 D5:1 F5:1', 'C5:1 Eb5:1 G5:1.5 F5:.5', 'Eb5:3 C5:1',
                'G5:1.5 F5:.5 Eb5:1 Bb4:1', 'C5:1 Eb5:1 Ab5:2', 'Ab5:1 G5:.5 F5:.5 Eb5:2', 'F5:2 D5:1 Bb4:1'],
             {'ctr': ['Bb3:.5 Eb4:.5 F4:.5 G4:2.5', 'F4:2 D4:2', 'Eb4:2 G4:2', 'Ab4:2 Eb4:2',
                      'Bb3:.5 Eb4:.5 F4:.5 G4:2.5', 'Ab4:2 C5:2', 'Ab4:2 Eb4:2', 'D4:2 F4:2']}),
        ], arrange=arr_ending),
    'mq_orch_again': dict(
        title='もういちど', key='A minor', bpm=75, group='正式8枠', usage='BGM08 特殊枠（「もういちど」の焚き火）',
        motifs=['焚き火の動機'], form='A 独奏バイオリンとハープで焚き火の動機 → B フルートが受け継ぎ、最後に焚き火の動機へ戻る',
        sections=[
            ('A', 'Am F6 C G Am F6 Dm7 E', [
                'E5:1.5 D5:.5 C5:1 G4:1', 'A4:1 C5:1 D5:2', 'E5:2 G5:1 E5:1', 'D5:3 r:1',
                'E5:1.5 D5:.5 C5:1 G4:1', 'A4:1 C5:1 D5:1 F5:1', 'F5:1.5 E5:.5 D5:1 C5:1', 'B4:2 G#4:1 E4:1']),
            ('B', 'F G Em7 Am Dm7 G C E7', [
                'C5:1 F5:1 A5:2', 'G5:1.5 F5:.5 D5:2', 'E5:1 G5:1 B5:1.5 A5:.5', 'A5:2 E5:2',
                'F5:1 A5:1 C6:1.5 B5:.5', 'B5:2 G5:1 D5:1', 'E5:1.5 D5:.5 C5:1 G4:1', 'G#4:2 B4:1 D5:1']),
        ], arrange=arr_again),
}
