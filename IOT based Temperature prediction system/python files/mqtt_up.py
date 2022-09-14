import datetime
import paho.mqtt.client as paho
from paho import mqtt

broker = "broker.hivemq.com"
ports = 1883
topic = "sensors/group14"

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.connect(broker, ports)

def publish(value):
    client.publish(topic, payload= value , qos=1)
