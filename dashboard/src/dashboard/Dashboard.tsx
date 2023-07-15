import { Grid, Col } from "@tremor/react";
import LiquidLevel from "../components/LiquidLevel";
import Vazamento from "../components/Vazamento";
import Alerts from "../components/Alerts";

export default function Dashboard() {
  return (
    <main className="p-10 h-screen">
      <Grid numItemsLg={7} className="gap-10 h-full">
        <Col numColSpanLg={5}>
          <div className="grid gap-10 h-full">
            <LiquidLevel />
            <Vazamento />
          </div>
        </Col>
        <Col numColSpanLg={2}>
          <Alerts />
        </Col>
      </Grid>
    </main>
  );
}
