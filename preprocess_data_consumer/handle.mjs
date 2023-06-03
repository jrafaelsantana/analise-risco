import { MongoDBConnector } from "./database/mongodb.mjs";

const saveHistoric = async (connector, message) => {
  const messageBody = JSON.parse(message.Body);
  const data = JSON.parse(messageBody.Message)[0];
  await connector.insertRecord('historic', data);
}

const preprocess = async (connector, message) => {
  // TODO
}

export const handleMessage = async (message) => {
  const connector = new MongoDBConnector(process.env.MONGODB_URI);
  await connector.connect();

  await saveHistoric(connector, message);
  await preprocess(connector, message);

  connector.close();
}