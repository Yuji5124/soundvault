import { readdir, readFile, writeFile, stat, mkdir } from 'node:fs/promises';
import { join, relative, extname, basename } from 'node:path';

const root = new URL('../public/sounds/', import.meta.url);
const output = new URL('../data/sounds.json', import.meta.url);
const publicOutput = new URL('../public/data/sounds.json', import.meta.url);
const supported = new Set(['.wav', '.mp3', '.ogg', '.m4a']);
const defaults = { tags: [], duration: 0, loop: false, volume: 0.8, license: 'UNKNOWN', source: '', author: '', favorite: false, notes: '' };

async function files(directory) { const entries = await readdir(directory, { withFileTypes: true }).catch(() => []); const result = []; for (const entry of entries) { const path = new URL(entry.name + (entry.isDirectory() ? '/' : ''), directory); if (entry.isDirectory()) result.push(...await files(path)); else if (supported.has(extname(entry.name).toLowerCase())) result.push(path); } return result; }
const old = JSON.parse(await readFile(output, 'utf8').catch(() => '[]'));
const oldByFile = new Map(old.map((sound) => [sound.file, sound]));
const soundFiles = await files(root);
const sounds = [];
for (const file of soundFiles) {
  const relativePath = relative(new URL('../public/', import.meta.url).pathname, file.pathname).split('\\').join('/');
  const publicPath = `/${relativePath}`;
  const metadata = oldByFile.get(publicPath) ?? {};
  const info = await stat(file);
  const category = basename(new URL('../public/sounds/', import.meta.url).pathname === file.pathname ? file.pathname : file.pathname.split('/').slice(-2, -1)[0]).toUpperCase();
  const stem = basename(file.pathname, extname(file.pathname));
  sounds.push({ id: metadata.id ?? stem.toLowerCase().replace(/[^a-z0-9]+/g, '_'), name: metadata.name ?? stem.replace(/[-_]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase()), file: publicPath, category: metadata.category ?? category, tags: metadata.tags ?? [category.toLowerCase()], duration: metadata.duration ?? 0, format: extname(file.pathname).slice(1).toLowerCase(), size: info.size, loop: metadata.loop ?? defaults.loop, volume: metadata.volume ?? defaults.volume, license: metadata.license ?? defaults.license, source: metadata.source ?? defaults.source, author: metadata.author ?? defaults.author, favorite: metadata.favorite ?? defaults.favorite, notes: metadata.notes ?? defaults.notes, ...(metadata.collections ? { collections: metadata.collections } : {}), createdAt: metadata.createdAt ?? new Date().toISOString() });
}
sounds.sort((a, b) => a.name.localeCompare(b.name));
const serialized = `${JSON.stringify(sounds, null, 2)}\n`;
await writeFile(output, serialized);
await mkdir(new URL('../public/data/', import.meta.url), { recursive: true });
await writeFile(publicOutput, serialized);
console.log(`Indexed ${sounds.length} sound${sounds.length === 1 ? '' : 's'} in data/sounds.json`);
