import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { evolvePath } from "@remotion/paths";
import type { StockProps } from "./schema";

const INDIGO = "#6366f1";
const W = 1780;
const H = 700;
const PAD = { l: 90, r: 160, t: 40, b: 70 };

export const PriceChartScene: React.FC<{ props: StockProps }> = ({ props }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const chartProgress = interpolate(frame, [20, 4 * fps], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  const statsOpacity = interpolate(frame, [3 * fps, 3 * fps + 20], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const maOpacity = interpolate(frame, [3 * fps + 10, 3 * fps + 30], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  const hist = props.priceHistory;
  if (!hist || hist.length < 2) return null;

  const prices = hist.map((p) => p.close);
  const allVals = [...prices];
  if (props.ma50 > 0)  allVals.push(props.ma50);
  if (props.ma200 > 0) allVals.push(props.ma200);
  const minP = Math.min(...allVals) * 0.97;
  const maxP = Math.max(...allVals) * 1.03;
  const chartW = W - PAD.l - PAD.r;
  const chartH = H - PAD.t - PAD.b;

  const toX = (i: number) => PAD.l + (i / (hist.length - 1)) * chartW;
  const toY = (p: number) => PAD.t + chartH - ((p - minP) / (maxP - minP)) * chartH;

  const pathD = hist.map((p, i) => `${i === 0 ? "M" : "L"} ${toX(i)} ${toY(p.close)}`).join(" ");
  const fillD = `${pathD} L ${toX(hist.length - 1)} ${PAD.t + chartH} L ${toX(0)} ${PAD.t + chartH} Z`;

  const { strokeDasharray, strokeDashoffset } = evolvePath(chartProgress, pathD);

  // Stats
  const firstP = hist[0].close;
  const lastP  = hist[hist.length - 1].close;
  const pctChange = ((lastP - firstP) / firstP) * 100;
  const isUp = pctChange >= 0;
  const priceColor = isUp ? "#10b981" : "#ef4444";

  // Y axis labels
  const yTicks = 6;
  const yLabels = Array.from({ length: yTicks }, (_, i) => {
    const val = minP + ((maxP - minP) * i) / (yTicks - 1);
    return { y: toY(val), label: `$${val.toFixed(0)}` };
  });

  // Current price line Y
  const curY = toY(lastP);
  const priceLineOpacity = interpolate(frame, [4 * fps - 10, 4 * fps + 10], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // MA line Y positions (only if valid)
  const yMA50  = props.ma50  > 0 ? toY(props.ma50)  : null;
  const yMA200 = props.ma200 > 0 ? toY(props.ma200) : null;

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(150deg, #07071a 0%, #0e0e28 100%)",
        fontFamily: "Inter, sans-serif",
        padding: "36px 60px 24px 60px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Title */}
      <div style={{ opacity: titleOpacity, marginBottom: 12 }}>
        <div style={{ fontSize: 32, fontWeight: 700, color: "#f1f5f9" }}>
          {props.ticker} — Price History
        </div>
        <div style={{ fontSize: 15, color: "#475569", marginTop: 4 }}>1-Year · Daily Close</div>
      </div>

      {/* Chart SVG */}
      <svg width={W} height={H} style={{ overflow: "visible", flex: 1 }}>
        {/* Grid lines */}
        {yLabels.map((t, i) => (
          <g key={i}>
            <line x1={PAD.l} y1={t.y} x2={PAD.l + chartW} y2={t.y}
              stroke="rgba(99,102,241,.12)" strokeWidth={1} strokeDasharray="4,6" />
            <text x={PAD.l - 10} y={t.y + 5} textAnchor="end"
              fill="#475569" fontSize={14} fontFamily="JetBrains Mono, monospace">
              {t.label}
            </text>
          </g>
        ))}

        {/* Fill gradient */}
        <defs>
          <linearGradient id="fillGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={INDIGO} stopOpacity={0.20 * chartProgress} />
            <stop offset="100%" stopColor={INDIGO} stopOpacity={0} />
          </linearGradient>
          <clipPath id="lineClip">
            <rect x={PAD.l} y={PAD.t} width={chartW * chartProgress} height={chartH + 10} />
          </clipPath>
        </defs>
        <path d={fillD} fill="url(#fillGrad)" clipPath="url(#lineClip)" />

        {/* MA200 line */}
        {yMA200 !== null && (
          <g style={{ opacity: maOpacity }}>
            <line x1={PAD.l} y1={yMA200} x2={PAD.l + chartW} y2={yMA200}
              stroke="#ef4444" strokeWidth={2} strokeDasharray="14,6" />
            <rect x={PAD.l + chartW + 4} y={yMA200 - 14} width={148} height={28} rx={6}
              fill="#ef444422" stroke="#ef444455" strokeWidth={1} />
            <text x={PAD.l + chartW + 12} y={yMA200 + 5} fill="#ef4444"
              fontSize={17} fontWeight={700} fontFamily="JetBrains Mono, monospace">
              MA200 ${props.ma200.toFixed(0)}
            </text>
          </g>
        )}

        {/* MA50 line */}
        {yMA50 !== null && (
          <g style={{ opacity: maOpacity }}>
            <line x1={PAD.l} y1={yMA50} x2={PAD.l + chartW} y2={yMA50}
              stroke="#f59e0b" strokeWidth={2} strokeDasharray="14,6" />
            <rect x={PAD.l + chartW + 4} y={yMA50 - 14} width={148} height={28} rx={6}
              fill="#f59e0b22" stroke="#f59e0b55" strokeWidth={1} />
            <text x={PAD.l + chartW + 12} y={yMA50 + 5} fill="#f59e0b"
              fontSize={17} fontWeight={700} fontFamily="JetBrains Mono, monospace">
              MA50 ${props.ma50.toFixed(0)}
            </text>
          </g>
        )}

        {/* Price line */}
        <path
          d={pathD}
          fill="none"
          stroke={INDIGO}
          strokeWidth={4}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
        />

        {/* Current price dashed line */}
        <g style={{ opacity: priceLineOpacity }}>
          <line x1={PAD.l} y1={curY} x2={PAD.l + chartW} y2={curY}
            stroke={priceColor} strokeWidth={2} strokeDasharray="8,5" />
          <rect x={PAD.l + chartW + 4} y={curY - 18} width={148} height={36} rx={8}
            fill={`${priceColor}22`} stroke={`${priceColor}55`} strokeWidth={1.5} />
          <text x={PAD.l + chartW + 78} y={curY + 7} textAnchor="middle"
            fill={priceColor} fontSize={24} fontWeight={800}
            fontFamily="JetBrains Mono, monospace">
            ${lastP.toFixed(0)}
          </text>
        </g>

        {/* Axes */}
        <line x1={PAD.l} y1={PAD.t} x2={PAD.l} y2={PAD.t + chartH}
          stroke="rgba(99,102,241,.3)" strokeWidth={1.5} />
        <line x1={PAD.l} y1={PAD.t + chartH} x2={PAD.l + chartW} y2={PAD.t + chartH}
          stroke="rgba(99,102,241,.3)" strokeWidth={1.5} />
      </svg>

      {/* Stats bar */}
      <div style={{
        opacity: statsOpacity,
        display: "flex", gap: 36, marginTop: 16,
        fontFamily: "JetBrains Mono, monospace",
        flexWrap: "wrap",
      }}>
        {[
          { label: "Current",  value: `$${lastP.toFixed(2)}`,                                              color: "#f1f5f9" },
          { label: "1Y Change",value: `${pctChange >= 0 ? "+" : ""}${pctChange.toFixed(1)}%`,              color: priceColor },
          { label: "1Y Low",   value: `$${Math.min(...prices).toFixed(2)}`,                                color: "#64748b" },
          { label: "1Y High",  value: `$${Math.max(...prices).toFixed(2)}`,                                color: "#64748b" },
          { label: "MA 50",    value: props.ma50  > 0 ? `$${props.ma50.toFixed(0)}`  : "N/A",             color: "#f59e0b" },
          { label: "MA 200",   value: props.ma200 > 0 ? `$${props.ma200.toFixed(0)}` : "N/A",             color: "#ef4444" },
          { label: "RSI-14",   value: props.rsi.toFixed(1), color: props.rsi > 70 ? "#ef4444" : props.rsi < 30 ? "#f59e0b" : "#10b981" },
        ].map((s, i) => (
          <div key={i}>
            <div style={{ fontSize: 12, color: "#334155", textTransform: "uppercase", letterSpacing: 1 }}>
              {s.label}
            </div>
            <div style={{ fontSize: 22, fontWeight: 700, color: s.color, marginTop: 4 }}>
              {s.value}
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
