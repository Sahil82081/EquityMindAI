import React, { useState, useEffect, useRef } from 'react';
import type { Company, ResearchResponseData, SimulationStage, WorkspaceTabId } from '../types';
import { RESEARCH_STEPS } from '../services/mockData';
import { WorkspaceHeader } from '../components/WorkspaceHeader';
import { AgentPipeline } from '../components/AgentPipeline';
import { ReliabilityScore } from '../components/ReliabilityScore';
import { ReportTab } from '../components/ReportTab';
import { DebateTab } from '../components/DebateTab';
import { ClaimsTab } from '../components/ClaimsTab';
import { DataTab } from '../components/DataTab';
import { ResearchCopilot } from '../components/ResearchCopilot';

interface ResearchWorkspaceProps {
  company: Company | null;
  stage: SimulationStage;
  agentStatuses: Record<number, 'idle' | 'run' | 'done' | 'rev'>;
  stepStatuses: Record<number, 'idle' | 'run' | 'done'>;
  researchData?: ResearchResponseData | null;
  onNewTicker: () => void;
}

const TABS: { id: WorkspaceTabId; label: string }[] = [
  { id: 'report', label: 'Report' },
  { id: 'debate', label: 'Bull vs Bear' },
  { id: 'claims', label: 'Claims (4)' },
  { id: 'data', label: 'Data' },
];

export const ResearchWorkspace: React.FC<ResearchWorkspaceProps> = ({
  company,
  stage,
  agentStatuses,
  stepStatuses,
  researchData,
  onNewTicker,
}) => {
  const [activeTab, setActiveTab] = useState<WorkspaceTabId>('report');
  const tabsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // When completed, ensure top scroll position
    if (stage === 'completed') {
      window.scrollTo(0, 0);
    }
  }, [stage]);

  const handleTabKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    const currentIndex = TABS.findIndex((t) => t.id === activeTab);
    if (currentIndex === -1) return;

    if (e.key === 'ArrowRight') {
      e.preventDefault();
      const nextIndex = (currentIndex + 1) % TABS.length;
      setActiveTab(TABS[nextIndex].id);
      const nextBtn = tabsRef.current?.querySelector<HTMLButtonElement>(`#tb-${TABS[nextIndex].id}`);
      nextBtn?.focus();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      const prevIndex = (currentIndex - 1 + TABS.length) % TABS.length;
      setActiveTab(TABS[prevIndex].id);
      const prevBtn = tabsRef.current?.querySelector<HTMLButtonElement>(`#tb-${TABS[prevIndex].id}`);
      prevBtn?.focus();
    }
  };

  const ticker = company?.ticker || 'AAPL';
  const financialData = researchData?.financial_data;

  return (
    <section id="ws">
      <WorkspaceHeader
        company={company}
        stage={stage}
        financialData={financialData}
        onNewTicker={onNewTicker}
      />

      <div className="wrap">
        {stage === 'loading' && (
          <div id="loading" style={{ display: 'block' }}>
            <h2 id="lt">EquityMind is researching {ticker}…</h2>
            <div id="ll">
              {RESEARCH_STEPS.map((stepName, idx) => {
                const s = stepStatuses[idx] || 'idle';
                const icon = s === 'done' ? '✓' : s === 'run' ? '◐' : '○';
                const statusClass = s !== 'idle' ? `ls ${s}` : 'ls';

                return (
                  <div key={idx} className={statusClass} id={`ls${idx}`}>
                    <span>{icon}</span>
                    {stepName}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {stage === 'completed' && (
          <div className="grid" id="main">
            <aside className="rail">
              <AgentPipeline agentStatuses={agentStatuses} />
              <ReliabilityScore reliabilityScore={researchData?.reliability_score} />
            </aside>

            <main>
              <div
                className="tabs"
                role="tablist"
                id="tabs"
                ref={tabsRef}
                onKeyDown={handleTabKeyDown}
              >
                {TABS.map((tab) => {
                  const isSelected = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      className="tab"
                      role="tab"
                      id={`tb-${tab.id}`}
                      aria-selected={isSelected}
                      data-t={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      type="button"
                    >
                      {tab.label}
                    </button>
                  );
                })}
              </div>

              {activeTab === 'report' && (
                <ReportTab
                  company={company}
                  report={researchData?.report}
                  financialData={financialData}
                />
              )}
              {activeTab === 'debate' && <DebateTab debate={researchData?.debate} />}
              {activeTab === 'claims' && <ClaimsTab claims={researchData?.claims} />}
              {activeTab === 'data' && <DataTab financialData={financialData} />}

              <ResearchCopilot
                ticker={company?.ticker}
                researchId={researchData?.research_id}
              />
            </main>
          </div>
        )}
      </div>
    </section>
  );
};
