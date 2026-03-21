import { z } from "zod";

const TimePoint = z.object({ year: z.string(), value: z.number() });
const PricePoint = z.object({ date: z.string(), close: z.number() });

export const StockSchema = z.object({
  ticker: z.string(),
  companyName: z.string(),
  sector: z.string(),
  logoUrl: z.string(),
  score: z.number(),
  verdict: z.string(),
  vcolor: z.string(),
  horizon: z.string(),
  price: z.number(),
  pctChange: z.number(),
  marketCap: z.number(),
  pe: z.number(),
  peg: z.number(),
  margins: z.number(),
  cagr: z.number(),
  fcfy: z.number(),
  rsi: z.number(),
  nAnalysts: z.number(),
  targetMean: z.number(),
  targetHigh: z.number(),
  targetLow: z.number(),
  recKey: z.string(),
  priceHistory: z.array(PricePoint),
  revenue: z.array(TimePoint),
  netIncome: z.array(TimePoint),
  grossMargin: z.array(TimePoint),
  opMargin: z.array(TimePoint),
  eps: z.array(TimePoint),
  scoreGrowth: z.number(),
  scoreProfitability: z.number(),
  scoreCashFlow: z.number(),
  scoreTechnical: z.number(),
  scoreValuation: z.number(),
  scorePeg: z.number(),
  dateStr: z.string(),
  ma50: z.number(),
  ma200: z.number(),
});

export type StockProps = z.infer<typeof StockSchema>;
