import React from 'react';
import type { Company, FinancialData, SimulationStage } from '../types';

interface WorkspaceHeaderProps {
  company: Company | null;
  stage: SimulationStage;
  financialData?: FinancialData | null;
  onNewTicker: () => void;
}

export const WorkspaceHeader: React.FC<WorkspaceHeaderProps> = ({
  company,
  stage,
  financialData,
  onNewTicker,
}) => {
  const isResearching = stage === 'loading';

  const isIndian =
    company?.ticker?.endsWith('.NS') ||
    company?.ticker?.endsWith('.BO') ||
    company?.exchange === 'NSE' ||
    company?.exchange === 'BSE' ||
    company?.market?.toLowerCase() === 'india' ||
    financialData?.quote?.currency === 'INR';

  let displayPrice = financialData?.quote?.formatted_price;
  if (displayPrice) {
    if (isIndian && displayPrice.includes('$')) {
      displayPrice = displayPrice.replace(/\$/g, '₹');
    }
  } else {
    displayPrice = isIndian ? '₹2,460.00' : '$228.40';
  }

  const displayChange = financialData?.quote?.formatted_change || '+2.41%';
  const isDown = financialData?.quote?.change_direction === 'down';
  const changeBadgeClass = isDown ? 'badge b-bad' : 'badge b-ok';

  return (
    <header className="top">
      <div className="wrap">
        <div>
          <div className="nm" id="hn">
            {company?.name || '–'}
          </div>
          <div className="mut sm">
            <span id="ht">
              {company ? `${company.ticker} · ${company.exchange}` : ''}
            </span>
          </div>
        </div>

        <div className="px" id="hp">
          {displayPrice}
        </div>
        <span className={changeBadgeClass} id="hc">
          {displayChange}
        </span>
        <span className="mut sm" id="hu">
          Updated 3 min ago
        </span>
        <span className="sp" />

        {isResearching ? (
          <span className="badge b-n" id="hs">
            Researching
          </span>
        ) : (
          <span className="badge b-warn" id="hs">
            ⚠ Needs review
          </span>
        )}

        <button className="btn sm" id="nw" onClick={onNewTicker}>
          New ticker
        </button>
      </div>
    </header>
  );
};
