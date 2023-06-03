import { Consumer } from 'sqs-consumer';
import { SQSClient } from '@aws-sdk/client-sqs';
import { preprocess } from './preprocess.mjs';

const queueUrl = 'https://sqs.us-east-1.amazonaws.com/650730994064/simulation_read_queue';
const region = 'us-east-1';

const app = Consumer.create({
  queueUrl,
  handleMessage: preprocess,
  sqs: new SQSClient({ region })
});

const handleError = (err) => console.error(err.message);

app.on('error', handleError);
app.on('processing_error', handleError);
app.on('timeout_error', handleError);

app.start();