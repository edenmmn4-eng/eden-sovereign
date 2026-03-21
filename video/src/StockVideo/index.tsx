import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { z } from "zod";
import { StockSchema } from "./schema";
import { CoverScene }      from "./CoverScene";
import { PriceChartScene } from "./PriceChartScene";
import { FinancialsScene } from "./FinancialsScene";
import { RadarScene }      from "./RadarScene";
import { VerdictScene }    from "./VerdictScene";

const FPS = 30;
const COVER_DUR     = 4  * FPS;
const PRICE_DUR     = 6  * FPS;
const FIN_DUR       = 7  * FPS;
const RADAR_DUR     = 7  * FPS;
const VERDICT_DUR   = 6  * FPS;

const PRICE_START   = COVER_DUR;
const FIN_START     = PRICE_START + PRICE_DUR;
const RADAR_START   = FIN_START   + FIN_DUR;
const VERDICT_START = RADAR_START + RADAR_DUR;
export const TOTAL_DUR = VERDICT_START + VERDICT_DUR;

export const StockVideo: React.FC<z.infer<typeof StockSchema>> = (props) => {
  return (
    <AbsoluteFill style={{ background: "#07071a" }}>
      <Sequence from={0} durationInFrames={COVER_DUR}>
        <CoverScene props={props} />
      </Sequence>
      <Sequence from={PRICE_START} durationInFrames={PRICE_DUR}>
        <PriceChartScene props={props} />
      </Sequence>
      <Sequence from={FIN_START} durationInFrames={FIN_DUR}>
        <FinancialsScene props={props} />
      </Sequence>
      <Sequence from={RADAR_START} durationInFrames={RADAR_DUR}>
        <RadarScene props={props} />
      </Sequence>
      <Sequence from={VERDICT_START} durationInFrames={VERDICT_DUR}>
        <VerdictScene props={props} />
      </Sequence>
    </AbsoluteFill>
  );
};
