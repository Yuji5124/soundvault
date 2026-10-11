import './styles.css';
import './project-styles.css';
import { loadProjects, saveProjects, type Project } from './projects';

type Category = 'UI' | 'ACTION' | 'ITEM' | 'ENVIRONMENT' | 'FX' | 'KIDS' | 'VOICE' | 'BGM';
type Sound = {
  id: string; name: string; file: string; category: Category; tags: string[];
  duration: number; format: string; size: number; loop: boolean; volume: number;
  license: string; source: string; author: string; favorite?: boolean; notes?: string;
  collections?: string[]; createdAt?: string; projectIds?: string[];
};

const categories: Array<'ALL' | Category> = ['ALL', 'UI', 'ACTION', 'ITEM', 'ENVIRONMENT', 'FX', 'KIDS', 'VOICE', 'BGM'];
const baseUrl = import.meta.env.BASE_URL;
const assetUrl = (file: string) => `${baseUrl}${file.replace(/^\/+/, '')}`;
const formatDuration = (seconds: number) => `${Math.floor(seconds / 60)}:${(seconds % 60).toFixed(2).padStart(5, '0')}`;
const formatSize = (bytes: number) => bytes < 1024 ? `${bytes} B` : bytes < 1048576 ? `${(bytes / 1024).toFixed(1)} KB` : `${(bytes / 1048576).toFixed(1)} MB`;
const escapeHtml = (value: string) => value.replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[char] ?? char));
const codeUrl = (sound: Sound) => assetUrl(sound.file);

let sounds: Sound[] = [];
const projectState = loadProjects();
let projectView = 'all';
let projectFilter = 'all';
let projectTypeFilter = 'all';
function projectsFor(sound: Sound): Project[] {
  const ids = projectState.assignments[sound.id] ?? sound.projectIds ?? [];
  return projectState.projects.filter(project => ids.includes(project.id));
}
function persistProjects() {
  try { saveProjects(projectState); } catch { notify('保存できません。JSON を書き出して保管してください。'); }
}
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
      <section class="project-tools">
        <label>種別 <select id="project-view"><option value="all">すべて</option><option value="active">Project</option><option value="archive">Project Archive</option><option value="unassigned">未分類</option></select></label>
        <label>Project の種類 <select id="project-type-filter"></select></label>
        <label>Project <select id="project-filter"></select></label>
        <button id="manage-projects">Project 管理</button>
      </section>
      <dialog id="project-dialog">
        <h2>Project 管理</h2><p>このブラウザに保存されます。共有する場合は JSON を書き出してください。</p>
        <form id="project-form"><label>Project 名 <input name="name" placeholder="桃太郎" required maxlength="100"></label><label>Project の種類 <input name="type" list="project-types" placeholder="紙芝居" required maxlength="100"></label><datalist id="project-types"><option value="紙芝居"><option value="ゲーム"><option value="Web アプリ"><option value="その他"></datalist><button>追加</button></form>
        <div id="project-list"></div><button id="export-projects">JSON 書き出し</button><button id="close-projects">閉じる</button>
      </dialog>
      <dialog id="assignment-dialog"><h2>効果音の Project</h2><form id="assignment-form"><div id="assignment-options"></div><button>保存</button><button type="button" id="close-assignment">キャンセル</button></form></dialog>
      <section id="grid" class="sound-grid" aria-live="polite"></section>
      <section id="empty" class="empty hidden"><div class="empty-icon">∿</div><h3>No sounds found</h3><p>Try another search or add files to <code>public/sounds/</code>.</p></section>
    </main>
    <div id="toast" class="toast" role="status"></div>
  `;
  bindControls();
  bindProjects();
}

function refreshProjectControls() {
  const option = (value: string, label: string) => `<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`;
  document.querySelector('#project-filter')!.innerHTML = option('all', 'すべて') + projectState.projects.map(p => option(p.id, p.name)).join('');
  document.querySelector('#project-type-filter')!.innerHTML = option('all', 'すべて') + [...new Set(projectState.projects.map(p => p.type))].map(type => option(type, type)).join('');
  if (!projectState.projects.some(p => p.id === projectFilter)) projectFilter = 'all';
  if (!projectState.projects.some(p => p.type === projectTypeFilter)) projectTypeFilter = 'all';
  (document.querySelector('#project-filter') as HTMLSelectElement).value = projectFilter;
  (document.querySelector('#project-type-filter') as HTMLSelectElement).value = projectTypeFilter;
  document.querySelector('#project-list')!.innerHTML = projectState.projects.map(p => `<div class="project-row"><span>${escapeHtml(p.name)} · ${escapeHtml(p.type)} · ${p.archived ? 'Project Archive' : 'Project'}</span><button data-project="${escapeHtml(p.id)}" data-operation="archive">${p.archived ? '復元' : 'アーカイブ'}</button><button data-project="${escapeHtml(p.id)}" data-operation="delete">削除</button></div>`).join('') || '<p>Project はまだありません。</p>';
}

let assignmentSound: Sound | undefined;
function bindProjects() {
  refreshProjectControls();
  const dialog = document.querySelector<HTMLDialogElement>('#project-dialog')!;
  document.querySelector('#manage-projects')!.addEventListener('click', () => dialog.showModal());
  document.querySelector('#close-projects')!.addEventListener('click', () => dialog.close());
  for (const id of ['project-view', 'project-filter', 'project-type-filter']) {
    document.querySelector(`#${id}`)!.addEventListener('change', event => {
      const value = (event.target as HTMLSelectElement).value;
      if (id === 'project-view') projectView = value;
      else if (id === 'project-filter') projectFilter = value;
      else projectTypeFilter = value;
      renderCards();
    });
  }
  document.querySelector('#project-form')!.addEventListener('submit', event => {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const fields = new FormData(form);
    const name = String(fields.get('name')).trim(), type = String(fields.get('type')).trim();
    if (!name || !type) return;
    if (projectState.projects.some(p => p.name === name && p.type === type)) { notify('同じ Project が登録されています'); return; }
    projectState.projects.push({ id: crypto.randomUUID(), name, type, archived: false });
    persistProjects(); form.reset(); refreshProjectControls(); renderCards();
  });
  document.querySelector('#project-list')!.addEventListener('click', event => {
    const button = (event.target as HTMLElement).closest<HTMLButtonElement>('[data-project]');
    const project = projectState.projects.find(p => p.id === button?.dataset.project);
    if (!project || !button) return;
    if (button.dataset.operation === 'archive') project.archived = !project.archived;
    else {
      if (!confirm(`「${project.name}」を削除し、効果音との紐付けを解除します。音源ファイルは残ります。`)) return;
      for (const sound of sounds) projectState.assignments[sound.id] = projectsFor(sound).map(p => p.id).filter(id => id !== project.id);
      projectState.projects = projectState.projects.filter(p => p.id !== project.id);
      projectState.deleted.push(project.id);
    }
    persistProjects(); refreshProjectControls(); renderCards();
  });
  document.querySelector('#export-projects')!.addEventListener('click', () => {
    const data = { projects: projectState.projects, sounds: sounds.map(sound => ({ ...sound, projectIds: projectsFor(sound).map(p => p.id) })) };
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a'); link.href = url; link.download = 'soundvault-projects.json'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  document.querySelector('#close-assignment')!.addEventListener('click', () => document.querySelector<HTMLDialogElement>('#assignment-dialog')!.close());
  document.querySelector('#assignment-form')!.addEventListener('submit', event => {
    event.preventDefault();
    if (assignmentSound) projectState.assignments[assignmentSound.id] = new FormData(event.target as HTMLFormElement).getAll('project').map(String);
    persistProjects(); document.querySelector<HTMLDialogElement>('#assignment-dialog')!.close(); renderCards();
  });
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
    const projects = projectsFor(sound);
    if (projectView === 'unassigned' && projects.length) return false;
    if (projectView !== 'unassigned' && (projectView !== 'all' || projectFilter !== 'all' || projectTypeFilter !== 'all') && !projects.some(p => (projectView === 'all' || (projectView === 'archive' ? p.archived : !p.archived)) && (projectFilter === 'all' || p.id === projectFilter) && (projectTypeFilter === 'all' || p.type === projectTypeFilter))) return false;
    const haystack = [sound.name, sound.category, ...sound.tags, sound.author, sound.license, ...projects.flatMap(p => [p.name, p.type])].join(' ').toLowerCase();
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
    <div class="project-badges">${projectsFor(sound).map(p => `<span>${escapeHtml(p.name)} · ${escapeHtml(p.type)}${p.archived ? ' · Project Archive' : ''}</span>`).join('')}<button data-action="assign-project">Project を設定</button></div>
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
  if (action === 'assign-project') {
    assignmentSound = sound;
    const selected = projectsFor(sound).map(p => p.id);
    document.querySelector('#assignment-options')!.innerHTML = projectState.projects.map(p => `<label><input type="checkbox" name="project" value="${escapeHtml(p.id)}" ${selected.includes(p.id) ? 'checked' : ''}> ${escapeHtml(p.name)} · ${escapeHtml(p.type)}${p.archived ? ' (Archive)' : ''}</label>`).join('') || '<p>先に Project 管理で Project を追加してください。</p>';
    document.querySelector<HTMLDialogElement>('#assignment-dialog')!.showModal(); return;
  }
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

async function init() {
  renderShell();
  try {
    const response = await fetch(`${baseUrl}data/sounds.json`);
    if (!response.ok) throw new Error('Index unavailable');
    sounds = await response.json() as Sound[];
    try {
      const projectsResponse = await fetch(`${baseUrl}data/projects.json`);
      if (projectsResponse.ok) {
        const shared = await projectsResponse.json() as Project[];
        for (const project of shared) if (!projectState.deleted.includes(project.id) && !projectState.projects.some(p => p.id === project.id)) projectState.projects.push(project);
      }
    } catch { /* Projects are optional for existing libraries. */ }
    refreshProjectControls(); renderCards();
  } catch { notify('Could not load sounds.json'); }
}
init();
