import React, { useState, useRef, useMemo, useEffect } from 'react';
import type { FinancialData, RevenueYearItem } from '../types';
import { SAMPLE_FINANCIAL_DATA } from '../services/mockData';

const W = 640;
const Hh = 240;
const P = 36;
const MONTHS = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'];

interface DataTabProps {
  financialData?: FinancialData | null;
}

export const DataTab: React.FC<DataTabProps> = ({ financialData }) => {
  const [tooltipState, setTooltipState] = useState<{
    visible: boolean;
    x: number;
    y: number;
    tipX: number;
    tipY: number;
    text: string;
  }>({
    visible: false,
    x: 0,
    y: 0,
    tipX: 0,
    tipY: 0,
    text: '',
  });

  const [barsAnimated, setBarsAnimated] = useState(false);
  const svgRef = useRef<SVGSVGElement>(null);

  // Use live price points from market data layer or fallback
  const priceData = useMemo(() => {
    if (financialData?.price_points && financialData.price_points.length >= 10) {
      return financialData.price_points;
    }
    const n = 60;
    let s = 7;
    let y = 170;
    const series: number[] = [];
    for (let i = 0; i < n; i++) {
      s = (s * 9301 + 49297) % 233280;
      y += (s / 233280 - 0.42) * 5;
      series.push(y);
    }
    return series;
  }, [financialData]);

  const nPoints = priceData.length;

  const { minVal, maxVal, pts, polygonPts, gridLines } = useMemo(() => {
    const mn = Math.min(...priceData);
    const mx = Math.max(...priceData);
    const range = mx - mn || 1;

    const getX = (i: number) => P + (i * (W - P - 8)) / (nPoints - 1);
    const getY = (v: number) => Hh - 24 - ((v - mn) / range) * (Hh - 50);

    const points = priceData
      .map((v, i) => `${getX(i).toFixed(1)},${getY(v).toFixed(1)}`)
      .join(' ');

    const poly = `${P},${Hh - 24} ${points} ${getX(nPoints - 1)},${Hh - 24}`;

    const lines = [0, 1, 2, 3].map((k) => {
      const v = mn + (range * k) / 3;
      return {
        y: getY(v),
        label: `$${v.toFixed(0)}`,
      };
    });

    return {
      minVal: mn,
      maxVal: mx,
      pts: points,
      polygonPts: poly,
      gridLines: lines,
    };
  }, [priceData, nPoints]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setBarsAnimated(true);
    }, 50);
    return () => clearTimeout(timer);
  }, []);

  const handlePointerMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    const xCoord = ((e.clientX - rect.left) / rect.width) * W;
    const i = Math.max(0, Math.min(nPoints - 1, Math.round(((xCoord - P) * (nPoints - 1)) / (W - P - 8))));

    const range = maxVal - minVal || 1;
    const getX = (index: number) => P + (index * (W - P - 8)) / (nPoints - 1);
    const getY = (v: number) => Hh - 24 - ((v - minVal) / range) * (Hh - 50);

    const pointX = getX(i);
    const pointY = getY(priceData[i]);

    let dateLabel = '';
    if (financialData?.historical_dates && financialData.historical_dates[i]) {
      dateLabel = financialData.historical_dates[i];
    } else {
      dateLabel = MONTHS[Math.floor((i / nPoints) * MONTHS.length)] || MONTHS[0];
    }

    const text = `${dateLabel} · $${priceData[i].toFixed(2)}`;

    setTooltipState({
      visible: true,
      x: pointX,
      y: pointY,
      tipX: (pointX / W) * rect.width,
      tipY: (pointY / Hh) * rect.height,
      text,
    });
  };

  const handlePointerLeave = () => {
    setTooltipState((prev) => ({ ...prev, visible: false }));
  };

  const revenueItems: RevenueYearItem[] = useMemo(() => {
    if (financialData?.revenue_history && financialData.revenue_history.length > 0) {
      return financialData.revenue_history;
    }
    return SAMPLE_FINANCIAL_DATA.revenue_history || [];
  }, [financialData]);

  const maxRevenue = useMemo(() => {
    const amounts = revenueItems.map((r: RevenueYearItem) => r.amount);
    return Math.max(...amounts, 100) * 1.08;
  }, [revenueItems]);

  return (
    <div className="pane on" id="p-data" role="tabpanel">
      <div className="card">
        <h3>Price history</h3>
        <p className="sm mut">
          {financialData?.is_live ? 'Verified market series, 12 months' : 'Sample series, 12 months'}
        </p>
        <div className="chart" id="ch">
          <svg
            ref={svgRef}
            viewBox={`0 0 ${W} ${Hh}`}
            role="img"
            aria-label="Price history line chart"
            onPointerMove={handlePointerMove}
            onPointerLeave={handlePointerLeave}
          >
            <defs>
              <linearGradient id="lg" x1="0" x2="1">
                <stop offset="0" stopColor="#06B6D4" />
                <stop offset=".55" stopColor="#8B5CF6" />
                <stop offset="1" stopColor="#EC4899" />
              </linearGradient>
              <linearGradient id="ag" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0" stopColor="#8B5CF6" stopOpacity=".32" />
                <stop offset="1" stopColor="#8B5CF6" stopOpacity="0" />
              </linearGradient>
            </defs>

            {gridLines.map((line, idx) => (
              <g key={idx}>
                <line
                  x1={P}
                  x2={W}
                  y1={line.y}
                  y2={line.y}
                  stroke="var(--line)"
                />
                <text
                  x={P - 6}
                  y={line.y + 4}
                  textAnchor="end"
                  fontSize="11"
                  fill="var(--mut)"
                >
                  {line.label}
                </text>
              </g>
            ))}

            <polygon points={polygonPts} fill="url(#ag)" />
            <polyline
              className="draw"
              points={pts}
              fill="none"
              stroke="url(#lg)"
              strokeWidth="2.5"
              strokeLinejoin="round"
            />

            {tooltipState.visible && (
              <>
                <line
                  id="cx"
                  x1={tooltipState.x}
                  x2={tooltipState.x}
                  y1={10}
                  y2={Hh - 24}
                  stroke="var(--mut)"
                  strokeDasharray="3 3"
                />
                <circle
                  id="cd"
                  cx={tooltipState.x}
                  cy={tooltipState.y}
                  r={4}
                  fill="var(--acc)"
                />
              </>
            )}
          </svg>

          {tooltipState.visible && (
            <div
              className="tip"
              id="tp"
              style={{
                display: 'block',
                left: `${tooltipState.tipX}px`,
                top: `${tooltipState.tipY}px`,
              }}
            >
              {tooltipState.text}
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h3>Revenue by year</h3>
        <p className="sm mut">Verified filings in $B</p>
        <div id="rv">
          {revenueItems.map((item: RevenueYearItem) => {
            const widthPct = Math.min(100, Math.max(5, (item.amount / maxRevenue) * 100));
            return (
              <div
                key={item.year}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '44px 1fr 56px',
                  gap: '10px',
                  alignItems: 'center',
                  margin: '8px 0',
                  fontVariantNumeric: 'tabular-nums',
                }}
              >
                <span className="mut sm">{item.year}</span>
                <div
                  style={{
                    height: '12px',
                    background: 'var(--line)',
                    borderRadius: '3px',
                    overflow: 'hidden',
                  }}
                >
                  <i
                    className="rb"
                    style={{
                      display: 'block',
                      height: '100%',
                      width: barsAnimated ? `${widthPct}%` : '0%',
                      background: 'var(--acc)',
                      transition: 'width .8s ease',
                    }}
                    data-w={widthPct}
                  />
                </div>
                <b>${item.amount}B</b>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
