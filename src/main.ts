import './styles.css';

type Category = 'UI' | 'ACTION' | 'ITEM' | 'ENVIRONMENT' | 'FX' | 'KIDS' | 'VOICE' | 'BGM';
type Sound = {
  id: string; name: string; file: string; category: Category; tags: string[];
  duration: number; format: string; size: number; loop: boolean; volume: number;
  license: string; source: string; author: string; favorite?: boolean; notes?: string;
  collections?: string[]; createdAt?: string;
};

const categories: Array<'ALL' | Category> = ['ALL', 'UI', 'ACTION', 'ITEM', 'ENVIRONMENT', 'FX', 'KIDS', 'VOICE', 'BGM'];
const baseUrl = import.meta.env.BASE_URL;
const assetUrl = (file: string) => `${baseUrl}${file.replace(/^\/+/, '')}`;
const formatDuration = (seconds: number) => `${Math.floor(seconds / 60)}:${(seconds % 60).toFixed(2).padStart(5, '0')}`;
const formatSize = (bytes: number) => bytes < 1024 ? `${bytes} B` : bytes < 1048576 ? `${(bytes / 1024).toFixed(1)} KB` : `${(bytes / 1048576).toFixed(1)} MB`;
const escapeHtml = (value: string) => value.replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[char] ?? char));
const codeUrl = (sound: Sound) => assetUrl(sound.file);

let sounds: Sound[] = [];
let activeCategory = 'ALL';
let query = '';
let durationFilter = 'all';
let formatFilter = 'all';
let loopFilter = 'all';
let licenseFilter = 'all';
let sortOrder = 'newest';
let favoritesOnly = false;
let activeAudio: HTMLAudioElement | null = null;
let activeId: string | null = null;
let favorites = new Set<string>(JSON.parse(localStorage.getItem('soundvault:favorites') ?? '[]'));

const app = document.querySelector<HTMLDivElement>('#app')!;

function renderShell() {
  app.innerHTML = `
    <header class="topbar">
      <div class="brand"><span class="brand-mark">S</span><div><h1>SOUNDVAULT</h1><p>Reusable Sound Asset Library</p></div></div>
      <a class="github-link" href="https://github.com/Yuji5124/soundvault" target="_blank" rel="noreferrer">GitHub ↗</a>
    </header>
    <main>
      <section class="hero">
        <div><p class="eyebrow">SOUND ASSET INDEX / ${new Date().getFullYear()}</p><h2>Find the right sound.<br><em>Ship it in seconds.</em></h2><p class="intro">A lightweight, searchable vault for reusable game and web audio.</p></div>
        <div class="stats"><strong id="result-count">0</strong><span>indexed sounds</span></div>
      </section>
      <section class="toolbar">
        <label class="search"><span>⌕</span><input id="search" type="search" placeholder="Search sounds, tags, author, license..." autocomplete="off"><kbd>/</kbd></label>
        <div class="category-tabs" id="categories">${categories.map((category) => `<button class="category ${category === activeCategory ? 'active' : ''}" data-category="${category}">${category}</button>`).join('')}</div>
      </section>
      <section class="controls">
        <div class="filter-group"><span class="control-label">FILTER</span>
          <select id="duration"><option value="all">Duration: Any</option><option value="short">&lt; 1 sec</option><option value="medium">1 – 3 sec</option><option value="long">3 – 10 sec</option><option value="verylong">10 sec +</option></select>
          <select id="format"><option value="all">Format: Any</option><option value="wav">WAV</option><option value="mp3">MP3</option><option value="ogg">OGG</option><option value="m4a">M4A</option></select>
          <select id="loop"><option value="all">Loop: Any</option><option value="loop">Loop</option><option value="oneshot">One shot</option></select>
          <select id="license"><option value="all">License: Any</option><option value="CC0">CC0</option><option value="CC-BY">CC-BY</option><option value="Original">Original</option><option value="UNKNOWN">Unknown</option></select>
        </div>
        <div class="view-group"><button id="favorites" class="text-button ${favoritesOnly ? 'selected' : ''}">☆ Favorites</button><select id="sort"><option value="newest">Newest</option><option value="name">Name</option><option value="shortest">Shortest</option><option value="longest">Longest</option><option value="size">File size</option></select></div>
      </section>
      <section id="grid" class="sound-grid" aria-live="polite"></section>
      <section id="empty" class="empty hidden"><div class="empty-icon">∿</div><h3>No sounds found</h3><p>Try another search or add files to <code>public/sounds/</code>.</p></section>
    </main>
    <div id="toast" class="toast" role="status"></div>
  `;
  bindControls();
}

function matchesDuration(sound: Sound) {
  if (durationFilter === 'short') return sound.duration < 1;
  if (durationFilter === 'medium') return sound.duration >= 1 && sound.duration <= 3;
  if (durationFilter === 'long') return sound.duration > 3 && sound.duration <= 10;
  if (durationFilter === 'verylong') return sound.duration > 10;
  return true;
}

function filteredSounds() {
  const words = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
  return sounds.filter((sound) => {
    const haystack = [sound.name, sound.category, ...sound.tags, sound.author, sound.license].join(' ').toLowerCase();
    return (!words.length || words.every((word) => haystack.includes(word))) && (activeCategory === 'ALL' || sound.category === activeCategory) && matchesDuration(sound) && (formatFilter === 'all' || sound.format.toLowerCase() === formatFilter) && (loopFilter === 'all' || (loopFilter === 'loop' ? sound.loop : !sound.loop)) && (licenseFilter === 'all' || sound.license.toLowerCase() === licenseFilter.toLowerCase()) && (!favoritesOnly || favorites.has(sound.id));
  }).sort((a, b) => sortOrder === 'name' ? a.name.localeCompare(b.name) : sortOrder === 'shortest' ? a.duration - b.duration : sortOrder === 'longest' ? b.duration - a.duration : sortOrder === 'size' ? b.size - a.size : (b.createdAt ?? '').localeCompare(a.createdAt ?? ''));
}

function card(sound: Sound) {
  const isPlaying = activeId === sound.id;
  const unknown = sound.license.toUpperCase() === 'UNKNOWN';
  return `<article class="sound-card ${isPlaying ? 'playing' : ''}" data-id="${escapeHtml(sound.id)}">
    <div class="card-top"><button class="play-button" data-action="play" aria-label="${isPlaying ? 'Stop' : 'Play'} ${escapeHtml(sound.name)}">${isPlaying ? '■' : '▶'}</button><div class="waveform"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><button class="favorite ${favorites.has(sound.id) ? 'on' : ''}" data-action="favorite" aria-label="Favorite">${favorites.has(sound.id) ? '★' : '☆'}</button></div>
    <div class="card-title"><div><h3>${escapeHtml(sound.name)}</h3><span class="file-name">${escapeHtml(sound.file.split('/').pop() ?? sound.file)}</span></div><span class="duration">${formatDuration(sound.duration)}</span></div>
    <div class="meta"><span class="category-badge">${escapeHtml(sound.category)}</span><span>${sound.format.toUpperCase()}</span><span>${formatSize(sound.size)}</span>${sound.loop ? '<span class="loop-badge">↻ LOOP</span>' : ''}</div>
    <div class="tags">${sound.tags.map((tag) => `<span>#${escapeHtml(tag)}</span>`).join('')}</div>
    ${unknown ? '<div class="license-warning">⚠ License unknown — verify before use</div>' : `<div class="license-line">${escapeHtml(sound.license)}${sound.author ? ` · ${escapeHtml(sound.author)}` : ''}</div>`}
    <div class="card-actions"><button data-action="copy-url">Copy URL</button><button data-action="copy-path">Copy path</button><button data-action="more">Use code <span>⌄</span></button><a href="${codeUrl(sound)}" download>Download</a></div>
    <div class="code-menu hidden"><button data-code="js">Copy JS</button><button data-code="three">Copy Three.js</button><button data-code="phaser">Copy Phaser</button></div>
  </article>`;
}

function renderCards() {
  const items = filteredSounds();
  document.querySelector('#result-count')!.textContent = String(items.length).padStart(2, '0');
  const grid = document.querySelector<HTMLDivElement>('#grid')!;
  grid.innerHTML = items.map(card).join('');
  document.querySelector('#empty')!.classList.toggle('hidden', items.length > 0);
}

function notify(message: string) {
  const toast = document.querySelector<HTMLDivElement>('#toast')!;
  toast.textContent = message; toast.classList.add('show');
  window.setTimeout(() => toast.classList.remove('show'), 1800);
}

async function copy(text: string, label: string) { await navigator.clipboard.writeText(text); notify(`${label} copied`); }

function codeFor(sound: Sound, type: string) {
  const url = codeUrl(sound);
  if (type === 'three') return `const listener = new THREE.AudioListener();\ncamera.add(listener);\n\nconst sound = new THREE.Audio(listener);\nconst loader = new THREE.AudioLoader();\n\nloader.load(\n  "${url}",\n  buffer => {\n    sound.setBuffer(buffer);\n    sound.setVolume(${sound.volume});\n    sound.play();\n  }\n);`;
  if (type === 'phaser') return `this.load.audio(\n  "${sound.id}",\n  "${url}"\n);`;
  return `const audio = new Audio("${url}");\naudio.volume = ${sound.volume};\naudio.play();`;
}

function handleCardClick(event: Event) {
  const target = event.target as HTMLElement;
  const button = target.closest<HTMLElement>('[data-action], [data-code]');
  if (!button) return;
  const sound = sounds.find((item) => item.id === button.closest<HTMLElement>('[data-id]')?.dataset.id);
  if (!sound) return;
  const action = button.dataset.action;
  if (action === 'play') {
    if (activeId === sound.id) { activeAudio?.pause(); activeAudio = null; activeId = null; renderCards(); return; }
    activeAudio?.pause(); activeAudio = new Audio(codeUrl(sound)); activeAudio.volume = sound.volume; activeId = sound.id; activeAudio.addEventListener('ended', () => { activeId = null; renderCards(); }); activeAudio.play().catch(() => notify('Audio could not be played')); renderCards();
  } else if (action === 'favorite') { favorites.has(sound.id) ? favorites.delete(sound.id) : favorites.add(sound.id); localStorage.setItem('soundvault:favorites', JSON.stringify([...favorites])); renderCards(); }
  else if (action === 'copy-url') copy(new URL(codeUrl(sound), window.location.href).href, 'URL');
  else if (action === 'copy-path') copy(sound.file, 'Path');
  else if (action === 'more') button.closest('.sound-card')?.querySelector('.code-menu')?.classList.toggle('hidden');
  else if (button.dataset.code) copy(codeFor(sound, button.dataset.code), `${button.dataset.code.toUpperCase()} code`);
}

function bindControls() {
  document.querySelector<HTMLInputElement>('#search')!.addEventListener('input', (event) => { query = (event.target as HTMLInputElement).value; renderCards(); });
  document.querySelector('#categories')!.addEventListener('click', (event) => { const button = (event.target as HTMLElement).closest<HTMLButtonElement>('[data-category]'); if (button) { activeCategory = button.dataset.category!; document.querySelectorAll('.category').forEach((item) => item.classList.toggle('active', item === button)); renderCards(); } });
  const select = (id: string, setter: (value: string) => void) => document.querySelector<HTMLSelectElement>(id)!.addEventListener('change', (event) => { setter((event.target as HTMLSelectElement).value); renderCards(); });
  select('#duration', (value) => durationFilter = value); select('#format', (value) => formatFilter = value); select('#loop', (value) => loopFilter = value); select('#license', (value) => licenseFilter = value); select('#sort', (value) => sortOrder = value);
  document.querySelector('#favorites')!.addEventListener('click', () => { favoritesOnly = !favoritesOnly; document.querySelector('#favorites')!.classList.toggle('selected', favoritesOnly); renderCards(); });
  document.querySelector('#grid')!.addEventListener('click', handleCardClick);
  window.addEventListener('keydown', (event) => { if (event.key === '/' && document.activeElement?.tagName !== 'INPUT') { event.preventDefault(); document.querySelector<HTMLInputElement>('#search')?.focus(); } });
}

async function init() { renderShell(); try { const response = await fetch(`${baseUrl}data/sounds.json`); sounds = await response.json() as Sound[]; renderCards(); } catch { notify('Could not load sounds.json'); } }
init();
