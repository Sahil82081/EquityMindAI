import React from 'react';
import type { DebateResult } from '../types';
import { SAMPLE_DEBATE } from '../services/mockData';

interface DebateTabProps {
  debate?: DebateResult | null;
}

export const DebateTab: React.FC<DebateTabProps> = ({ debate: liveDebate }) => {
  const activeDebate = liveDebate || SAMPLE_DEBATE;
  const bull = activeDebate.bull;
  const bear = activeDebate.bear;
  const judgeConclusion =
    activeDebate.judgeConclusion ||
    activeDebate.judge_conclusion ||
    SAMPLE_DEBATE.judgeConclusion;

  const bullMetrics = bull.keyMetrics || bull.key_metrics || 'Rev verified, operating margin supported';
  const bearMetrics = bear.keyMetrics || bear.key_metrics || 'Valuation multiple verified';

  return (
    <div className="pane on" id="p-debate" role="tabpanel">
      <div className="deb">
        <div className="side bu">
          <h3>
            🐂 Bull case
            <span className="badge b-ok">{bull.confidence}% confidence</span>
          </h3>
          <div className="conf">
            <i style={{ width: `${bull.confidence}%`, background: 'var(--bull)' }} />
          </div>
          {bull.arguments.map((arg, idx) => (
            <div className="arg" key={idx}>
              <b>{arg.title}</b>
              <p>{arg.description}</p>
              <div className="ev">{arg.source}</div>
            </div>
          ))}
          <p className="sm mut" style={{ marginTop: '8px' }}>
            Key metrics: {bullMetrics}
          </p>
        </div>

        <div className="side be">
          <h3>
            🐻 Bear case
            <span className="badge b-bad">{bear.confidence}% confidence</span>
          </h3>
          <div className="conf">
            <i style={{ width: `${bear.confidence}%`, background: 'var(--bear)' }} />
          </div>
          {bear.arguments.map((arg, idx) => (
            <div className="arg" key={idx}>
              <b>{arg.title}</b>
              <p>{arg.description}</p>
              <div className="ev">{arg.source}</div>
            </div>
          ))}
          <p className="sm mut" style={{ marginTop: '8px' }}>
            Key metrics: {bearMetrics}
          </p>
        </div>
      </div>

      <div className="card judge">
        <h3>Judge’s conclusion</h3>
        <p>{judgeConclusion}</p>
      </div>
    </div>
  );
};
