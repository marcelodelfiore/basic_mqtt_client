import paho.mqtt.client as paho

"""
 Basic client connecting to Cloud MQTT
 
"""

broker_address = 'm15.cloudmqtt.com'
broker_port = 12460
broker_user_name = 'fjobiivi'
broker_password = 'ik8o68Dsnlgk'


# callback functions
def on_connect(client, userdata, flags, rc):
  print("Connected with code " + str(rc))
  client.subscribe("eqpto1/#")


def on_message(client, userdata, msg):
  topic = str(msg._topic)[-3:-1]

  if topic in ['va', 'vb', 'vc']:
    mess = str(msg.payload)[-4:-1]
  elif topic in ['ia', 'ib', 'ic']:
    mess = str(msg.payload)[-3:-1]
  else:
    mess = str(msg.payload)[-5:-1]

  print(f'Grandeza: {topic}, Valor: {mess}')


if __name__ == '__main__':

  client = paho.Client()

  client.on_connect = on_connect

  client.on_message = on_message

  client.username_pw_set(broker_user_name, broker_password)
  client.connect(broker_address, broker_port, 60)

  client.loop_forever()

