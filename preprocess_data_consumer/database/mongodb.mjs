import { MongoClient } from "mongodb";

export class MongoDBConnector {
  constructor(url) {
    this.url = url;
    this.client = null;
  }

  async connect() {
    try {
      this.client = await MongoClient.connect(this.url, { useNewUrlParser: true, useUnifiedTopology: true });
    } catch (err) {
      console.error('Failed to connect to MongoDB:', err);
    }
  }

  async insertRecord(collectionName, record) {
    try {
      const db = this.client.db('sensor_data');
      const collection = db.collection(collectionName);
      await collection.insertOne(record);
    } catch (err) {
      console.error('Failed to insert record:', err);
    }
  }

  close() {
    if (this.client) {
      this.client.close();
    }
  }
}