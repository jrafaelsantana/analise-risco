import os
import OpenOPC
import boto3

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def printInfos(interation, time_start):
  print("Captura iniciada as: " + time_start)
  print(str(interation) + ' novas linhas enviadas para a fila.')

def connectOpc(opc_server, opc_host):
  opc = OpenOPC.client()
  opc.connect(opc_server, opc_host)

  return opc

def publishMessageToSns(topic_name, region_name, message):
   sns_client = boto3.client("sns", region_name)
   message_id = sns_client.publish(TopicArn=topic_name, Message=message)

   return message_id
