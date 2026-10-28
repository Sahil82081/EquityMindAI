import React from 'react';
import type { Company } from '../types';

interface SelectedCompanyProps {
  company: Company | null;
  onChangeCompany: () => void;
  onStartResearch: (company: Company) => void;
}

export const SelectedCompany: React.FC<SelectedCompanyProps> = ({
  company,
  onChangeCompany,
  onStartResearch,
}) => {
  if (!company) return null;

  return (
    <div id="sel" className="selc">
      <div>
        <b className="serif" style={{ fontSize: '19px' }}>
          {company.name}
        </b>
        <div className="mut sm">
          {company.ticker} · {company.exchange} · {company.market} · {company.sector}
        </div>
      </div>
      <div className="sa">
        <button type="button" className="btn sm" id="chg" onClick={onChangeCompany}>
          Change company
        </button>
        <button
          type="button"
          className="btn pri"
          id="go"
          autoFocus
          onClick={() => onStartResearch(company)}
        >
          Start AI research →
        </button>
      </div>
    </div>
  );
};
