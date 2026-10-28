import type { Company } from '../types';
import { lev } from './levenshtein';

export const nz = (s: string): string => s.toLowerCase().replace(/[^a-z0-9 ]/g, '').trim();

export interface ResolveResult {
  results: Company[];
  fuzzy: boolean;
}

export function resolveCompany(query: string, directory: Company[]): ResolveResult {
  const q = nz(query);
  if (!q) {
    return { results: [], fuzzy: false };
  }

  const out = directory
    .map((c) => {
      const n = nz(c.name);
      const t = c.ticker.toLowerCase();
      const w = n.split(' ');
      let s = 0;
      if (t === q || t.split('.')[0] === q) s = 100;
      else if (n.startsWith(q)) s = 90;
      else if (t.startsWith(q)) s = 80;
      else if (w.some((x) => x.startsWith(q))) s = 70;
      else if (n.includes(q)) s = 50;
      return { c, s };
    })
    .filter((x) => x.s > 0)
    .sort((a, b) => b.s - a.s);

  if (out.length > 0) {
    return { results: out.map((x) => x.c).slice(0, 6), fuzzy: false };
  }

  if (q.length < 3) {
    return { results: [], fuzzy: false };
  }

  const tol = q.length >= 5 ? 2 : 1;

  const f = directory
    .map((c) => {
      const ws = nz(c.name).split(' ').filter((x) => x.length > 1);
      const minDistance = Math.min(
        ...ws.map((w) => Math.min(lev(q, w), lev(q, w.slice(0, q.length)))),
        q.length >= 4 ? lev(q, c.ticker.toLowerCase()) : 9
      );
      return { c, d: minDistance };
    })
    .filter((x) => x.d <= tol)
    .sort((a, b) => a.d - b.d);

  return { results: f.map((x) => x.c).slice(0, 4), fuzzy: true };
}
