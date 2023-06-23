
import { Card, Metric, Flex, DonutChart, LineChart } from "@tremor/react";
import probabilityToPercent from "../../utils/probabilityToPercent";

const chartdata = [
  {
    year: 1970,
    "Export Growth Rate": 2.04,
    "Import Growth Rate": 1.53,
  },
  {
    year: 1971,
    "Export Growth Rate": 1.96,
    "Import Growth Rate": 1.58,
  },
  {
    year: 1972,
    "Export Growth Rate": 1.96,
    "Import Growth Rate": 1.61,
  },
  {
    year: 1973,
    "Export Growth Rate": 1.93,
    "Import Growth Rate": 1.61,
  },
  {
    year: 1974,
    "Export Growth Rate": 1.88,
    "Import Growth Rate": 1.67,
  },
];

export default function LiquidLevel() {
  const result = [
    {
      name: "Probabilidade",
      prediction: 1,
    }
  ];
  return (
    <Card className="h-full" decoration="top" decorationColor="indigo">
      <Flex className="h-full flex-col">
        <Flex className="w-full h-auto"><Metric>Nível do líquido</Metric></Flex>
        <Flex className="h-full flex-row space-x-4">
          <Flex className="w-1/3">
            <DonutChart
              valueFormatter={probabilityToPercent}
              data={result}
              showTooltip={false}
              category="prediction"
              index="name"
              colors={["green"]}
            />
          </Flex>
          <Flex className="w-full">
            <LineChart
              className="w-full"
              data={chartdata}
              index="year"
              categories={["Export Growth Rate", "Import Growth Rate"]}
              colors={["emerald", "gray"]}
              valueFormatter={probabilityToPercent}
              yAxisWidth={40}
            />
          </Flex>
        </Flex>
      </Flex>
    </Card>
  );
}