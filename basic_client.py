from _datetime import datetime
from random import random

import paho.mqtt.client as paho
import requests

"""
 Basic client connecting to Cloud MQTT and savind data on Slicing Dice
 
"""
data_list = []

topic1 = "148:222:107:191:113:60/#"

broker_address = 'm15.cloudmqtt.com'
broker_port = 12460
broker_user_name = 'fjobiivi'
broker_password = 'ik8o68Dsnlgk'

MASTER_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfX3NhbHQiOiIxNTYwOTcwMDQ0OTA4IiwicGVybWlzc2lvbl9sZXZlbCI6MywicHJvamVjdF9pZCI6MTg1ODg3LCJjbGllbnRfaWQiOjc1MX0.RL5VESP63Q6QaZuubcO4aZdb9vSaWPh6047ZrLROfno"
sd_insert_endpoint_url = "https://api.slicingdice.com/v1/insert"
sd_insert_header = {'Authorization': MASTER_API_KEY, 'content-type': 'application/json'}


def update_database(topic, id, data):

  insert_data = {
    id: {
      "dimension": topic,
      "va": data[0],
      "vb": data[1],
      "vc": data[2],
      "pa": data[3],
      "pb": data[4],
      "pc": data[5],
      "timestamp": id
    },
    "auto-create": ["dimension", "column"]
  }

  resp = requests.post(url=sd_insert_endpoint_url, json=insert_data, headers=sd_insert_header)

  print(id, insert_data, resp.content)


# callback functions
def on_connect(client, userdata, flags, rc):
  print("Connected with code " + str(rc))
  client.subscribe(topic1)


def on_message(client, userdata, msg):

  topic = (str(msg._topic)).strip("'b")
  payload = str(msg.payload)

  _, va,_, vb, _, vc, _, pa, _, pb, _, pc, _, ts = payload.split(";")
  ts = ts.strip("'b")

  unique_ID = datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%dT%H:%M:%SZ')

  data_list[:] = (int(va), int(vb), int(vc), int(pa), int(pb), int(pc))

  dimension = topic.replace(":", "-")

  update_database(dimension, unique_ID, data_list)


if __name__ == '__main__':

  client = paho.Client()

  client.on_connect = on_connect

  client.on_message = on_message

  client.username_pw_set(broker_user_name, broker_password)
  client.connect(broker_address, broker_port, 60)

  client.loop_forever()
