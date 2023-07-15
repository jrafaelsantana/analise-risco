import { Callout, Card, Metric } from "@tremor/react";
import { useEffect, useState } from "react";
import mlInferenceService from "../../services/mlInferenceService";
import { ExclamationIcon } from "@heroicons/react/solid";
import { format, subHours } from "date-fns";

export default function LiquidLevel() {
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await mlInferenceService.alerts();

        if (result) {
          setAlerts(result["alerts"]);
        }
      } catch (error) {
        console.log("Ocorreu um erro", error);
      }
    };

    const intervalId = setInterval(fetchData, 5000);
    return () => clearInterval(intervalId);
  }, [alerts]);

  return (
    <Card className="h-full" decoration="top" decorationColor="yellow">
      <Metric>Alertas</Metric>
      <div className="h-full mt-4">
        {alerts.map((_alert) => (
          <Callout
            className="h-auto mt-4 bg-yellow-400"
            title={_alert.message}
            icon={ExclamationIcon}
            color="gray"
            key={_alert._id}
          >
            <p>
              Última ocorrência:{" "}
              {format(
                subHours(new Date(_alert.lastViewed), 3),
                "dd/MM/yyyy HH:mm:ss"
              )}
            </p>
            <p>Sensores: {_alert.sensors.join(", ")}</p>
          </Callout>
        ))}
      </div>
    </Card>
  );
}
