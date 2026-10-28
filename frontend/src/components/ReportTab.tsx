import React from 'react';
import type { Company, FinancialData, ResearchReport } from '../types';
import { getSampleReport } from '../services/mockData';

interface ReportTabProps {
  company: Company | null;
  report?: ResearchReport | null;
  financialData?: FinancialData | null;
}

export const ReportTab: React.FC<ReportTabProps> = ({
  company,
  report: liveReport,
  financialData,
}) => {
  const currentCompany = company || {
    name: 'Apple Inc.',
    ticker: 'AAPL',
    exchange: 'NASDAQ',
    market: 'US',
    sector: 'Technology',
  };

  const defaultReport = getSampleReport(currentCompany);
  const activeReport = liveReport || defaultReport;

  const sentimentBadge =
    activeReport.thesis.sentimentBadge ||
    activeReport.thesis.sentiment_badge ||
    'Neutral, leaning bullish';
  const sentimentClass =
    activeReport.thesis.sentimentClass ||
    activeReport.thesis.sentiment_class ||
    'b-warn';
  const summary = activeReport.thesis.summary || defaultReport.thesis.summary;

  const strengths =
    activeReport.keyStrengths ||
    activeReport.key_strengths ||
    defaultReport.keyStrengths ||
    [];
  const risks =
    activeReport.keyRisks ||
    activeReport.key_risks ||
    defaultReport.keyRisks ||
    [];

  const snapshotItems =
    financialData?.snapshot ||
    activeReport.financialSnapshot ||
    activeReport.financial_snapshot ||
    defaultReport.financialSnapshot ||
    [];

  const conclusion = activeReport.conclusion || defaultReport.conclusion;

  return (
    <div className="pane on" id="p-report" role="tabpanel">
      <div className="card">
        <div className="thesis">
          <h3 style={{ margin: 0 }}>Investment thesis</h3>
          <span className={`badge ${sentimentClass}`}>
            {sentimentBadge}
          </span>
        </div>
        <p>{summary}</p>
      </div>

      <div className="two">
        <div className="card">
          <h3>Key strengths</h3>
          <ul className="l">
            {strengths.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>Key risks</h3>
          <ul className="l">
            {risks.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card">
        <h3>Financial snapshot</h3>
        <div className="snap">
          {snapshotItems.map((item) => (
            <div key={item.label}>
              <small>{item.label}</small>
              <b>{item.value}</b>
            </div>
          ))}
        </div>
      </div>

      <details className="card" open>
        <summary style={{ cursor: 'pointer', listStyle: 'none' }}>
          <h3 style={{ display: 'inline' }}>Final conclusion</h3>
        </summary>
        <div style={{ marginTop: '8px' }}>
          <p>{conclusion}</p>
        </div>
      </details>
    </div>
  );
};
