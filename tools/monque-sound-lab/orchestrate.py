"""Turn score.py (melody + chords per section) into orchestral parts.

Each part is a list of notes (start_beat, beats, pitch, velocity) bound to one
VSCO 2 CE instrument (.sfz). Roles: melody, pad, bass, arpeggio, ostinato,
counter-line (guide tones), brass stabs, timpani, percussion.
"""
import random

import pretty_midi as pm

NOTE = pm.note_name_to_number
QUALITY = {
    '': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'm7': [0, 3, 7, 10], 'maj7': [0, 4, 7, 11],
    'm7b5': [0, 3, 6, 10], 'dim': [0, 3, 6], 'sus4': [0, 5, 7], '6': [0, 4, 7, 9], 'm6': [0, 3, 7, 9],
}

# instrument: (sfz file, lowest, highest MIDI note, max sustain seconds)
INSTR = {
    'vln1': ('ViolinEnsSusVib.sfz', 55, 86, 8), 'vln2': ('ViolinEnsSusVib.sfz', 55, 86, 8),
    'vln1_q': ('ViolinEnsSusVib-Quiet.sfz', 55, 86, 8), 'vln_trem': ('ViolinEnsTrem.sfz', 55, 86, 7),
    'vln2_spic': ('ViolinEnsSpic.sfz', 55, 86, 1), 'vln2_pizz': ('ViolinEnsPizz.sfz', 55, 86, 2),
    'vla': ('ViolaEnsSusVib.sfz', 48, 86, 7), 'vla_spic': ('ViolaEnsSpic.sfz', 48, 86, 1),
    'vla_pizz': ('ViolaEnsPizz.sfz', 48, 86, 2), 'vla_trem': ('ViolaEnsTrem.sfz', 48, 86, 7),
    'vc': ('CelloEnsSusVib.sfz', 36, 77, 6), 'vc_spic': ('CelloEnsSpic.sfz', 36, 77, 1), 'vc_pizz': ('CelloEnsPizz.sfz', 36, 77, 2),
    'cb': ('ContrabassSusVB.sfz', 24, 60, 6), 'cb_spic': ('ContrabassSpic.sfz', 24, 60, 1), 'cb_pizz': ('ContrabassPizz.sfz', 24, 60, 2),
    'fl': ('FluteSusVib.sfz', 60, 96, 4.5), 'ob': ('OboeSusVib.sfz', 58, 89, 6), 'cl': ('ClarinetSus.sfz', 50, 90, 4.5),
    'bn': ('BassoonSus.sfz', 34, 75, 6), 'hn': ('FHornSus.sfz', 33, 77, 4), 'hn_stac': ('FHornStac.sfz', 33, 77, 1),
    'tpt': ('TrumpetSus.sfz', 52, 84, 5), 'tpt_stac': ('TrumpetStac.sfz', 52, 84, 1),
    'tbn': ('TromboneSus.sfz', 34, 65, 4), 'tbn_stac': ('TromboneStac.sfz', 34, 70, 1), 'tba': ('TubaSus.sfz', 29, 62, 3),
    'harp': ('Harp.sfz', 28, 101, 12), 'glock': ('Glockenspiel.sfz', 67, 96, 4),
    'svln': ('SViolinVib.sfz', 55, 96, 10), 'org': ('OrganQuiet.sfz', 36, 96, 11), 'bells': ('TubularBells.sfz', 60, 79, 13),
    'xylo': ('Xylophone.sfz', 55, 96, 1.5), 'hn_mute': ('FHornMute.sfz', 46, 77, 4),
    'timp': ('Timpani.sfz', 36, 60, 12), 'timp_roll': ('TimpaniRolls.sfz', 36, 60, 12), 'perc': ('GM-StylePerc.sfz', 32, 104, 12),
}
# GM-StylePerc keys in VSCO 2 CE
BD, SN, SN_ROLL, CRASH, SUS_HIT, SUS_SWELL, TAMB, TAMB_SHAKE, TRI, GONG, BELLTREE = 36, 38, 39, 49, 51, 48, 54, 53, 81, 46, 83


def parse_chord(sym):
    bass = None
    if '/' in sym:
        sym, bass = sym.split('/')
    root = sym[0] + (sym[1] if len(sym) > 1 and sym[1] in '#b' else '')
    q = sym[len(root):]
    r = NOTE(root + '4') % 12
    pcs = [(r + i) % 12 for i in QUALITY[q]]
    return dict(root=r, pcs=pcs, bass=NOTE(bass + '4') % 12 if bass else r, third=pcs[1], seventh=pcs[3] if len(pcs) > 3 else pcs[2])


def near(pc, center):
    base = center - ((center - pc) % 12)
    return base if center - base <= 6 else base + 12


class Arranger:
    def __init__(self, piece, seed=1):
        self.piece = piece
        self.parts = {}
        self.rng = random.Random(seed)
        self.bpb = piece.get('meter', 4)  # beats per bar
        self.bars = []  # (section, bar_index_in_piece, chord list [(beat_offset, beats, chord)], melody tokens, extra lines)
        b = 0
        for sec in piece['sections']:
            name, chords, melody = sec[:3]
            extras = sec[3] if len(sec) > 3 else {}
            syms = chords.split()
            assert len(syms) == len(melody), (piece['title'], name)
            for k, (sym, mel) in enumerate(zip(syms, melody)):
                halves = sym.split('|')
                span = self.bpb / len(halves)
                lines = {key: bars[k] for key, bars in extras.items()}
                self.bars.append(dict(section=name, bar=b, chords=[(i * span, span, parse_chord(h)) for i, h in enumerate(halves)], melody=mel, lines=lines))
                b += 1
        self.total_beats = self.bpb * len(self.bars)
        self.warnings = []

    # ---- helpers
    def add(self, part, start, beats, pitch, vel, role='mel'):
        inst = part.split('#')[0]
        part = inst + '#' + role
        lo, hi = INSTR[inst][1], INSTR[inst][2]
        if not lo <= pitch <= hi:
            self.warnings.append(f'{part}: pitch {pitch} out of range {lo}-{hi} at beat {start}')
            while pitch < lo:
                pitch += 12
            while pitch > hi:
                pitch -= 12
        max_beats = INSTR[inst][3] * self.piece['bpm'] / 60
        self.parts.setdefault(part, []).append((start, min(beats, max_beats), int(pitch), int(max(1, min(127, vel)))))

    def section_bars(self, sections):
        return [x for x in self.bars if x['section'] in sections]

    def chords_in(self, sections):
        for bar in self.section_bars(sections):
            for off, span, ch in bar['chords']:
                yield bar, bar['bar'] * self.bpb + off, span, ch

    # ---- roles
    def bar_start(self, bar):
        return bar['bar'] * self.bpb

    def melody(self, parts, sections, octave=0, vel=90, legato=0.98, line=None, role='mel'):
        """line=None plays the main melody; line='ctr' etc. plays a hand-written extra line of the section."""
        for bar in self.section_bars(sections):
            t = bar['bar'] * self.bpb
            tokens = bar['melody'] if line is None else bar['lines'].get(line, '')
            for tok in tokens.split():
                n, d = tok.split(':')
                d = float(d)
                if n != 'r':
                    accent = 6 if (t - bar['bar'] * self.bpb) == 0 else (3 if t % 1 == 0 else 0)
                    for p in parts:
                        self.add(p, t, d * legato, NOTE(n) + octave, vel + accent + self.rng.randint(-3, 3), role=role)
                t += d

    def pad(self, parts_ranges, sections, voices=3, vel=60, rearticulate=4):
        """parts_ranges: list of (part, lo, hi); voices spread over the parts (one voice each, or several)."""
        prev = None
        for bar, start, span, ch in self.chords_in(sections):
            lo = min(r[1] for r in parts_ranges)
            hi = max(r[2] for r in parts_ranges)
            cands = sorted(p for p in range(lo, hi + 1) if p % 12 in ch['pcs'])
            best = None
            for i in range(len(cands) - voices + 1):
                v = cands[i:i + voices]
                if ch['third'] not in [x % 12 for x in v]:
                    continue
                cost = sum(abs(a - b) for a, b in zip(v, prev)) if prev else abs(sum(v) / voices - (lo + hi) / 2)
                if best is None or cost < best[0]:
                    best = (cost, v)
            v = best[1] if best else cands[:voices]
            prev = v
            t = start
            while t < start + span - 1e-6:
                seg = min(rearticulate, start + span - t)
                for i, pitch in enumerate(v):
                    # voices ascend; parts_ranges are listed high to low
                    part = parts_ranges[len(parts_ranges) - 1 - min(i * len(parts_ranges) // voices, len(parts_ranges) - 1)][0]
                    self.add(part, t, seg * 0.97, pitch, vel + self.rng.randint(-2, 2), role='pad')
                t += seg

    def bass(self, parts, sections, pattern='whole', center=40, vel=84):
        pats = {
            'whole': [(0, 4, 0)], 'half': [(0, 2, 0), (2, 2, 0)],
            'root5': [(0, 1, 0), (2, 1, 7)],
            'march': [(0, 1, 0), (1, 1, 7), (2, 1, 0), (3, 1, 7)],
            'synco': [(0, 1.5, 0), (1.5, 1, 0), (2.5, 0.5, 7), (3, 0.5, 12), (3.5, 0.5, 0)],
            'drive8': [(i * 0.5, 0.45, 12 if i % 2 else 0) for i in range(8)],
            'pedal': [(0, 4, 0)],
        }
        for bar, start, span, ch in self.chords_in(sections):
            root = near(ch['bass'], center)
            if pattern == 'pedal':
                root = near(parse_chord(self.piece['key'].split()[0].replace('♭', 'b'))['root'], center)
            for off, d, iv in pats[pattern]:
                if off >= span:
                    continue
                for p in parts:
                    self.add(p, start + off, min(d, span - off) * 0.95, root + iv, vel - (6 if off % 1 else 0) + self.rng.randint(-3, 3), role='bass')

    def arpeggio(self, part, sections, step=0.5, lo=48, hi=84, vel=62, shape='updown'):
        for bar, start, span, ch in self.chords_in(sections):
            tones = sorted(p for p in range(lo, hi + 1) if p % 12 in ch['pcs'])
            base = near(ch['bass'], lo + 6)
            seq = [base] + [x for x in tones if x > base][:5]
            if shape == 'updown':
                seq = seq + seq[-2:0:-1]
            n = int(round(span / step))
            for i in range(n):
                self.add(part, start + i * step, step * 2.5, seq[i % len(seq)], vel + (8 if i == 0 else 0) + self.rng.randint(-4, 4), role='arp')

    def ostinato(self, parts, sections, step=0.5, center=62, vel=70, pattern=(0, 2, 1, 2)):
        for bar, start, span, ch in self.chords_in(sections):
            v = sorted(near(pc, center) for pc in ch['pcs'][:3])
            n = int(round(span / step))
            for i in range(n):
                if pattern[i % len(pattern)] is None:  # rest
                    continue
                acc = 10 if i % 4 == 0 else (4 if i % 2 == 0 else 0)
                for p in parts:
                    self.add(p, start + i * step, step * 0.8, v[pattern[i % len(pattern)] % len(v)], vel + acc + self.rng.randint(-3, 3), role='ost')

    def counter(self, part, sections, center=64, vel=66, beats=2):
        prev = center
        for bar, start, span, ch in self.chords_in(sections):
            t = start
            for k in range(max(1, int(span // beats))):
                cands = [near(ch['third'], prev), near(ch['seventh'], prev)]
                pitch = min(cands, key=lambda c: abs(c - prev) + abs(c - center) * 0.3)
                self.add(part, t, beats * 0.97, pitch, vel + self.rng.randint(-2, 2), role='ctr')
                prev, t = pitch, t + beats

    def stabs(self, parts_ranges, sections, rhythm=((0, 0.5), (1.5, 0.5), (3, 0.5)), voices=3, vel=96):
        for bar, start, span, ch in self.chords_in(sections):
            for off, d in rhythm:
                if off >= span:
                    continue
                for part, lo, hi in parts_ranges:
                    cands = sorted(p for p in range(lo, hi + 1) if p % 12 in ch['pcs'])
                    mid = (lo + hi) // 2
                    v = sorted(cands, key=lambda p: abs(p - mid))[:voices]
                    for pitch in v:
                        self.add(part, start + off, d, pitch, vel + self.rng.randint(-4, 4), role='stab')

    def timpani(self, sections, beats=(0,), vel=88, center=45, roll_last_bar=False):
        for bar, start, span, ch in self.chords_in(sections):
            for off in beats:
                if off < span:
                    pc = ch['root'] if off == 0 else (ch['root'] + 7) % 12
                    self.add('timp', start + off, 1, near(pc, center), vel + self.rng.randint(-5, 5), role='perc')
        if roll_last_bar:
            last = self.section_bars(sections)[-1]
            ch = last['chords'][-1][2]
            for i in range(self.bpb):  # crescendo roll into the next downbeat
                self.add('timp_roll', last['bar'] * self.bpb + i, 1.05, near(ch['root'], center), 60 + i * 56 // self.bpb, role='perc')

    def drums(self, sections, pattern, vel=80, crash_first=True):
        pats = {
            'march': [(0, BD, 0), (1, SN, -14), (1.5, SN, -24), (2, BD, -6), (2.5, SN, -24), (3, SN, -8), (3.75, SN, -26)],
            'boss': [(0, BD, 0), (1, SN, -2), (1.5, BD, -8), (2.5, BD, -6), (3, SN, 0), (3.5, SN, -18)],
            'town': [(1, TAMB, -26), (3, TAMB, -22), (3.5, TAMB_SHAKE, -34)],
            'title': [(0, BD, -10), (2, BD, -18)],
            'waltz': [(0, BD, -18), (1, TAMB, -32), (2, TAMB, -32)],
            'battle': [(0, BD, 0), (1, SN, -6), (2, BD, -4), (2.5, BD, -12), (3, SN, -2)],
            'tom': [(0, 77, -10), (1.5, 76, -20), (2, 77, -14), (3, 76, -18)],  # log drums
            'shuffle': [(0, BD, -10), (1, SN, -16), (1.67, SN, -30), (2, BD, -14), (3, SN, -16), (3.67, TAMB, -30)],
        }
        bars = self.section_bars(sections)
        for i, bar in enumerate(bars):
            t = bar['bar'] * self.bpb
            if crash_first and i == 0:
                self.add('perc', t, 4, CRASH, vel + 10, role='perc')
            if pattern == 'town' and i % 2 == 0:
                self.add('perc', t, 2, TRI, vel - 30, role='perc')
            for off, key, dv in pats[pattern]:
                self.add('perc', t + off, 0.5, key, vel + dv + self.rng.randint(-4, 4), role='perc')
            if pattern in ('march', 'boss', 'battle') and i % 4 == 3 and self.bpb == 4:  # fill
                for k in range(4):
                    self.add('perc', t + 3 + k * 0.25, 0.25, SN, vel - 20 + k * 6, role='perc')

    def swell_into(self, section_start_bar, vel=70):
        """Suspended-cymbal swell over the bar before a section start."""
        self.add('perc', (section_start_bar - 1) * self.bpb + 0.5, self.bpb - 0.5, SUS_SWELL, vel, role='perc')


def arrange(piece):
    a = Arranger(piece)
    S = [s[0] for s in piece['sections']]
    starts = {name: next(b['bar'] for b in a.bars if b['section'] == name) for name in S}
    if 'arrange' in piece:  # piece-specific orchestration written as code
        piece['arrange'](a, starts)
        return a
    style = piece['style']
    if style == 'title':
        a.melody(['vc'], ['A'], octave=-12, vel=90)
        a.melody(['hn'], ['A'], octave=-12, vel=80)
        a.pad([('vln1_q', 67, 84), ('vln2', 60, 76), ('vla', 53, 69)], ['A'], voices=4, vel=52)
        a.bass(['cb'], ['A', 'B'], 'whole', center=36, vel=80)
        a.arpeggio('harp', ['A', 'B', 'A2'], step=0.5, lo=46, hi=82, vel=58)
        a.timpani(['A'], beats=(0,), vel=78)
        a.melody(['fl', 'vln1'], ['B'], vel=84)
        a.counter('ob', ['B'], center=67, vel=62)
        a.pad([('vla', 50, 67), ('vc', 43, 60)], ['B'], voices=3, vel=56)
        a.pad([('hn', 50, 67)], ['B'], voices=2, vel=48)
        a.timpani(['B'], beats=(), roll_last_bar=True)
        a.swell_into(starts['A2'])
        a.melody(['tpt', 'vln1'], ['A2'], vel=98)
        a.melody(['fl'], ['A2'], octave=12, vel=82)
        a.counter('hn', ['A2'], center=62, vel=86)
        a.pad([('vln2', 62, 79), ('vla', 55, 72)], ['A2'], voices=4, vel=72)
        a.pad([('tbn', 46, 62)], ['A2'], voices=3, vel=78)
        a.bass(['cb', 'tba'], ['A2'], 'synco', center=38, vel=92)
        a.bass(['vc'], ['A2'], 'synco', center=50, vel=86)
        a.timpani(['A2'], beats=(0, 2), vel=92, roll_last_bar=True)
        a.drums(['A2'], 'title', vel=86)
        for bar in a.section_bars(['A2']):  # glockenspiel sparkle on downbeats
            first = bar['melody'].split()[0].split(':')[0]
            if first != 'r':
                a.add('glock', bar['bar'] * a.bpb, 1, NOTE(first) + 12, 60, role='spk')
    elif style == 'town':
        a.melody(['fl'], ['A'], vel=82)
        a.arpeggio('harp', ['A', 'B', 'A2'], step=0.5, lo=48, hi=79, vel=56)
        a.bass(['cb_pizz', 'vc_pizz'], ['A', 'A2'], 'root5', center=41, vel=80)
        a.ostinato(['vla_pizz'], ['A'], step=1, center=60, vel=58, pattern=(None, 1, None, 2))  # off-beat pizzicato chords
        a.counter('cl', ['A'], center=62, vel=56)
        a.drums(['A', 'B', 'A2'], 'town', vel=86, crash_first=False)
        a.melody(['ob'], ['B'], vel=82)
        a.pad([('vln2', 62, 77), ('vla', 55, 69), ('vc', 45, 60)], ['B'], voices=3, vel=54)
        a.bass(['cb'], ['B'], 'whole', center=38, vel=72)
        a.counter('fl', ['B'], center=76, vel=58)
        a.melody(['vln1'], ['A2'], vel=84)
        a.melody(['fl'], ['A2'], octave=12, vel=70)
        a.counter('vc', ['A2'], center=55, vel=66)
        a.pad([('hn', 53, 67)], ['A2'], voices=2, vel=46)
        for bar in a.section_bars(['A2']):
            first = bar['melody'].split()[0].split(':')[0]
            a.add('glock', bar['bar'] * a.bpb, 1, NOTE(first) + 12, 54, role='spk')
    elif style == 'field':
        a.melody(['vln1', 'fl'], ['A'], vel=88)
        a.ostinato(['vln2_spic', 'vla_spic'], ['A', 'A2', 'C'], step=0.5, center=62, vel=70)
        a.pad([('hn', 50, 67)], ['A'], voices=3, vel=64)
        a.bass(['cb'], ['A', 'A2'], 'march', center=38, vel=84)
        a.bass(['vc'], ['A', 'A2'], 'march', center=50, vel=78)
        a.drums(['A', 'A2', 'C'], 'march', vel=78)
        a.timpani(['A', 'A2', 'C'], beats=(0, 2), vel=80)
        a.melody(['vln1', 'ob'], ['A2'], vel=90)
        a.melody(['hn'], ['A2'], octave=-12, vel=74)
        a.counter('tpt', ['A2'], center=69, vel=70)
        a.melody(['fl', 'cl'], ['B'], vel=84)
        a.pad([('vln2', 62, 79), ('vla', 55, 69), ('vc', 43, 60)], ['B'], voices=3, vel=60)
        a.pad([('hn', 50, 65)], ['B'], voices=2, vel=52)
        a.arpeggio('harp', ['B'], step=0.5, lo=50, hi=83, vel=60)
        a.bass(['cb'], ['B'], 'half', center=38, vel=72)
        a.timpani(['B'], beats=(), roll_last_bar=True)
        a.swell_into(starts['C'])
        a.melody(['vln1', 'fl'], ['C'], vel=96)
        a.melody(['hn'], ['C'], octave=-12, vel=78)
        a.stabs([('tpt_stac', 62, 79), ('tbn_stac', 46, 62)], ['C'], rhythm=((0, 0.5), (2.5, 0.5)), vel=92)
        a.bass(['cb', 'tba'], ['C'], 'march', center=38, vel=94)
        a.bass(['vc'], ['C'], 'march', center=50, vel=88)
    elif style == 'dungeon':
        a.melody(['ob'], ['A'], vel=78)
        a.arpeggio('harp', ['A', 'B'], step=0.5, lo=50, hi=74, vel=58, shape='up')
        a.bass(['cb'], ['A'], 'pedal', center=38, vel=66)
        a.bass(['vc'], ['A'], 'pedal', center=50, vel=58)
        a.pad([('vln_trem', 69, 84)], ['A', 'B'], voices=2, vel=42)
        a.add('perc', 0, 4, GONG, 60, role='perc')
        a.timpani(['A', 'B'], beats=(0,), vel=58, center=43)
        a.melody(['bn', 'vc'], ['B'], octave=-12, vel=82)
        a.counter('fl', ['B'], center=79, vel=50)
        a.pad([('vla_trem', 55, 67)], ['B'], voices=2, vel=48)
        a.pad([('hn', 45, 60)], ['B'], voices=2, vel=44)
        a.bass(['cb'], ['B'], 'whole', center=36, vel=70)
        for bar in a.section_bars(['A', 'B'])[1::2]:
            a.add('glock', bar['bar'] * a.bpb + 2.5, 1, NOTE('A6') if bar['section'] == 'A' else NOTE('D7') - 12, 40, role='spk')
    elif style == 'boss':
        a.melody(['tpt', 'vln1'], ['A', 'C'], vel=98)
        a.ostinato(['vln2_spic', 'vla_spic'], ['A', 'A2', 'B', 'C'], step=0.5, center=64, vel=78, pattern=(0, 1, 2, 1, 0, 2, 1, 2))
        a.bass(['cb_spic'], ['A', 'A2', 'B', 'C'], 'drive8', center=36, vel=96)
        a.bass(['vc_spic'], ['A', 'A2', 'B', 'C'], 'drive8', center=48, vel=90)
        a.stabs([('hn_stac', 55, 70), ('tbn_stac', 45, 60)], ['A', 'A2', 'C'], vel=96)
        a.drums(['A', 'A2', 'B', 'C'], 'boss', vel=90)
        a.timpani(['A', 'A2', 'C'], beats=(0, 2.5), vel=96, center=43)
        a.melody(['vln1', 'fl'], ['A2'], vel=98)
        a.counter('tpt', ['A2'], center=72, vel=84)
        a.melody(['hn'], ['B'], octave=-12, vel=78)
        a.melody(['vc'], ['B'], octave=-12, vel=96)
        a.pad([('vln1_q', 67, 84)], ['B'], voices=2, vel=70)
        a.stabs([('tpt_stac', 64, 79)], ['B'], rhythm=((0, 0.5), (3.5, 0.5)), vel=90)
        a.timpani(['B'], beats=(0,), vel=88, center=43, roll_last_bar=True)
        a.swell_into(starts['C'], vel=86)
        a.melody(['fl'], ['C'], octave=12, vel=86)
        a.pad([('tbn', 45, 62), ('tba', 33, 45)], ['C'], voices=3, vel=82)
    return a
