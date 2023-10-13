import { MongoDBConnector } from "./database/mongodb.mjs";

const saveHistoric = async (connector, data) => {
  await connector.insertRecord("historic", data);
};

const saveAlert = async (connector, alert) => {
  const now = new Date();
  const secondsAgo = new Date(now.getTime() - 30000);

  const query = {
    message: alert.message,
    sensors: { $all: alert.sensors },
    lastViewed: { $gte: secondsAgo, $lt: now },
  };

  const find = await connector.findOne("alerts", query);

  if (!find) {
    await connector.insertRecord("alerts", alert);
  } else {
    find.lastViewed = new Date();

    await connector.updateOne("alerts", find._id, { $set: find });
  }
};

const preprocess = async (connector, data) => {
  const isTransmissorEquals = (...args) =>
    (Math.max(...args) - Math.min(...args)).toFixed(2) <= 0.02;

  if (
    !isTransmissorEquals(
      data["Transmissor.TR1.OUT"],
      data["Transmissor.TR2.OUT"]
    )
  ) {
    const alert = {
      datetime: new Date(),
      lastViewed: new Date(),
      message: "Transmissores com leituras diferentes.",
      sensors: ["Transmissor.TR1.OUT", "Transmissor.TR2.OUT"],
      data: {
        "Transmissor.TR1.OUT": data["Transmissor.TR1.OUT"],
        "Transmissor.TR2.OUT": data["Transmissor.TR2.OUT"],
      },
    };
    await saveAlert(connector, alert);
  }

  if (
    !isTransmissorEquals(
      data["Transmissor.TR2.OUT"],
      data["Transmissor.TR3.OUT"]
    )
  ) {
    const alert = {
      datetime: new Date(),
      lastViewed: new Date(),
      message: "Transmissores com leituras diferentes.",
      sensors: ["Transmissor.TR2.OUT", "Transmissor.TR3.OUT"],
      data: {
        "Transmissor.TR2.OUT": data["Transmissor.TR2.OUT"],
        "Transmissor.TR3.OUT": data["Transmissor.TR3.OUT"],
      },
    };
    await saveAlert(connector, alert);
  }

  if (
    !isTransmissorEquals(
      data["Transmissor.TR1.OUT"],
      data["Transmissor.TR3.OUT"]
    )
  ) {
    const alert = {
      datetime: new Date(),
      lastViewed: new Date(),
      message: "Transmissores com leituras diferentes.",
      sensors: ["Transmissor.TR1.OUT", "Transmissor.TR3.OUT"],
      data: {
        "Transmissor.TR1.OUT": data["Transmissor.TR1.OUT"],
        "Transmissor.TR3.OUT": data["Transmissor.TR3.OUT"],
      },
    };
    await saveAlert(connector, alert);
  }
};

export const handleMessage = async (message) => {
  const connector = new MongoDBConnector(process.env.MONGODB_URI);
  await connector.connect();

  const messageBody = JSON.parse(message.Body);
  const data = JSON.parse(messageBody.Message)[0];

  await Promise.all([
    saveHistoric(connector, data),
    preprocess(connector, data),
  ]);

  connector.close();
};
