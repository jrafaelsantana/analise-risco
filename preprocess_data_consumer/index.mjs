import 'dotenv/config'
import { Consumer } from 'sqs-consumer';
import { SQSClient } from '@aws-sdk/client-sqs';
import { handleMessage } from './handle.mjs';

const app = Consumer.create({
  queueUrl: process.env.QUEUE_URL,
  handleMessage,
  sqs: new SQSClient({ 
    region: process.env.AWS_REGION,
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_KEY
    }
  })
});

const handleError = (err) => console.error(err.message);

app.on('error', handleError);
app.on('processing_error', handleError);
app.on('timeout_error', handleError);

app.start();