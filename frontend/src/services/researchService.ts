import { startResearchApi, getResearchApi, type ResearchApiResponse } from './api';
import type { Company } from '../types';

export async function initiateResearch(company: Company): Promise<ResearchApiResponse | null> {
  try {
    return await startResearchApi(company);
  } catch (error) {
    console.warn('Backend unavailable, proceeding with local simulation fallback:', error);
    return null;
  }
}

export async function fetchResearchStatus(researchId: string): Promise<ResearchApiResponse | null> {
  try {
    return await getResearchApi(researchId);
  } catch (error) {
    console.warn(`Failed to fetch research with id '${researchId}':`, error);
    return null;
  }
}
