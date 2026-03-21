import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { StockProps } from "./schema";

const INDIGO = "#6366f1";
const CX = 480;
const CY = 420;
const R  = 280;

const dims = [
  { key: "scoreGrowth",       label: "Growth" },
  { key: "scoreProfitability", label: "Profitability" },
  { key: "scoreCashFlow",     label: "Cash Flow" },
  { key: "scoreTechnical",    label: "Technical" },
  { key: "scoreValuation",    label: "Valuation" },
  { key: "scorePeg",          label: "PEG" },
] as const;

const polar = (angle: number, r: number) => ({
  x: CX + r * Math.cos(angle),
  y: CY + r * Math.sin(angle),
});

export const RadarScene: React.FC<{ props: StockProps }> = ({ props }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = interpolate(
    spring({ frame, fps, config: { damping: 200 } }),
    [0, 1], [0, 1],
  );
  const labelsOpacity = interpolate(frame, [20, 50], [0, 1], { extrapolateRight: "clamp" });
  const statsOpacity  = interpolate(frame, [fps * 3, fps * 3 + 30], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  const n = dims.length;
  const angles = dims.map((_, i) => (i / n) * 2 * Math.PI - Math.PI / 2);

  // Grid circles
  const gridLevels = [25, 50, 75, 100];

  // Data polygon
  const dataPoints = dims.map((d, i) => {
    const val = (props[d.key] / 100) * R * progress;
    return polar(angles[i], val);
  });
  const dataPolygon = dataPoints.map((p) => `${p.x},${p.y}`).join(" ");

  // Grid polygons
  const gridPolygons = gridLevels.map((level) => {
    return angles.map((a) => {
      const p = polar(a, (level / 100) * R);
      return `${p.x},${p.y}`;
    }).join(" ");
  });

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(150deg, #07071a 0%, #0e0e28 100%)",
        fontFamily: "Inter, sans-serif",
        display: "flex",
        flexDirection: "row",
        padding: "40px 60px",
        gap: 60,
      }}
    >
      {/* Left: Radar SVG */}
      <div style={{ flex: "0 0 auto" }}>
        <div style={{ fontSize: 28, fontWeight: 700, color: "#f1f5f9", marginBottom: 12 }}>
          Score Breakdown
        </div>
        <div style={{ fontSize: 14, color: "#334155", marginBottom: 24 }}>
          Multi-factor analysis · 0–100 per dimension
        </div>

        <svg width={960} height={840} style={{ overflow: "visible" }}>
          {/* Grid polygons */}
          {gridPolygons.map((poly, i) => (
            <polygon key={i} points={poly} fill="none"
              stroke="rgba(99,102,241,.12)" strokeWidth={1} />
          ))}
          {/* Axis lines */}
          {angles.map((a, i) => {
            const outer = polar(a, R);
            return (
              <line key={i} x1={CX} y1={CY} x2={outer.x} y2={outer.y}
                stroke="rgba(99,102,241,.15)" strokeWidth={1} />
            );
          })}

          {/* Data polygon fill */}
          <polygon points={dataPolygon}
            fill={`${INDIGO}25`} stroke={INDIGO} strokeWidth={2.5}
            strokeLinejoin="round" />

          {/* Data points */}
          {dataPoints.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r={8}
              fill={INDIGO} stroke="#07071a" strokeWidth={2.5} />
          ))}

          {/* Labels */}
          <g style={{ opacity: labelsOpacity }}>
            {dims.map((d, i) => {
              const outer = polar(angles[i], R + 36);
              const score = props[d.key];
              const color = score >= 70 ? "#10b981" : score >= 45 ? "#f59e0b" : "#ef4444";
              const anchor = outer.x < CX - 10 ? "end" : outer.x > CX + 10 ? "start" : "middle";
              return (
                <g key={d.key}>
                  <text x={outer.x} y={outer.y - 2} textAnchor={anchor}
                    fill="#94a3b8" fontSize={15} fontWeight={600}>
                    {d.label}
                  </text>
                  <text x={outer.x} y={outer.y + 18} textAnchor={anchor}
                    fill={color} fontSize={18} fontWeight={800}
                    fontFamily="JetBrains Mono, monospace">
                    {score.toFixed(0)}
                  </text>
                </g>
              );
            })}
          </g>

          {/* Grid level labels */}
          {gridLevels.map((level) => (
            <text key={level} x={CX + 4} y={CY - (level / 100) * R + 4}
              fill="rgba(99,102,241,.35)" fontSize={10}
              fontFamily="JetBrains Mono, monospace">
              {level}
            </text>
          ))}

          {/* Center score */}
          <text x={CX} y={CY - 18} textAnchor="middle"
            fill="#f1f5f9" fontSize={52} fontWeight={900}
            fontFamily="JetBrains Mono, monospace">
            {props.score}
          </text>
          <text x={CX} y={CY + 20} textAnchor="middle"
            fill="#334155" fontSize={14} fontWeight={600} letterSpacing={2}>
            SOVEREIGN SCORE
          </text>
        </svg>
      </div>

      {/* Right: dimension breakdown list */}
      <div style={{ opacity: statsOpacity, flex: 1, display: "flex", flexDirection: "column",
                    gap: 18, justifyContent: "center", paddingTop: 80 }}>
        {dims.map((d) => {
          const score = props[d.key];
          const barProgress = spring({ frame: frame - fps * 3, fps, config: { damping: 200 } });
          const color = score >= 70 ? "#10b981" : score >= 45 ? "#f59e0b" : "#ef4444";
          return (
            <div key={d.key}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <span style={{ fontSize: 14, color: "#64748b", fontWeight: 600 }}>{d.label}</span>
                <span style={{ fontFamily: "JetBrains Mono, monospace", fontSize: 16,
                               fontWeight: 800, color }}>{score.toFixed(0)}</span>
              </div>
              <div style={{ height: 8, background: "rgba(99,102,241,.1)", borderRadius: 4 }}>
                <div style={{
                  height: "100%", borderRadius: 4,
                  width: `${(score / 100) * 100 * barProgress}%`,
                  background: `linear-gradient(90deg, ${color}, ${color}88)`,
                  boxShadow: `0 0 10px ${color}55`,
                }} />
              </div>
            </div>
          );
        })}

        {/* Verdict callout */}
        <div style={{
          marginTop: 24, padding: "18px 24px",
          background: `${props.vcolor}12`,
          border: `1.5px solid ${props.vcolor}44`,
          borderRadius: 14,
        }}>
          <div style={{ fontSize: 11, color: "#334155", textTransform: "uppercase",
                        letterSpacing: 2, marginBottom: 6 }}>Verdict</div>
          <div style={{ fontFamily: "JetBrains Mono, monospace", fontSize: 28,
                        fontWeight: 900, color: props.vcolor }}>
            {props.verdict}
          </div>
          <div style={{ fontSize: 13, color: "#475569", marginTop: 6 }}>
            Score {props.score}/100 · Confidence {Math.min(95, 50 + Math.abs(props.score - 50))}%
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
