export type Project = { id: string; name: string; type: string; archived: boolean };
export type ProjectState = { projects: Project[]; assignments: Record<string, string[]>; deleted: string[] };
const key = 'soundvault:projects:v1';
export function loadProjects(): ProjectState {
  try {
    const value = JSON.parse(localStorage.getItem(key) ?? 'null');
    if (value && Array.isArray(value.projects) && value.assignments && Array.isArray(value.deleted)) return value;
  } catch { /* Keep the library available when local storage is unavailable. */ }
  return { projects: [], assignments: {}, deleted: [] };
}
export function saveProjects(state: ProjectState) { localStorage.setItem(key, JSON.stringify(state)); }
