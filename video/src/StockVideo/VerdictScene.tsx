import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { StockProps } from "./schema";

export const VerdictScene: React.FC<{ props: StockProps }> = ({ props }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const labelOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const verdictScale = spring({ frame: frame - 10, fps, config: { damping: 20, stiffness: 200 } });
  const scoreOpacity = interpolate(frame, [30, 55], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const cardOpacity  = interpolate(frame, [50, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const cardY        = interpolate(frame, [50, 80], [30, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const analystOpacity = interpolate(frame, [70, fps * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const confidence = Math.min(95, 50 + Math.abs(props.score - 50));
  const upside = props.targetMean > 0 && props.price > 0
    ? ((props.targetMean - props.price) / props.price * 100) : null;

  const fmtPct = (v: number) => `${(v * 100).toFixed(1)}%`;
  const fmtPrice = (v: number) => `$${v.toFixed(2)}`;

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(150deg, #07071a 0%, #0d0d25 55%, #09111e 100%)`,
        fontFamily: "Inter, sans-serif",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 24,
        padding: "40px 80px",
        textAlign: "center",
      }}
    >
      {/* Label */}
      <div style={{ opacity: labelOpacity, fontSize: 13, fontWeight: 700, color: "#1e293b",
                    letterSpacing: 4, textTransform: "uppercase" }}>
        Sovereign Verdict
      </div>

      {/* Big verdict */}
      <div style={{ transform: `scale(${verdictScale})` }}>
        <div style={{
          fontSize: 110, fontWeight: 900, color: props.vcolor,
          letterSpacing: -4, lineHeight: 1.05,
          textShadow: `0 0 80px ${props.vcolor}44`,
        }}>
          {props.verdict}
        </div>
      </div>

      {/* Score row */}
      <div style={{
        opacity: scoreOpacity,
        display: "flex", gap: 28, alignItems: "center",
        fontFamily: "JetBrains Mono, monospace",
      }}>
        {[
          { label: "Score", value: `${props.score}/100`, color: "#f1f5f9" },
          { label: "Confidence", value: `${confidence}%`, color: "#818cf8" },
          { label: "Horizon", value: props.horizon, color: "#64748b" },
        ].map((item, i) => (
          <React.Fragment key={item.label}>
            {i > 0 && <div style={{ width: 1, height: 44, background: "rgba(99,102,241,.2)" }} />}
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 30, fontWeight: 800, color: item.color }}>{item.value}</div>
              <div style={{ fontSize: 10, color: "#334155", letterSpacing: 1.5,
                            textTransform: "uppercase", marginTop: 4 }}>{item.label}</div>
            </div>
          </React.Fragment>
        ))}
      </div>

      {/* Summary card */}
      <div style={{
        opacity: cardOpacity,
        transform: `translateY(${cardY}px)`,
        maxWidth: 880, textAlign: "left",
        background: `${props.vcolor}08`,
        border: `1.5px solid ${props.vcolor}33`,
        borderLeft: `4px solid ${props.vcolor}99`,
        borderRadius: 14,
        padding: "20px 28px",
      }}>
        <div style={{ fontSize: 16, color: "#64748b", lineHeight: 1.85 }}>
          <strong style={{ color: "#94a3b8" }}>{props.companyName}</strong> is a {props.sector} company.{" "}
          Gross margins <strong style={{ color: "#818cf8" }}>{fmtPct(props.margins)}</strong>{" "}
          · Revenue CAGR <strong style={{ color: "#818cf8" }}>{fmtPct(props.cagr)}</strong>{" "}
          · FCF Yield <strong style={{ color: "#818cf8" }}>{fmtPct(props.fcfy)}</strong>.
        </div>
      </div>

      {/* Analyst consensus */}
      {props.nAnalysts > 0 && (
        <div style={{
          opacity: analystOpacity,
          display: "flex", gap: 24, alignItems: "center",
          background: "rgba(99,102,241,.07)",
          border: "1px solid rgba(99,102,241,.18)",
          borderRadius: 12, padding: "14px 24px",
          fontFamily: "JetBrains Mono, monospace",
        }}>
          <span style={{ fontSize: 11, color: "#6366f1", fontWeight: 700,
                         letterSpacing: 1.5, textTransform: "uppercase" }}>Wall St.</span>
          <span style={{ fontSize: 17, fontWeight: 700, color: "#f1f5f9" }}>{props.recKey}</span>
          <span style={{ fontSize: 13, color: "#475569" }}>{props.nAnalysts} analysts</span>
          {upside !== null && (
            <>
              <span style={{ color: "#1e293b" }}>·</span>
              <span style={{ fontSize: 15, fontWeight: 700,
                             color: upside >= 0 ? "#10b981" : "#ef4444" }}>
                {upside >= 0 ? "+" : ""}{upside.toFixed(1)}% upside
              </span>
              <span style={{ fontSize: 13, color: "#475569" }}>
                Target {fmtPrice(props.targetMean)}
              </span>
            </>
          )}
        </div>
      )}

      {/* Footer */}
      <div style={{ fontSize: 11, color: "#0f172a", marginTop: 4 }}>
        Eden Sovereign Intelligence Terminal · {props.dateStr}
      </div>
    </AbsoluteFill>
  );
};
