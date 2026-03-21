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

const fmtB = (v: number) => {
  const abs = Math.abs(v);
  const sign = v < 0 ? "-" : "";
  if (abs >= 1e12) return `${sign}$${(abs / 1e12).toFixed(1)}T`;
  if (abs >= 1e9)  return `${sign}$${(abs / 1e9).toFixed(1)}B`;
  if (abs >= 1e6)  return `${sign}$${(abs / 1e6).toFixed(0)}M`;
  return `${sign}$${abs.toFixed(1)}`;
};

const Bar: React.FC<{
  frame: number; fps: number; delay: number;
  label: string; value: number; maxVal: number;
  color: string; maxH: number; width?: number;
}> = ({ frame, fps, delay, label, value, maxVal, color, maxH, width = 64 }) => {
  const progress = spring({ frame: frame - delay, fps, config: { damping: 200 } });
  const barH = maxVal > 0 ? Math.abs(value / maxVal) * maxH * progress : 0;
  const isNeg = value < 0;

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8, width: width + 16 }}>
      <div style={{
        fontFamily: "JetBrains Mono, monospace", fontSize: 16,
        color: isNeg ? "#ef4444" : color, fontWeight: 700,
        opacity: progress, minHeight: 22, textAlign: "center",
      }}>
        {fmtB(value)}
      </div>
      <div style={{ position: "relative", height: maxH, display: "flex", alignItems: "flex-end" }}>
        <div style={{
          width, height: barH, borderRadius: "6px 6px 0 0",
          background: isNeg ? "#ef4444" : color,
          boxShadow: `0 -4px 18px ${isNeg ? "#ef4444" : color}44`,
        }} />
      </div>
      <div style={{ fontSize: 14, color: "#475569", fontWeight: 600 }}>{label}</div>
    </div>
  );
};

export const FinancialsScene: React.FC<{ props: StockProps }> = ({ props }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity  = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const dividerW      = interpolate(frame, [15, 40], [0, 100], { extrapolateRight: "clamp" });
  const col2Opacity   = interpolate(frame, [fps * 1.5, fps * 1.5 + 25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const col3Opacity   = interpolate(frame, [fps * 3, fps * 3 + 25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const maxRev  = Math.max(...props.revenue.map((r) => r.value), 1);
  const maxNI   = Math.max(...props.netIncome.map((n) => Math.abs(n.value)), 1);
  const maxRevNI = Math.max(maxRev, maxNI);
  const maxEPS  = props.eps.length > 0
    ? Math.max(...props.eps.map((e) => Math.abs(e.value)), 1)
    : 1;

  const fmtPct = (v: number) => `${(v * 100).toFixed(1)}%`;

  // Max bar height fills the available vertical space after title
  const MAX_H = 620;

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(150deg, #07071a 0%, #0e0e28 100%)",
        fontFamily: "Inter, sans-serif",
        padding: "36px 70px 28px 70px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Title */}
      <div style={{ opacity: titleOpacity, marginBottom: 18, flexShrink: 0 }}>
        <div style={{ fontSize: 34, fontWeight: 700, color: "#f1f5f9" }}>
          Financials — {props.ticker}
        </div>
        <div style={{ height: 2, background: `linear-gradient(90deg, ${INDIGO}, transparent)`,
                      width: `${dividerW}%`, marginTop: 10, borderRadius: 2 }} />
      </div>

      {/* 3-column content — fills remaining height */}
      <div style={{ display: "flex", gap: 48, flex: 1, minHeight: 0, alignItems: "stretch" }}>

        {/* ── Column 1: Revenue & Net Income ── */}
        <div style={{ flex: 1.3, display: "flex", flexDirection: "column", minWidth: 0 }}>
          <div style={{ fontSize: 15, color: INDIGO, fontWeight: 700, textTransform: "uppercase",
                        letterSpacing: 1.5, marginBottom: 16, flexShrink: 0 }}>
            Revenue &amp; Net Income
          </div>
          <div style={{ flex: 1, display: "flex", alignItems: "flex-end", gap: 10, flexWrap: "nowrap", overflow: "hidden" }}>
            {props.revenue.map((r, i) => {
              const ni = props.netIncome.find((n) => n.year === r.year);
              return (
                <div key={r.year} style={{ display: "flex", gap: 3, alignItems: "flex-end", flexShrink: 0 }}>
                  <Bar frame={frame} fps={fps} delay={i * 6}
                    label={r.year} value={r.value} maxVal={maxRevNI} color={INDIGO} maxH={MAX_H} width={56} />
                  {ni && (
                    <Bar frame={frame} fps={fps} delay={i * 6 + 3}
                      label="" value={ni.value} maxVal={maxRevNI} color="#10b981" maxH={MAX_H} width={56} />
                  )}
                </div>
              );
            })}
            {/* Legend */}
            <div style={{ display: "flex", flexDirection: "column", gap: 10, marginLeft: 12, paddingBottom: 28, flexShrink: 0 }}>
              {[{ color: INDIGO, label: "Revenue" }, { color: "#10b981", label: "Net Income" }].map((l) => (
                <div key={l.label} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <div style={{ width: 14, height: 14, borderRadius: 3, background: l.color }} />
                  <span style={{ fontSize: 13, color: "#64748b" }}>{l.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── Column 2: Profit Margins table ── */}
        <div style={{ opacity: col2Opacity, flex: 0.85, display: "flex", flexDirection: "column", minWidth: 300 }}>
          <div style={{ fontSize: 15, color: "#f59e0b", fontWeight: 700, textTransform: "uppercase",
                        letterSpacing: 1.5, marginBottom: 16, flexShrink: 0 }}>
            Profit Margins (%)
          </div>
          <table style={{ borderCollapse: "collapse", width: "100%", flex: 1 }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left", padding: "12px 14px", fontSize: 13, color: "#334155",
                              fontWeight: 600, textTransform: "uppercase", letterSpacing: 1 }}>Year</th>
                <th style={{ textAlign: "right", padding: "12px 14px", fontSize: 13, color: "#6366f1",
                              fontWeight: 600, textTransform: "uppercase", letterSpacing: 1 }}>Gross</th>
                <th style={{ textAlign: "right", padding: "12px 14px", fontSize: 13, color: "#f59e0b",
                              fontWeight: 600, textTransform: "uppercase", letterSpacing: 1 }}>Operating</th>
              </tr>
            </thead>
            <tbody>
              {props.grossMargin.map((gm, i) => {
                const om = props.opMargin.find((o) => o.year === gm.year);
                const rowProgress = spring({ frame: frame - fps * 1.5 - i * 10, fps, config: { damping: 200 } });
                return (
                  <tr key={gm.year} style={{
                    opacity: rowProgress,
                    borderBottom: "1px solid rgba(99,102,241,.12)",
                  }}>
                    <td style={{ padding: "18px 14px", fontFamily: "JetBrains Mono, monospace",
                                  fontSize: 17, color: "#94a3b8" }}>{gm.year}</td>
                    <td style={{ padding: "18px 14px", textAlign: "right",
                                  fontFamily: "JetBrains Mono, monospace", fontSize: 20,
                                  fontWeight: 700, color: "#6366f1" }}>
                      {fmtPct(gm.value)}
                    </td>
                    <td style={{ padding: "18px 14px", textAlign: "right",
                                  fontFamily: "JetBrains Mono, monospace", fontSize: 20,
                                  fontWeight: 700,
                                  color: om && om.value >= 0 ? "#f59e0b" : "#ef4444" }}>
                      {om ? fmtPct(om.value) : "—"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          {/* CAGR + FCF callout below margins */}
          <div style={{
            marginTop: 24, padding: "18px 20px", flexShrink: 0,
            background: `${INDIGO}0d`, borderRadius: 14,
            border: `1px solid ${INDIGO}22`,
            display: "flex", gap: 28,
          }}>
            {[
              { label: "Rev CAGR", value: `${(props.cagr * 100).toFixed(1)}%`,  color: INDIGO },
              { label: "FCF Yield", value: `${(props.fcfy * 100).toFixed(1)}%`, color: "#a78bfa" },
              { label: "P/E",       value: props.pe > 0 ? props.pe.toFixed(1) : "N/A", color: "#fb923c" },
            ].map((m) => (
              <div key={m.label}>
                <div style={{ fontSize: 11, color: "#475569", textTransform: "uppercase", letterSpacing: 1 }}>{m.label}</div>
                <div style={{ fontFamily: "JetBrains Mono, monospace", fontSize: 24,
                              fontWeight: 800, color: m.color, marginTop: 4 }}>{m.value}</div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Column 3: EPS bars (or key metrics if no EPS) ── */}
        <div style={{ opacity: col3Opacity, flex: 0.85, display: "flex", flexDirection: "column", minWidth: 0 }}>
          {props.eps.length >= 2 ? (
            <>
              <div style={{ fontSize: 15, color: "#38bdf8", fontWeight: 700, textTransform: "uppercase",
                            letterSpacing: 1.5, marginBottom: 16, flexShrink: 0 }}>
                EPS (Earnings Per Share)
              </div>
              <div style={{ flex: 1, display: "flex", alignItems: "flex-end", gap: 12 }}>
                {props.eps.map((e, i) => (
                  <Bar key={e.year} frame={frame} fps={fps} delay={fps * 3 + i * 6}
                    label={e.year} value={e.value} maxVal={maxEPS} color="#38bdf8" maxH={MAX_H} width={56} />
                ))}
              </div>
            </>
          ) : (
            <>
              <div style={{ fontSize: 15, color: "#38bdf8", fontWeight: 700, textTransform: "uppercase",
                            letterSpacing: 1.5, marginBottom: 16, flexShrink: 0 }}>
                Key Metrics
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 16, flex: 1 }}>
                {[
                  { label: "Gross Margin", value: `${(props.margins * 100).toFixed(1)}%`, color: "#10b981" },
                  { label: "Op Margin",    value: props.opMargin.length > 0 ? `${(props.opMargin[props.opMargin.length-1].value * 100).toFixed(1)}%` : "N/A", color: "#f59e0b" },
                  { label: "FCF Yield",    value: `${(props.fcfy * 100).toFixed(1)}%`, color: "#a78bfa" },
                  { label: "RSI-14",       value: props.rsi.toFixed(1), color: props.rsi > 70 ? "#ef4444" : props.rsi < 30 ? "#f59e0b" : "#10b981" },
                  { label: "P/E Ratio",    value: props.pe > 0 ? props.pe.toFixed(1) : "N/A", color: "#fb923c" },
                  { label: "PEG Ratio",    value: props.peg > 0 ? props.peg.toFixed(2) : "N/A", color: "#f472b6" },
                ].map((m, i) => {
                  const p = spring({ frame: frame - fps * 3 - i * 10, fps, config: { damping: 200 } });
                  return (
                    <div key={m.label} style={{
                      opacity: p,
                      padding: "16px 20px",
                      background: `${m.color}0d`,
                      borderRadius: 12,
                      border: `1px solid ${m.color}22`,
                      flex: 1,
                    }}>
                      <div style={{ fontSize: 12, color: "#475569", textTransform: "uppercase", letterSpacing: 1 }}>{m.label}</div>
                      <div style={{ fontFamily: "JetBrains Mono, monospace", fontSize: 26,
                                    fontWeight: 800, color: m.color, marginTop: 6 }}>{m.value}</div>
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </div>

      </div>
    </AbsoluteFill>
  );
};
