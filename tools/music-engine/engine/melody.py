"""Write each piece's main melody as a one-track MIDI (used by the melody-similarity check)."""
from pathlib import Path

import pretty_midi as pm


def write_melodies(pieces, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for pid, p in pieces.items():
        midi = pm.PrettyMIDI(initial_tempo=p['bpm'])
        lead = pm.Instrument(0, name='lead')
        spb, t = 60 / p['bpm'], 0.0
        for sec in p['sections']:
            for bar in sec[2]:
                for tok in bar.split():
                    n, d = tok.split(':')
                    d = float(d)
                    if n != 'r':
                        lead.notes.append(pm.Note(90, pm.note_name_to_number(n), t * spb, (t + d * 0.98) * spb))
                    t += d
        midi.instruments.append(lead)
        path = out_dir / f'{pid}.mid'
        midi.write(str(path))
        paths.append(path)
    return paths
