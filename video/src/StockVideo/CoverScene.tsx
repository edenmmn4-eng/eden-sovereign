import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { StockProps } from "./schema";

const INDIGO = "#6366f1";
const NAVY   = "#07071a";

export const CoverScene: React.FC<{ props: StockProps }> = ({ props }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // props.logoUrl is pre-verified by Python (_logo_url).
  // Empty string means no valid logo was found — show nothing.
  const hasLogo = !!props.logoUrl;

  const logoScale   = spring({ frame, fps, config: { damping: 200 } });
  const nameOpacity = interpolate(frame, [8, 25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const tickerY     = interpolate(
    spring({ frame: frame - 12, fps, config: { damping: 200 } }),
    [0, 1], [60, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const badgeScale  = spring({ frame: frame - 25, fps, config: { damping: 20, stiffness: 180 } });
  const metaOpacity = interpolate(frame, [35, 55], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  const fmtMcap = (v: number) => {
    if (v >= 1e12) return `$${(v / 1e12).toFixed(1)}T`;
    if (v >= 1e9)  return `$${(v / 1e9).toFixed(1)}B`;
    return `$${(v / 1e6).toFixed(0)}M`;
  };

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(150deg, ${NAVY} 0%, #0e0e28 55%, #091220 100%)`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 20,
        fontFamily: "Inter, sans-serif",
      }}
    >
      {/* Logo + company name block — only rendered when Python confirmed a valid logo */}
      <div style={{ transform: `scale(${logoScale})`, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
        {hasLogo && (
          <Img
            src={props.logoUrl}
            style={{
              width: 200, height: 200, borderRadius: 32, objectFit: "contain",
              background: "#fff", padding: 8,
              boxShadow: `0 0 80px ${INDIGO}55, 0 16px 48px rgba(0,0,0,.7)`,
            }}
          />
        )}

        {/* Company name */}
        <div style={{
          opacity: nameOpacity,
          fontSize: 38, fontWeight: 600, color: "#94a3b8",
          letterSpacing: 0.5, textAlign: "center", maxWidth: 700,
        }}>
          {props.companyName}
        </div>
      </div>

      {/* Ticker */}
      <div style={{ textAlign: "center", transform: `translateY(${tickerY}px)` }}>
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 110, fontWeight: 900, color: "#f1f5f9",
          letterSpacing: -5, lineHeight: 1,
          textShadow: `0 0 80px ${INDIGO}30`,
        }}>
          {props.ticker}
        </div>
      </div>

      {/* Verdict badge */}
      <div style={{
        transform: `scale(${badgeScale})`,
        background: `${props.vcolor}18`,
        border: `2px solid ${props.vcolor}55`,
        borderRadius: 36,
        padding: "12px 40px",
        boxShadow: `0 0 40px ${props.vcolor}22`,
      }}>
        <span style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 30, fontWeight: 800, color: props.vcolor, letterSpacing: 1,
        }}>
          ⚡ {props.score} · {props.verdict}
        </span>
      </div>

      {/* Meta row */}
      <div style={{
        opacity: metaOpacity,
        display: "flex", gap: 20, alignItems: "center", fontSize: 15, color: "#334155",
      }}>
        <span style={{
          background: `${INDIGO}18`, color: "#818cf8",
          padding: "5px 18px", borderRadius: 18, fontSize: 14,
          border: `1px solid ${INDIGO}33`,
        }}>
          {props.sector}
        </span>
        <span style={{ color: "#64748b" }}>{props.horizon}</span>
        <span style={{ color: "#1e293b" }}>·</span>
        <span style={{ color: "#64748b" }}>Market Cap {fmtMcap(props.marketCap)}</span>
        <span style={{ color: "#1e293b" }}>·</span>
        <span style={{ color: "#64748b" }}>{props.dateStr}</span>
      </div>

      {/* Eden Sovereign brand — bottom */}
      <div style={{
        position: "absolute", bottom: 32,
        fontSize: 11, fontWeight: 700, color: `${INDIGO}88`, letterSpacing: 3,
        textTransform: "uppercase",
      }}>
        Eden Sovereign Intelligence Terminal
      </div>
    </AbsoluteFill>
  );
};
