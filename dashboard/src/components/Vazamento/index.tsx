
import { Card, Metric, Flex, DonutChart, LineChart, Title } from "@tremor/react";
import probabilityToPercent from "../../utils/probabilityToPercent";
import { useEffect, useState } from "react";
import mlInferenceService from "../../services/mlInferenceService";

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
  {
    year: 1975,
    "Export Growth Rate": 1.88,
    "Import Growth Rate": 1.67,
  },
];

export default function Vazamento() {
  const [historic, setHistoric] = useState<any[]>([]);
  const [current, setCurrent] = useState<any[]>([{ probability: 0 }]);

  useEffect(() => {
    const fetchData= async () => {
      try {
        const result = await mlInferenceService.vazamento();
        setHistoric(prevData => [...prevData.slice(-50), result]);
        setCurrent([result]);
      } catch (error) {
        console.log('Ocorreu um erro', error);
      }
    }

    const intervalId = setInterval(fetchData, 5000);
    return () => clearInterval(intervalId);
  }, [historic, current]);

  return (
    <Card className="h-full" decoration="top" decorationColor="indigo">
      <Flex className="h-full flex-col">
        <Flex className="w-full h-auto">
          <Metric>Vazamento</Metric>
          <Title>Última Atualização: 09/09/2023 14:09:22</Title>
        </Flex>
        <Flex className="h-full flex-row space-x-4">
          <Flex className="w-1/3">
            <DonutChart
              valueFormatter={probabilityToPercent}
              data={current}
              showTooltip={false}
              category="probability"
              colors={["red"]}
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