import { MongoDBConnector } from "./database/mongodb.mjs";

const saveHistoric = async (connector, data) => {
  await connector.insertRecord('historic', data);
}

const saveAlert = async (connector, message) => {
  const alert = { message };
  await connector.insertRecord('alerts', alert);
}

const preprocess = async (connector, data) => {
  // TODO: Implement rules scheme
  if (
    data['Transmissor.TR1.OUT'] - data['Transmissor.TR2.OUT'] >= 0.02 ||
    data['Transmissor.TR2.OUT'] - data['Transmissor.TR3.OUT'] >= 0.02 ||
    data['Transmissor.TR1.OUT'] - data['Transmissor.TR3.OUT'] >= 0.02
  ) {
    await saveAlert(connector, 'Transmissores com leituras diferentes.');
  }
}

export const handleMessage = async (message) => {
  const connector = new MongoDBConnector(process.env.MONGODB_URI);
  await connector.connect();

  const messageBody = JSON.parse(message.Body);
  const data = JSON.parse(messageBody.Message)[0];

  await saveHistoric(connector, data);
  await preprocess(connector, data);

  connector.close();
}