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


def on_message(client, userdata, msg):
  print(str(msg.payload))


if __name__ == '__main__':

  client = paho.Client()

  client.on_connect = on_connect()

  client.on_message = on_message()

  client.connect(broker_address, broker_port, 60)
  client.username_pw_set(broker_user_name, broker_password)

  client.loop_forever()

