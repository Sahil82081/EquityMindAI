import type { Company } from '../types';
import { COMPANIES } from './mockData';
import { resolveCompany } from '../utils/searchResolver';
import { searchCompaniesApi } from './api';

const RECENT_KEY = 'em_recent';

export interface CompanyResolveResult {
  results: Company[];
  fuzzy: boolean;
  ambiguous?: boolean;
  match?: Company | null;
}

export function getRecentSearches(): Company[] {
  try {
    const raw = localStorage.getItem(RECENT_KEY);
    return raw ? (JSON.parse(raw) as Company[]) : [];
  } catch {
    return [];
  }
}

export function saveRecentSearch(company: Company): void {
  try {
    const current = getRecentSearches();
    const filtered = current.filter((item) => item.ticker !== company.ticker);
    const updated = [company, ...filtered].slice(0, 3);
    localStorage.setItem(RECENT_KEY, JSON.stringify(updated));
  } catch {
    // Ignore storage quota / privacy exceptions
  }
}

/**
 * Perform company search and resolution via FastAPI backend, with graceful local fallback if offline.
 */
export async function searchCompanies(query: string): Promise<CompanyResolveResult> {
  try {
    const apiResult = await searchCompaniesApi(query);
    return {
      results: apiResult.results,
      fuzzy: apiResult.fuzzy,
      ambiguous: apiResult.ambiguous,
      match: apiResult.match,
    };
  } catch {
    // Graceful fallback to deterministic client resolver if backend is unavailable
    const local = resolveCompany(query, COMPANIES);
    return {
      results: local.results,
      fuzzy: local.fuzzy,
      ambiguous: local.results.length > 1,
      match: local.results[0] || null,
    };
  }
}
