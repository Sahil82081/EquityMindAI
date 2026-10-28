import { useState, useRef, useCallback, useEffect } from 'react';
import type { AgentStatusCode, Company, ResearchResponseData, SimulationStage } from '../types';
import { PIPELINE_SEQUENCE } from '../services/mockData';

export function useResearchSimulation(
  _company: Company | null,
  researchData?: ResearchResponseData | null
) {
  const [stage, setStage] = useState<SimulationStage>('idle');
  const [agentStatuses, setAgentStatuses] = useState<Record<number, AgentStatusCode>>({
    0: 'idle',
    1: 'idle',
    2: 'idle',
    3: 'idle',
    4: 'idle',
    5: 'idle',
    6: 'idle',
  });
  const [stepStatuses, setStepStatuses] = useState<Record<number, 'idle' | 'run' | 'done'>>({
    0: 'idle',
    1: 'idle',
    2: 'idle',
    3: 'idle',
    4: 'idle',
    5: 'idle',
  });

  const timersRef = useRef<number[]>([]);

  const clearAllTimers = useCallback(() => {
    timersRef.current.forEach((id) => clearTimeout(id));
    timersRef.current = [];
  }, []);

  useEffect(() => {
    return () => {
      clearAllTimers();
    };
  }, [clearAllTimers]);

  // Synchronize with actual backend LangGraph execution progress when available
  useEffect(() => {
    if (!researchData?.agent_status) return;
    const { data, news, valuation, bull, bear, judge, verification } = researchData.agent_status;
    queueMicrotask(() => {
      setAgentStatuses((prev) => ({
        ...prev,
        0: data === 'completed' ? 'done' : data === 'running' ? 'run' : prev[0],
        1: news === 'completed' ? 'done' : news === 'running' ? 'run' : prev[1],
        2: valuation === 'completed' ? 'done' : valuation === 'running' ? 'run' : prev[2],
        3: bull === 'completed' ? 'done' : bull === 'running' ? 'run' : prev[3],
        4: bear === 'completed' ? 'done' : bear === 'running' ? 'run' : prev[4],
        5: judge === 'completed' ? 'done' : judge === 'running' ? 'run' : prev[5],
        6: verification === 'completed' ? 'rev' : verification === 'running' ? 'run' : prev[6],
      }));
      setStepStatuses((prev) => ({
        ...prev,
        0: data === 'completed' ? 'done' : prev[0],
        1: news === 'completed' ? 'done' : prev[1],
        2: valuation === 'completed' ? 'done' : prev[2],
        3: bull === 'completed' && bear === 'completed' ? 'done' : prev[3],
        4: verification === 'completed' ? 'done' : prev[4],
        5: verification === 'completed' ? 'done' : prev[5],
      }));
    });
  }, [researchData]);

  const startSimulation = useCallback(() => {
    clearAllTimers();
    setStage('loading');

    // Reset statuses
    setAgentStatuses({
      0: 'idle',
      1: 'idle',
      2: 'idle',
      3: 'idle',
      4: 'idle',
      5: 'idle',
      6: 'idle',
    });
    setStepStatuses({
      0: 'idle',
      1: 'idle',
      2: 'idle',
      3: 'idle',
      4: 'idle',
      5: 'idle',
    });

    const prefersReducedMotion = typeof window !== 'undefined'
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
      : false;
    const dur = prefersReducedMotion ? 60 : 850;

    let t = 0;
    PIPELINE_SEQUENCE.forEach((group, stepIndex) => {
      // Step start
      const startId = window.setTimeout(() => {
        setAgentStatuses((prev) => {
          const next = { ...prev };
          group.forEach((agentIdx) => {
            next[agentIdx] = 'run';
          });
          return next;
        });
        setStepStatuses((prev) => ({
          ...prev,
          [stepIndex]: 'run',
        }));
      }, t);
      timersRef.current.push(startId);

      t += dur;

      // Step completion
      const finishId = window.setTimeout(() => {
        setAgentStatuses((prev) => {
          const next = { ...prev };
          group.forEach((agentIdx) => {
            next[agentIdx] = agentIdx === 6 ? 'rev' : 'done';
          });
          return next;
        });
        setStepStatuses((prev) => ({
          ...prev,
          [stepIndex]: 'done',
        }));
      }, t);
      timersRef.current.push(finishId);
    });

    const completionId = window.setTimeout(() => {
      setStage('completed');
    }, t + 250);
    timersRef.current.push(completionId);
  }, [clearAllTimers]);

  const resetSimulation = useCallback(() => {
    clearAllTimers();
    setStage('idle');
    setAgentStatuses({
      0: 'idle',
      1: 'idle',
      2: 'idle',
      3: 'idle',
      4: 'idle',
      5: 'idle',
      6: 'idle',
    });
    setStepStatuses({
      0: 'idle',
      1: 'idle',
      2: 'idle',
      3: 'idle',
      4: 'idle',
      5: 'idle',
    });
  }, [clearAllTimers]);

  return {
    stage,
    agentStatuses,
    stepStatuses,
    startSimulation,
    resetSimulation,
  };
}
