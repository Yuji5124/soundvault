import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const root = join(new URL('../public/sounds/', import.meta.url).pathname);
const samples = [
  ['ui', 'soft-click-001.wav', 440], ['action', 'jump-001.wav', 660], ['item', 'coin-001.wav', 880],
  ['environment', 'rain-loop-001.wav', 220], ['fx', 'spark-001.wav', 990], ['kids', 'happy-001.wav', 523], ['bgm', 'calm-loop-001.wav', 330],
];
function wav(frequency, seconds = 0.35) { const rate = 44100; const count = Math.floor(rate * seconds); const data = Buffer.alloc(count * 2); for (let i = 0; i < count; i++) { const envelope = Math.min(1, i / 500) * Math.min(1, (count - i) / 3000); data.writeInt16LE(Math.floor(Math.sin(i * Math.PI * 2 * frequency / rate) * 13000 * envelope), i * 2); } const header = Buffer.alloc(44); header.write('RIFF', 0); header.writeUInt32LE(36 + data.length, 4); header.write('WAVE', 8); header.write('fmt ', 12); header.writeUInt32LE(16, 16); header.writeUInt16LE(1, 20); header.writeUInt16LE(1, 22); header.writeUInt32LE(rate, 24); header.writeUInt32LE(rate * 2, 28); header.writeUInt16LE(2, 32); header.writeUInt16LE(16, 34); header.write('data', 36); header.writeUInt32LE(data.length, 40); return Buffer.concat([header, data]); }
for (const [category, name, frequency] of samples) { const directory = join(root, category); await mkdir(directory, { recursive: true }); const path = join(directory, name); try { await writeFile(path, wav(frequency, category === 'bgm' || category === 'environment' ? 1.2 : 0.35), { flag: 'wx' }); } catch (error) { if (error.code !== 'EEXIST') throw error; } }
console.log(`Generated ${samples.length} local demo WAV files.`);
