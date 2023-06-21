import { Card, Metric, Grid, Col } from "@tremor/react";

export default function Dashboard() {
  return (
    <main className="p-20 h-screen">
      <Grid numItemsLg={7} className="gap-10 h-full">
        <Col numColSpanLg={5}>
         <div className="grid gap-10 h-full">
            <Card className="h-full" decoration="top" decorationColor="indigo">
              <Metric>Nível do líquido</Metric>
              <Grid numItemsLg={10} className="pt-5">
                <Col numColSpanLg={4}>Indicador</Col>
                <Col numColSpanLg={6}>Grafico</Col>
              </Grid>
            </Card>
            <Card className="h-full" decoration="top" decorationColor="rose">
              <Metric>Vazamento</Metric>
              <Grid numItemsLg={10} className="pt-5">
                <Col numColSpanLg={4}>Indicador</Col>
                <Col numColSpanLg={6}>Grafico</Col>
              </Grid>
            </Card>
          </div>
        </Col>

        <Col numColSpanLg={2}>
          <Card className="h-full" decoration="top" decorationColor="yellow">
            <Metric>Alertas</Metric>
          </Card>
        </Col>
      </Grid>
    </main>
  );
}