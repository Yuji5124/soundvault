"""Title C 「時の扉」 and title D 「旅立ちの朝」 (original melodies for MONQUE SOUND LAB)."""
from pieces_places import sparkle

TICK, TOCK = 76, 77  # VSCO 2 CE log drums, high / low


def clock(a, sections, vel=62):
    """Tick-tock on every beat, accent on the downbeat."""
    for bar in a.section_bars(sections):
        t = a.bar_start(bar)
        for beat in range(a.bpb):
            a.add('perc', t + beat, 0.5, TICK if beat % 2 == 0 else TOCK, vel + (8 if beat == 0 else 0), role='perc')


def arr_title_c(a, s):
    clock(a, ['A', 'D'], vel=60)
    a.pad([('vln2', 62, 76), ('vla', 54, 68)], ['A', 'D'], voices=3, vel=58)
    a.arpeggio('harp', ['A', 'D'], step=0.5, lo=49, hi=80, vel=56, shape='up')
    a.ostinato(['vln2_pizz'], ['A', 'D'], step=0.5, center=66, vel=44, pattern=(0, 1, 2, 1))
    a.melody(['ob'], ['A'], vel=88)
    a.pad([('vc', 44, 57)], ['A', 'D'], voices=1, vel=54)
    a.bass(['cb'], ['A', 'D'], 'pedal', center=37, vel=62)
    a.melody(['vln1'], ['B'], vel=88)
    a.counter('hn', ['B'], center=62, vel=74)
    a.pad([('vla', 54, 68), ('vc', 44, 57)], ['B'], voices=3, vel=60)
    a.arpeggio('harp', ['B', 'C'], step=0.5, lo=52, hi=84, vel=58)
    a.bass(['cb'], ['B', 'C'], 'half', center=38, vel=78)
    a.timpani(['B'], beats=(), roll_last_bar=True, center=44)
    a.swell_into(s['C'], vel=88)
    a.melody(['vln1'], ['C'], vel=82)
    a.melody(['fl'], ['C'], vel=90)
    a.melody(['hn'], ['C'], octave=-12, vel=54)
    a.counter('tpt', ['C'], center=72, vel=74)
    a.pad([('tbn', 47, 61), ('tba', 33, 47)], ['C'], voices=3, vel=70)
    a.pad([('vln2', 64, 79), ('vla', 56, 69)], ['C'], voices=3, vel=70)
    a.timpani(['C'], beats=(0, 2), vel=78, center=44)
    a.add('perc', a.bar_start(a.section_bars(['C'])[0]), 4, 49, 74, role='perc')  # crash only, no bass drum
    sparkle(a, ['C'], every=2, vel=62)
    a.melody(['ob'], ['D'], vel=88)
    a.melody(['glock'], ['D'], vel=50, role='spk')
    a.pad([('vla_trem', 54, 68)], ['D'], voices=2, vel=52)


def arr_title_d(a, s):
    a.melody(['tpt'], ['A'], vel=100)
    a.melody(['vln1'], ['A'], vel=86)
    a.counter('hn', ['A'], center=62, vel=86)
    a.pad([('tbn', 46, 62), ('tba', 33, 46)], ['A'], voices=3, vel=80)
    a.ostinato(['vln2_spic', 'vla_spic'], ['A', 'C'], step=0.5, center=64, vel=70, pattern=(0, 1, 2, 1))
    a.bass(['cb'], ['A', 'C'], 'march', center=38, vel=88)
    a.bass(['vc'], ['A', 'C'], 'march', center=50, vel=80)
    a.drums(['A', 'C'], 'march', vel=80)
    a.timpani(['A', 'C', 'D'], beats=(0, 2), vel=86, center=43)
    a.melody(['fl', 'cl'], ['B'], vel=86)
    a.pad([('vln2', 62, 77), ('vla', 55, 69), ('vc', 43, 57)], ['B'], voices=3, vel=60)
    a.arpeggio('harp', ['B'], step=0.5, lo=52, hi=84, vel=58)
    a.bass(['cb'], ['B'], 'half', center=36, vel=74)
    a.drums(['B'], 'town', vel=90, crash_first=False)
    a.swell_into(s['C'], vel=86)
    a.melody(['vln1', 'fl'], ['C'], vel=98)
    a.melody(['hn'], ['C'], octave=-12, vel=76)
    a.counter('tpt', ['C'], center=74, vel=86)
    sparkle(a, ['C'], every=2, vel=62, up=0)
    a.melody(['tpt', 'vln1'], ['D'], vel=100)
    a.pad([('tbn', 46, 62), ('tba', 33, 46)], ['D'], voices=3, vel=82)
    a.pad([('vln2', 62, 77), ('vla', 55, 69)], ['D'], voices=3, vel=68)
    a.bass(['cb', 'vc'], ['D'], 'synco', center=40, vel=86)
    a.drums(['D'], 'title', vel=88)
    a.timpani(['D'], beats=(), roll_last_bar=True, center=43)


PIECES = {
    'mq_orch_title_c': dict(
        title='タイトルC「時の扉」', key='C# minor → E major', bpm=100, group='正式8枠', usage='BGM01 タイトル / オープニング（C案）',
        motifs=['主人公の主題（短調→長調）'],
        form='A 木の打楽器の「チクタク」とハープ、ピチカートの上でオーボエが短調の主題 → B 第1バイオリン、ホルンの対旋律 → '
             'C ホ長調で主題が総奏、トランペットの対旋律 → D 時計の音に戻り、オーボエとグロッケン',
        sections=[
            ('A', 'C#m C#m A B C#m F#m D#m7b5 G#7', [
                'G#4:.5 C#5:.5 D#5:.5 E5:2.5', 'D#5:.5 C#5:.5 G#4:1 E5:1 C#5:1', 'E5:1.5 C#5:.5 A4:1 C#5:1', 'D#5:2 F#5:1 B4:1',
                'G#4:.5 C#5:.5 D#5:.5 E5:1.5 G#5:1', 'A5:1.5 G#5:.5 F#5:1 C#5:1', 'F#5:1 A5:1 C#5:2', 'D#5:2 C5:1 G#4:1']),
            ('B', 'A B G#m C#m F#m7 B E E', [
                'C#5:1 E5:1 A5:2', 'B5:1.5 A5:.5 F#5:2', 'G#5:1 B5:1 D#5:2', 'C#6:2 G#5:1 E5:1',
                'A5:1 C#6:1 E5:2', 'D#5:2 F#5:1 B5:1', 'B4:.5 E5:.5 F#5:.5 G#5:2.5', 'G#5:1 F#5:1 E5:2']),
            ('C', 'E B/D# C#m A E/G# A F#m7|B E', [
                'B4:.5 E5:.5 F#5:.5 G#5:2.5', 'F#5:1 D#5:1 B4:2', 'C#5:.5 E5:.5 G#5:1 C#6:2', 'A5:1.5 G#5:.5 E5:2',
                'G#5:1 B5:1 G#5:1 E5:1', 'A5:2 C#6:1 A5:1', 'A5:1 F#5:1 D#5:1 F#5:1', 'E5:2 B4:1 G#4:1']),
            ('D', 'C#m A F#m G# C#m A D#m7b5 G#7', [
                'E5:1 G#5:1 C#6:2', 'C#6:1.5 B5:.5 A5:2', 'A5:1 F#5:1 C#5:2', 'D#5:2 C5:1 G#4:1',
                'G#4:.5 C#5:.5 D#5:.5 E5:2.5', 'E5:1 C#5:1 A4:2', 'A4:1 C#5:1 F#5:2', 'F#5:1 D#5:1 C5:1 G#4:1']),
        ], arrange=arr_title_c),
    'mq_orch_title_d': dict(
        title='タイトルD「旅立ちの朝」', key='C major → D major', bpm=125, group='正式8枠', usage='BGM01 タイトル / オープニング（D案）',
        motifs=['主人公の主題（ファンファーレ）'],
        form='A トランペットのファンファーレ、刻む弦と行進の小太鼓 → B フルート＋クラリネットの歌、ハープ → '
             'C 全音上のニ長調へ転調、バイオリン＋フルートとホルン → D ハ長調へ戻って総奏、ティンパニのロールで頭へ',
        sections=[
            ('A', 'C C F G Am F D7 G', [
                'G4:.5 C5:.5 D5:.5 E5:1 G5:1.5', 'G5:1 E5:.5 G5:.5 C6:2', 'A5:1.5 G5:.5 F5:1 C5:1', 'D5:1 G5:1 B5:2',
                'C6:1.5 B5:.5 A5:1 E5:1', 'F5:1 A5:1 C6:2', 'F#5:1.5 A5:.5 C6:1 A5:1', 'B5:2 G5:1 D5:1']),
            ('B', 'Em Am F C/E Dm7 G Em7 A7', [
                'B5:2 G5:1 E5:1', 'C6:2 A5:1 E5:1', 'A5:1.5 C6:.5 F5:2', 'E5:1 G5:1 C6:2',
                'D6:1.5 C6:.5 A5:1 F5:1', 'B5:2 D6:1 G5:1', 'G5:1 B5:1 D6:2', 'C#6:2 A5:1 G5:1']),
            ('C', 'D D G A Bm G E7 A7', [
                'A4:.5 D5:.5 E5:.5 F#5:1 A5:1.5', 'A5:1 F#5:.5 A5:.5 D6:2', 'B5:1.5 A5:.5 G5:1 D5:1', 'E5:1 A5:1 C#6:2',
                'D6:1.5 C#6:.5 B5:1 F#5:1', 'G5:1 B5:1 D6:2', 'G#5:1.5 B5:.5 D6:1 B5:1', 'C#6:2 A5:1 G5:1']),
            ('D', 'G Em Am F C/G Dm7 G G7', [
                'D5:1 G5:1 B5:1.5 A5:.5', 'G5:2 E5:1 B4:1', 'A5:1 C6:1 E5:2', 'F5:1.5 A5:.5 C6:2',
                'G5:1 C6:1 E5:2', 'F5:1 A5:1 C6:2', 'B5:2 G5:1 D5:1', 'F5:1 D5:1 B4:1 G4:1']),
        ], arrange=arr_title_d),
}
