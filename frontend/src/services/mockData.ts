import type {
  Company,
  Agent,
  Claim,
  ReliabilityScore,
  ResearchReport,
  DebateResult,
  FinancialData,
  CopilotQAItem,
} from '../types';

export const COMPANIES: Company[] = [
  { name: 'Apple Inc.', ticker: 'AAPL', exchange: 'NASDAQ', market: 'US', sector: 'Technology' },
  { name: 'Apple Hospitality REIT, Inc.', ticker: 'APLE', exchange: 'NYSE', market: 'US', sector: 'Real Estate' },
  { name: 'Apple Rush Company', ticker: 'APRU', exchange: 'OTC', market: 'US', sector: 'Beverages' },
  { name: 'Microsoft Corporation', ticker: 'MSFT', exchange: 'NASDAQ', market: 'US', sector: 'Technology' },
  { name: 'NVIDIA Corporation', ticker: 'NVDA', exchange: 'NASDAQ', market: 'US', sector: 'Technology' },
  { name: 'Tesla, Inc.', ticker: 'TSLA', exchange: 'NASDAQ', market: 'US', sector: 'Automotive' },
  { name: 'Amazon.com, Inc.', ticker: 'AMZN', exchange: 'NASDAQ', market: 'US', sector: 'Consumer Cyclical' },
  { name: 'Alphabet Inc.', ticker: 'GOOGL', exchange: 'NASDAQ', market: 'US', sector: 'Communication Services' },
  { name: 'Meta Platforms, Inc.', ticker: 'META', exchange: 'NASDAQ', market: 'US', sector: 'Communication Services' },
  { name: 'Netflix, Inc.', ticker: 'NFLX', exchange: 'NASDAQ', market: 'US', sector: 'Communication Services' },
  { name: 'Advanced Micro Devices, Inc.', ticker: 'AMD', exchange: 'NASDAQ', market: 'US', sector: 'Technology' },
  { name: 'Taiwan Semiconductor Manufacturing', ticker: 'TSM', exchange: 'NYSE', market: 'Taiwan', sector: 'Technology' },
  { name: 'Toyota Motor Corporation', ticker: 'TM', exchange: 'NYSE', market: 'Japan', sector: 'Automotive' },
  { name: 'Tata Consultancy Services Limited', ticker: 'TCS.NS', exchange: 'NSE', market: 'India', sector: 'Technology' },
  { name: 'Infosys Limited', ticker: 'INFY', exchange: 'NYSE', market: 'India', sector: 'Technology' },
  { name: 'Reliance Industries Limited', ticker: 'RELIANCE.NS', exchange: 'NSE', market: 'India', sector: 'Energy & Conglomerate' },
  { name: 'HDFC Bank Limited', ticker: 'HDB', exchange: 'NYSE', market: 'India', sector: 'Financial Services' },
  { name: 'ICICI Bank Limited', ticker: 'IBN', exchange: 'NYSE', market: 'India', sector: 'Financial Services' },
  { name: 'Wipro Limited', ticker: 'WIT', exchange: 'NYSE', market: 'India', sector: 'Technology' },
  { name: 'Tata Motors Limited', ticker: 'TATAMOTORS.NS', exchange: 'NSE', market: 'India', sector: 'Automotive' },
  { name: 'State Bank of India', ticker: 'SBIN.NS', exchange: 'NSE', market: 'India', sector: 'Financial Services' },
  { name: 'Berkshire Hathaway Inc.', ticker: 'BRK-B', exchange: 'NYSE', market: 'US', sector: 'Financial Services' },
];

export const SUGGESTED_TICKERS: string[] = ['Apple', 'Microsoft', 'Nvidia', 'Tesla', 'TCS', 'Amazon', 'AAPL'];

export const AGENTS: Agent[] = [
  { name: 'Data', description: 'Pulls prices and financial statements', icon: '▤' },
  { name: 'News', description: 'Scores recent headlines and sentiment', icon: '☰' },
  { name: 'Valuation', description: 'Compares multiples with history and peers', icon: '◈' },
  { name: 'Bull', description: 'Argues why the company is attractive', icon: '▲' },
  { name: 'Bear', description: 'Argues why the thesis could fail', icon: '▼' },
  { name: 'Judge', description: 'Weighs both sides and concludes', icon: '⚖' },
  { name: 'Verification', description: 'Checks each claim against source data', icon: '✓' },
];

export const RESEARCH_STEPS: string[] = [
  'Financial data collected',
  'News analyzed',
  'Valuation analysis',
  'Bull/Bear debate',
  'Claim verification',
  'Reliability scoring',
];

export const PIPELINE_SEQUENCE: number[][] = [[0], [1], [2], [3, 4], [5], [6]];

export const SAMPLE_RELIABILITY_SCORE: ReliabilityScore = {
  overallScore: 84,
  metrics: [
    {
      name: 'Evidence Quality',
      score: 91,
      description: 'How directly the cited figures come from filings and structured data rather than inference.',
    },
    {
      name: 'Claim Verification',
      score: 88,
      description: 'Share of claims that were recomputed from source data and matched.',
    },
    {
      name: 'Source Coverage',
      score: 84,
      description: 'How many of the required data types (financials, news, valuation inputs) were available.',
    },
    {
      name: 'Agent Agreement',
      score: 75,
      description: 'How consistently independent research agents support the final thesis.',
    },
  ],
};

export const SAMPLE_CLAIMS: Claim[] = [
  {
    id: 'c1',
    statement: 'Revenue increased 12% year over year.',
    status: 'ok',
    proofs: [
      { label: 'Source data', detail: 'Previous revenue $100.0B · Current revenue $112.0B' },
      { label: 'Calculation', detail: '(112.0 − 100.0) ÷ 100.0 = 12.0%' },
    ],
    result: 'Matches reported figures.',
  },
  {
    id: 'c2',
    statement: 'Operating margin expanded by roughly 150 basis points.',
    status: 'ok',
    proofs: [
      { label: 'Source data', detail: 'Prior margin 28.4% · Current margin 29.9%' },
      { label: 'Calculation', detail: '29.9 − 28.4 = 1.5 pts' },
    ],
    result: 'Matches reported figures.',
  },
  {
    id: 'c3',
    statement: 'The stock trades at a premium to its 5-year average multiple.',
    status: 'warn',
    proofs: [
      { label: 'Source data', detail: 'Current P/E 31.2 · 5-year average 24.8 (derived from price history)' },
      { label: 'Calculation', detail: '31.2 ÷ 24.8 = 1.26×' },
    ],
    result: 'The premium is confirmed, but the 5-year average uses estimated historical EPS.',
  },
  {
    id: 'c4',
    statement: 'Management guidance implies accelerating growth next year.',
    status: 'bad',
    proofs: [
      { label: 'Source data', detail: 'No guidance figures found in the retrieved data' },
      { label: 'Calculation', detail: 'None available' },
    ],
    result: 'No supporting data was retrieved. Treat as unverified.',
  },
];

export const SAMPLE_DEBATE: DebateResult = {
  bull: {
    confidence: 72,
    keyMetrics: 'Rev +12%, margin 29.9%',
    arguments: [
      {
        title: 'Durable revenue growth',
        description: 'Revenue +12% YoY, ahead of the prior year',
        source: 'Source: income statement',
      },
      {
        title: 'Expanding margins',
        description: 'Operating margin up 1.5 pts',
        source: 'Source: income statement',
      },
      {
        title: 'Strong cash generation',
        description: 'Free cash flow supports buybacks',
        source: 'Source: cash-flow statement',
      },
    ],
  },
  bear: {
    confidence: 58,
    keyMetrics: 'P/E 31.2, avg 24.8',
    arguments: [
      {
        title: 'Premium valuation',
        description: 'P/E 31.2 vs 24.8 five-year average',
        source: 'Source: price and EPS history',
      },
      {
        title: 'Slowing unit demand',
        description: 'News sentiment mixed on near-term volume',
        source: 'Source: 14 recent headlines',
      },
      {
        title: 'Concentration risk',
        description: 'Growth depends on a few product lines',
        source: 'Source: segment disclosure',
      },
    ],
  },
  judgeConclusion:
    'The bull case wins on evidence: two of its three arguments are backed by verified claims, while the bear case rests on one verified multiple and one inference from headlines. The bear argument on valuation is still valid and sets the thesis to neutral-leaning-bullish rather than bullish.',
};

export const SAMPLE_FINANCIAL_DATA: FinancialData = {
  ticker: 'AAPL',
  quote: {
    current_price: 242.84,
    previous_close: 239.5,
    price_change: 3.34,
    price_change_percent: 1.39,
    currency: 'USD',
    formatted_price: '$242.84',
    formatted_change: '+1.39%',
    change_direction: 'up',
  },
  fundamentals: {
    market_cap: 3500000000000,
    formatted_market_cap: '$3.50T',
    revenue: 112000000000,
    formatted_revenue: '$112.0B',
    net_income: 26400000000,
    formatted_net_income: '$26.4B',
    eps: 7.32,
    formatted_eps: '$7.32',
    pe_ratio: 31.2,
    formatted_pe: '31.2',
    operating_margin: 0.299,
    formatted_operating_margin: '29.9%',
    net_margin: 0.236,
    formatted_net_margin: '23.6%',
    revenue_growth: 0.12,
    formatted_revenue_growth: '+12.0%',
  },
  snapshot: [
    { label: 'Revenue', value: '$112.0B' },
    { label: 'Net profit', value: '$26.4B' },
    { label: 'EPS', value: '$7.32' },
    { label: 'P/E', value: '31.2' },
    { label: 'Market cap', value: '$3.5T' },
    { label: 'Op. margin', value: '29.9%' },
    { label: 'Revenue growth', value: '+12.0%' },
    { label: 'Net margin', value: '23.6%' },
  ],
  revenue_history: [
    { year: 2021, amount: 78 },
    { year: 2022, amount: 86 },
    { year: 2023, amount: 100 },
    { year: 2024, amount: 112 },
  ],
  price_points: [],
  historical_dates: [],
  is_live: false,
};

export function getSampleReport(company: Company): ResearchReport {
  return {
    thesis: {
      sentimentBadge: 'Neutral, leaning bullish',
      sentimentClass: 'b-warn',
      summary: `Sample summary: ${company.ticker} shows steady revenue growth and rising margins, but its premium valuation leaves little room for a miss. The Judge found the bull case better supported by data, and the bear case stronger on price.`,
    },
    keyStrengths: [
      'Revenue up 12% year over year (verified)',
      'Operating margin up 1.5 pts (verified)',
      'Cash generation funds buybacks',
    ],
    keyRisks: [
      'P/E 26% above its 5-year average',
      'Mixed near-term demand sentiment',
      'Growth concentrated in few product lines',
    ],
    financialSnapshot: SAMPLE_FINANCIAL_DATA.snapshot,
    conclusion:
      'Attractive business at a full price. The research supports holding exposure while treating the guidance claim as unproven. This is research output, not investment advice.',
  };
}

export const COPILOT_QUESTIONS: CopilotQAItem[] = [
  {
    question: 'Why is the valuation expensive?',
    answer:
      'The stock trades at 31.2× earnings against a five-year average of 24.8×. Earnings growth of 12% does not fully close that gap, so returns depend on margins continuing to expand. Evidence: Claim 3 (partially verified).',
  },
  {
    question: 'What are the biggest risks?',
    answer:
      'Valuation leaves little room for a growth miss, news sentiment on near-term demand is mixed, and revenue depends on a few product lines. The Bear agent rated its own confidence at 58%.',
  },
  {
    question: 'Show me the evidence behind the bullish thesis.',
    answer:
      'Two of the three bull arguments rest on verified claims: revenue growth and margin expansion. The cash-flow argument has no linked claim yet, so it is weaker than it reads.',
  },
  {
    question: 'Challenge the current conclusion.',
    answer:
      'The neutral-to-bullish call assumes margins keep expanding. If they flatten, the premium multiple has no support. The unsupported guidance claim should be removed or sourced before relying on it.',
  },
  {
    question: 'What changed in the financials?',
    answer:
      'Revenue rose from $100.0B to $112.0B and operating margin from 28.4% to 29.9%. Valuation multiples also rose, so part of the price gain reflects re-rating rather than earnings.',
  },
  {
    question: 'Why did the reliability score decrease?',
    answer:
      'The Research Reliability Score evaluates Evidence Quality (30%), Claim Verification (30%), Source Coverage (20%), and Agent Agreement (20%). It isolates unverified assertions to protect analytical integrity.',
  },
];
