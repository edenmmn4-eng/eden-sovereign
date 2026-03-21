import React from "react";
import { Composition } from "remotion";
import { StockVideo, TOTAL_DUR } from "./StockVideo";
import { StockSchema } from "./StockVideo/schema";

const DEFAULT_PROPS = {
  ticker: "AAPL",
  companyName: "Apple Inc.",
  sector: "Technology",
  logoUrl: "https://logo.clearbit.com/apple.com",
  score: 74,
  verdict: "BUY",
  vcolor: "#f59e0b",
  horizon: "1Y Strategic",
  price: 190.5,
  pctChange: 1.23,
  marketCap: 2.9e12,
  pe: 28.5,
  peg: 1.8,
  margins: 0.46,
  cagr: 0.08,
  fcfy: 0.035,
  rsi: 58.2,
  nAnalysts: 42,
  targetMean: 215.0,
  targetHigh: 260.0,
  targetLow: 170.0,
  recKey: "BUY",
  priceHistory: [],
  revenue: [
    { year: "2021", value: 365817000000 },
    { year: "2022", value: 394328000000 },
    { year: "2023", value: 383285000000 },
    { year: "2024", value: 391035000000 },
  ],
  netIncome: [
    { year: "2021", value: 94680000000 },
    { year: "2022", value: 99803000000 },
    { year: "2023", value: 96995000000 },
    { year: "2024", value: 93736000000 },
  ],
  grossMargin: [
    { year: "2021", value: 0.418 },
    { year: "2022", value: 0.433 },
    { year: "2023", value: 0.441 },
    { year: "2024", value: 0.458 },
  ],
  opMargin: [
    { year: "2021", value: 0.298 },
    { year: "2022", value: 0.302 },
    { year: "2023", value: 0.299 },
    { year: "2024", value: 0.314 },
  ],
  eps: [
    { year: "2021", value: 5.61 },
    { year: "2022", value: 6.11 },
    { year: "2023", value: 6.13 },
    { year: "2024", value: 6.08 },
  ],
  scoreGrowth: 65,
  scoreProfitability: 88,
  scoreCashFlow: 72,
  scoreTechnical: 61,
  scoreValuation: 55,
  scorePeg: 48,
  dateStr: "Mar 08, 2026",
  ma50: 185.0,
  ma200: 175.0,
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="StockVideo"
      component={StockVideo}
      durationInFrames={TOTAL_DUR}
      fps={30}
      width={1920}
      height={1080}
      schema={StockSchema}
      defaultProps={DEFAULT_PROPS}
    />
  );
};
