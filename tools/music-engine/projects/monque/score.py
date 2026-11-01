"""MONQUE SOUND LAB - orchestral test themes (original melodies, written for this test).

Shared leitmotif: the hero figure "5-1-2-3" (e.g. F-Bb-C-D in Bb) opens or
returns in every piece, in major, minor, augmented or driving form.
Notation: one string per bar, tokens "PITCH:beats" (r = rest).
Chords: one symbol per bar, or "A|B" for two halves of a bar.
"""

PIECES = {
    'mq_orch_title': dict(
        title='タイトル「幻の冒険の書」', key='B♭ major', bpm=96, style='title',
        sections=[
            ('A', 'Bb Dm/A Gm Gm/F Ebmaj7 Bb/D Cm7 F', [
                'F4:.5 Bb4:.5 C5:1 D5:2', 'F5:1.5 D5:.5 C5:1 A4:1', 'Bb4:2 D5:1 G5:1', 'F5:3 Eb5:1',
                'D5:1 Eb5:.5 F5:.5 G5:2', 'F5:1.5 D5:.5 Bb4:2', 'Eb5:1 D5:1 C5:1 Bb4:1', 'C5:3 r:1']),
            ('B', 'Gm Ebmaj7 Cm7 D Ebmaj7 Dm7 Cm7 F7', [
                'D5:2 Bb4:1 G4:1', 'G4:1 Bb4:1 D5:1.5 C5:.5', 'Eb5:2 D5:1 C5:1', 'A4:1 D5:1 F#5:2',
                'G5:1.5 F5:.5 Eb5:1 D5:1', 'F5:1 A5:1 C6:1 A5:1', 'G5:1 Eb5:1 C5:1 Bb4:1', 'A4:1 C5:1 Eb5:2']),
            ('A2', 'Bb F/A Gm Bb/F Eb Bb/D Cm7|F F', [
                'F4:.5 Bb4:.5 C5:1 D5:2', 'F5:1.5 D5:.5 C5:1 A4:1', 'Bb4:2 D5:1 G5:1', 'F5:2 G5:1 A5:1',
                'Bb5:2 G5:1 Eb5:1', 'F5:1.5 G5:.5 F5:1 D5:1', 'Eb5:1 D5:1 C5:1.5 D5:.5', 'C5:2 A4:1 F4:1']),
        ]),
    'mq_orch_town': dict(
        title='むら・まち（比較共通テーマ）', key='F major', bpm=100, style='town',
        sections=[
            ('A', 'F Bb/F F C/E Dm Bbmaj7 Gm7 C', [
                'C5:1 F5:1.5 G5:.5 A5:1', 'Bb5:1 A5:.5 G5:.5 F5:2', 'A5:1 C6:1 A5:1 F5:1', 'G5:3 E5:1',
                'F5:1 E5:.5 D5:.5 A4:2', 'D5:1 F5:1 A5:2', 'G5:1 F5:.5 D5:.5 Bb4:1 D5:1', 'C5:2 E5:1 G5:1']),
            ('B', 'Bb F/A Gm7 C Dm Eb Bb C7', [
                'D5:1 F5:1 Bb5:2', 'A5:1.5 G5:.5 F5:1 C5:1', 'Bb4:1 D5:1 F5:1 A5:1', 'G5:3 r:1',
                'A5:1 F5:1 D5:1 A4:1', 'G4:1 Bb4:1 Eb5:1.5 F5:.5', 'D5:2 F5:1 D5:1', 'C5:1 E5:1 G5:1 Bb5:1']),
            ('A2', 'F Bb/F F C/E Dm Bbmaj7 Gm7 C7', [
                'C5:1 F5:1.5 G5:.5 A5:1', 'Bb5:1 A5:.5 G5:.5 F5:2', 'A5:1 C6:1 A5:1 F5:1', 'G5:3 E5:1',
                'F5:1 E5:.5 D5:.5 A4:2', 'D5:1 F5:1 A5:2', 'G5:1 F5:.5 D5:.5 Bb4:1 D5:1', 'C5:1 G4:1 A4:1 Bb4:1']),
        ]),
    'mq_orch_field': dict(
        title='フィールド', key='D major', bpm=120, style='field',
        sections=[
            ('A', 'D D G/D D Bm G Em7 A', [
                'A4:.5 D5:.5 E5:.5 F#5:2.5', 'G5:.5 F#5:.5 E5:1 D5:1 A4:1', 'B4:.5 D5:.5 G5:1 B5:1.5 A5:.5', 'F#5:3 r:1',
                'F#5:.5 E5:.5 D5:1 B4:1 D5:1', 'G5:1.5 F#5:.5 E5:1 D5:1', 'E5:.5 F#5:.5 G5:1 B5:1 D6:1', 'C#6:2 A5:1 E5:1']),
            ('A2', 'D F#m G D/F# Em A/C# Bm7|E7 A7', [
                'A4:.5 D5:.5 E5:.5 F#5:2.5', 'C#6:1 A5:1 F#5:2', 'B5:1.5 A5:.5 G5:1 D5:1', 'F#5:1 A5:1 D6:2',
                'B5:1 G5:.5 F#5:.5 E5:2', 'C#5:1 E5:1 A5:1 C#6:1', 'D6:1 B5:1 G#5:1 E5:1', 'A5:2 G5:1 E5:1']),
            ('B', 'C D C D Bm G Em A', [
                'E5:1.5 G5:.5 C6:2', 'A5:1.5 F#5:.5 D5:2', 'E5:1 G5:1 C6:1 E6:1', 'D6:3 A5:1',
                'B5:1.5 F#5:.5 D5:2', 'D5:1 G5:1 B5:2', 'E5:1 G5:1 B5:1 E6:1', 'C#6:3 r:1']),
            ('C', 'D Bm G A D/F# G Em7|A A7', [
                'A4:.5 D5:.5 E5:.5 F#5:2.5', 'F#5:.5 G5:.5 F#5:1 D5:1 B4:1', 'B4:.5 D5:.5 G5:1 B5:1.5 A5:.5', 'A5:2 C#6:1 E5:1',
                'D6:1.5 C#6:.5 B5:1 A5:1', 'B5:1 G5:1 D5:1 G5:1', 'G5:1 F#5:1 E5:1 C#5:1', 'A5:2 G5:1 E5:1']),
        ]),
    'mq_orch_dungeon': dict(
        title='ダンジョン', key='D Dorian', bpm=80, style='dungeon',
        sections=[
            ('A', 'Dm G/D Dm G/D Bbmaj7 C Dm/F A', [
                'r:1 A4:1 D5:1 E5:1', 'F5:2 E5:1 B4:1', 'D5:3 A4:1', 'B4:1 D5:1 G5:1.5 F5:.5',
                'F5:2 D5:1 A4:1', 'E5:1 G5:1 C6:1 Bb5:1', 'A5:2 F5:1 D5:1', 'C#5:3 E5:1']),
            ('B', 'Dm Em7b5 F Bbmaj7 Gm7 Bb Em7b5 A7', [
                'D5:1 F5:1 A5:2', 'G5:1.5 F5:.5 E5:1 Bb4:1', 'A4:1 C5:1 F5:2', 'D5:1 F5:1 A5:1.5 G5:.5',
                'F5:2 D5:1 Bb4:1', 'D5:1 F5:1 Bb5:2', 'Bb5:1 G5:1 E5:1 D5:1', 'C#5:2 E5:1 G5:1']),
        ]),
    'mq_orch_boss': dict(
        title='ボス戦', key='E minor', bpm=150, style='boss',
        sections=[
            ('A', 'Em Em C D Em Em C B7', [
                'B4:.5 E5:.5 F#5:.5 G5:2.5', 'F#5:.5 E5:.5 D5:1 E5:1 B4:1', 'C5:.5 E5:.5 G5:1 C6:1.5 B5:.5', 'A5:2 F#5:1 D5:1',
                'B4:.5 E5:.5 F#5:.5 G5:2.5', 'A5:.5 G5:.5 F#5:1 G5:1 B5:1', 'C6:1.5 B5:.5 A5:1 G5:1', 'F#5:2 D#5:1 B4:1']),
            ('A2', 'Em G Am B C D Em/B B7', [
                'E5:1 G5:1 B5:1.5 A5:.5', 'G5:1 D5:1 B4:2', 'C5:.5 E5:.5 A5:1 C6:1.5 B5:.5', 'B5:2 F#5:1 D#5:1',
                'E5:1 G5:1 C6:2', 'D6:1.5 C6:.5 A5:1 F#5:1', 'G5:1 E5:1 B4:1 E5:1', 'D#5:1 F#5:1 A5:1 B5:1']),
            ('B', 'Am Em Am B7 C D Bm B', [
                'C6:2 B5:1 A5:1', 'G5:2 E5:2', 'A5:1 C6:1 B5:1 A5:1', 'F#5:3 D#5:1',
                'E5:2 G5:1 C6:1', 'D6:2 C6:1 A5:1', 'B5:2 F#5:1 D5:1', 'D#5:2 F#5:1 B5:1']),
            ('C', 'Em Em C D Em Em C B7', [
                'B4:.5 E5:.5 F#5:.5 G5:2.5', 'F#5:.5 E5:.5 D5:1 E5:1 B4:1', 'C5:.5 E5:.5 G5:1 C6:1.5 B5:.5', 'A5:2 F#5:1 D5:1',
                'B4:.5 E5:.5 F#5:.5 G5:2.5', 'A5:.5 G5:.5 F#5:1 G5:1 B5:1', 'C6:1.5 B5:.5 A5:1 G5:1', 'B5:1 A5:1 F#5:1 D#5:1']),
        ]),
}
