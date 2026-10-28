export interface Company {
  name: string;
  ticker: string;
  exchange: string;
  market: string;
  sector?: string;
}

export type AgentStatusCode = 'idle' | 'run' | 'done' | 'rev';

export interface Agent {
  name: string;
  description: string;
  icon: string;
  status?: AgentStatusCode;
}

export type SimulationStage = 'idle' | 'loading' | 'completed';
export type ResearchStage = SimulationStage;

export type WorkspaceTabId = 'report' | 'debate' | 'claims' | 'data';

export interface ResearchState {
  stage: ResearchStage;
  selectedCompany: Company | null;
  activeStepIndex: number;
  agentStatuses: Record<number, AgentStatusCode>;
  stepStatuses: Record<number, 'idle' | 'run' | 'done'>;
  activeTab: WorkspaceTabId;
}

export type ClaimVerificationStatus =
  | 'ok'
  | 'warn'
  | 'bad'
  | 'Verified'
  | 'Partially Verified'
  | 'Unsupported';

export interface Evidence {
  source_data: string;
  calculation: string;
  retrieved_values?: Record<string, unknown>;
  formula?: string | null;
}

export interface VerificationResult {
  status: 'Verified' | 'Partially Verified' | 'Unsupported';
  status_code?: string;
  result_text: string;
  confidence_score?: number;
  discrepancy_explanation?: string | null;
}

export interface ClaimProof {
  label: string;
  detail: string;
}

export interface Claim {
  id?: string;
  statement: string;
  status: ClaimVerificationStatus | string;
  verification_status?: 'Verified' | 'Partially Verified' | 'Unsupported';
  evidence?: Evidence;
  verification_result?: VerificationResult;
  proofs: ClaimProof[];
  result: string;
}

export interface ReliabilityMetrics {
  evidence_quality: number;
  claim_verification: number;
  source_coverage: number;
  agent_agreement: number;
}

export interface MetricBreakdown {
  name: string;
  score: number;
  description: string;
}

export interface ReliabilityScore {
  score?: number;
  overall_score?: number;
  overallScore?: number;
  metrics: ReliabilityMetrics | MetricBreakdown[];
  breakdown?: MetricBreakdown[];
}

export interface SnapshotMetric {
  label: string;
  value: string;
}

export interface RevenueYearItem {
  year: number;
  amount: number;
  formatted_amount?: string;
}

export interface PriceQuote {
  current_price?: number;
  previous_close?: number;
  price_change?: number;
  price_change_percent?: number;
  currency: string;
  formatted_price: string;
  formatted_change: string;
  change_direction: 'up' | 'down' | 'neutral';
}

export interface FundamentalMetrics {
  market_cap?: number;
  formatted_market_cap: string;
  revenue?: number;
  formatted_revenue: string;
  net_income?: number;
  formatted_net_income: string;
  eps?: number;
  formatted_eps: string;
  pe_ratio?: number;
  formatted_pe: string;
  operating_margin?: number;
  formatted_operating_margin: string;
  net_margin?: number;
  formatted_net_margin: string;
  revenue_growth?: number;
  formatted_revenue_growth: string;
}

export interface FinancialData {
  ticker: string;
  quote: PriceQuote;
  fundamentals: FundamentalMetrics;
  snapshot: SnapshotMetric[];
  revenue_history: RevenueYearItem[];
  price_points: number[];
  historical_dates: string[];
  is_live?: boolean;
  error_message?: string | null;
}

export interface ResearchThesis {
  sentimentBadge?: string;
  sentimentClass?: 'b-ok' | 'b-warn' | 'b-bad' | 'b-n';
  sentiment_badge?: string;
  sentiment_class?: 'b-ok' | 'b-warn' | 'b-bad' | 'b-n';
  summary: string;
}

export interface ResearchReport {
  thesis: ResearchThesis;
  keyStrengths?: string[];
  key_strengths?: string[];
  keyRisks?: string[];
  key_risks?: string[];
  financialSnapshot?: SnapshotMetric[];
  financial_snapshot?: SnapshotMetric[];
  conclusion: string;
}

export interface DebatePoint {
  title: string;
  description: string;
  source: string;
}

export interface DebateSide {
  confidence: number;
  arguments: DebatePoint[];
  keyMetrics?: string;
  key_metrics?: string;
}

export interface DebateResult {
  bull: DebateSide;
  bear: DebateSide;
  judgeConclusion?: string;
  judge_conclusion?: string;
}

export interface CopilotQAItem {
  question: string;
  answer: string;
}

export interface NewsArticle {
  headline: string;
  source: string;
  published_at: string;
  url: string;
  summary: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  sentiment_score?: number;
}

export interface NewsResearchResult {
  ticker: string;
  company_name: string;
  articles: NewsArticle[];
  overall_sentiment: string;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  total_articles: number;
  source_coverage?: string;
}

export interface ValuationMetric {
  metric_name: string;
  value?: number;
  formatted_value: string;
  benchmark?: string;
  assessment: string;
  calculation_formula: string;
  explanation: string;
}

export interface HistoricalValuationComparison {
  metric: string;
  current_value: string;
  historical_benchmark: string;
  variance_percent?: number;
  historical_context: string;
  comparison_summary: string;
}

export interface ValuationAnalysis {
  ticker: string;
  company_name: string;
  pe_ratio: ValuationMetric;
  forward_pe?: ValuationMetric;
  revenue_growth: ValuationMetric;
  operating_margin: ValuationMetric;
  net_margin: ValuationMetric;
  historical_comparison: HistoricalValuationComparison;
  valuation_score: number;
  valuation_classification: string;
  executive_explanation: string;
  calculations_summary: string[];
}

export interface ResearchResponseData {
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
