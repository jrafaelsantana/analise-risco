
import { Card, Metric, Flex, DonutChart, LineChart, Title } from "@tremor/react";
import probabilityToPercent from "../../utils/probabilityToPercent";
import { useEffect, useState } from "react";
import mlInferenceService from "../../services/mlInferenceService";
import convertDatetime from "../../utils/convertDatetime";

const returnColor = (prob: number) => {
  if (prob < 0.5) {
    return 'green';
  } else if (prob < 0.7) {
    return 'yellow';
  } else {
    return 'red';
  }
}

export default function LiquidLevel() {
  const [historic, setHistoric] = useState<any[]>([]);
  const [current, setCurrent] = useState<any[]>([{ Probabilidade: 0 }]);
  const [lastUpdate, setLastUpdate] = useState<string>();
  const [color, setColor] = useState<"green"|"yellow"|"red">("green");

  useEffect(() => {
    const fetchData= async () => {
      try {
        const result = await mlInferenceService.liquidLevel();

        if (result) {
          const datetime = convertDatetime(result['datetime']);
          result['time'] = datetime.toLocaleTimeString('pt-BR');
          result['Probabilidade'] = result['probability'];
          setLastUpdate(datetime.toLocaleString('pt-BR').replace(',', ''));
          setColor(returnColor(result['probability']));

          delete result['probability'];
        }

        setHistoric(prevData => [...prevData.slice(-10), result]);
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
          <Metric>Nível do líquido</Metric>
          {lastUpdate && <Title>Última Atualização: {lastUpdate}</Title>}
        </Flex>
        <Flex className="h-full flex-row space-x-4">
          <Flex className="w-1/3">
            <DonutChart
              valueFormatter={probabilityToPercent}
              data={current}
              showTooltip={false}
              category="Probabilidade"
              colors={[color]}
            />
          </Flex>
          <Flex className="w-full">
            <LineChart
              className="w-full"
              data={historic}
              index="time"
              categories={["Probabilidade"]}
              colors={["emerald"]}
              valueFormatter={probabilityToPercent}
              yAxisWidth={40}
            />
          </Flex>
        </Flex>
      </Flex>
    </Card>
  );
}