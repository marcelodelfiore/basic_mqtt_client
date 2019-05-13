import paho.mqtt.client as paho
import time
import datetime
"""
 Basic client connecting to Cloud MQTT
 
"""
MQTT_FRAME_SIZE = 6

data_list = []
data_pointer = 0

broker_address = 'm15.cloudmqtt.com'
broker_port = 12460
broker_user_name = 'fjobiivi'
broker_password = 'ik8o68Dsnlgk'


def update_database(topic, data):

  print(f'Tópico: {topic}, Data: {data}')

# callback functions
def on_connect(client, userdata, flags, rc):
  print("Connected with code " + str(rc))
  client.subscribe("eqpto1/#")


def on_message(client, userdata, msg):

  topic = (str(msg._topic))[-3:-1]
  payload = str(msg.payload)

  if topic in ['va', 'vb', 'vc']:
    data = payload.strip("'b")
  elif topic in ['pa', 'pb', 'pc']:
    data = payload.strip("'b")
  elif topic in ['ts']:
    data = payload.strip("'b")
    #data = time.ctime(int(payload.strip("'b")))

  update_database(topic, data)

if __name__ == '__main__':

  client = paho.Client()

  client.on_connect = on_connect

  client.on_message = on_message

  client.username_pw_set(broker_user_name, broker_password)
  client.connect(broker_address, broker_port, 60)

  client.loop_forever()

