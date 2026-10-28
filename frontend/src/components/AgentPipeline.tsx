import React from 'react';
import { AGENTS } from '../services/mockData';
import type { AgentStatusCode } from '../types';

interface AgentPipelineProps {
  agentStatuses: Record<number, AgentStatusCode>;
  animationDuration?: number;
}

export const AgentPipeline: React.FC<AgentPipelineProps> = ({
  agentStatuses,
  animationDuration = 850,
}) => {
  return (
    <div className="card">
      <h3 style={{ marginBottom: '4px' }}>Agent pipeline</h3>
      <ol className="pl" id="pl" aria-label="Agent pipeline">
        {AGENTS.map((agent, index) => {
          const status = agentStatuses[index] || 'idle';
          const statusClass = status !== 'idle' ? `ag ${status}` : 'ag';

          return (
            <li key={agent.name} className={statusClass} id={`ag${index}`}>
              <div className="dot">{agent.icon}</div>
              <div>
                <b>{agent.name}</b>
                <span className="d">{agent.description}</span>
                <div className="bar">
                  <i style={{ '--t': `${animationDuration}ms` } as React.CSSProperties} />
                </div>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
};
