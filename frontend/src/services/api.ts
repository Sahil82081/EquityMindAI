import type {
  Company,
  FinancialData,
  ResearchReport,
  DebateResult,
  Claim,
  ReliabilityScore,
  NewsResearchResult,
  ValuationAnalysis,
} from '../types';

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
}

export interface CompanySearchApiResponse {
  query: string;
  results: Company[];
  fuzzy: boolean;
  ambiguous?: boolean;
  count: number;
  match?: Company | null;
}

export interface ResearchApiResponse {
  research_id: string;
  company: Company;
  status: string;
  created_at: string;
  report?: ResearchReport;
  debate?: DebateResult;
  claims?: Claim[];
  reliability_score?: ReliabilityScore;
  financial_data?: FinancialData;
  news?: NewsResearchResult;
  valuation?: ValuationAnalysis;
  agent_status?: Record<string, string>;
  errors?: string[];
}

export interface CopilotApiResponse {
  research_id?: string;
  question: string;
  answer: string;
  ticker?: string;
  sources_cited?: string[];
  is_grounded?: boolean;
  sample?: boolean;
}

/**
 * Generic helper for API fetch requests with JSON payload handling.
 */
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `API error ${response.status} from ${endpoint}: ${errorText || response.statusText}`
    );
  }

  return response.json() as Promise<T>;
}

/**
 * Health check endpoint: GET /api/v1/health
 */
export async function checkHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>('/health');
}

/**
 * Search companies endpoint: GET /api/v1/company/search?q=
 */
export async function searchCompaniesApi(query: string): Promise<CompanySearchApiResponse> {
  const params = new URLSearchParams({ q: query });
  return apiFetch<CompanySearchApiResponse>(`/company/search?${params.toString()}`);
}

/**
 * Start research endpoint: POST /api/v1/research
 */
export async function startResearchApi(company: Company): Promise<ResearchApiResponse> {
  return apiFetch<ResearchApiResponse>('/research', {
    method: 'POST',
    body: JSON.stringify({ company }),
  });
}

/**
 * Get research by ID endpoint: GET /api/v1/research/{research_id}
 */
export async function getResearchApi(researchId: string): Promise<ResearchApiResponse> {
  return apiFetch<ResearchApiResponse>(`/research/${encodeURIComponent(researchId)}`);
}

/**
 * Copilot query endpoint: POST /api/v1/copilot
 */
export async function askCopilotApi(
  question: string,
  ticker?: string,
  researchId?: string,
  context?: string
): Promise<CopilotApiResponse> {
  return apiFetch<CopilotApiResponse>('/copilot', {
    method: 'POST',
    body: JSON.stringify({ question, ticker, research_id: researchId, context }),
  });
}
