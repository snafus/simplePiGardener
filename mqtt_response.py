from __future__ import print_function
import paho.mqtt.client as mqtt
import simpleWaterer
import time,os,sys
from datetime import datetime

broker_address="rpi3-01.local"
simpleWaterer.GPIO.setmode(simpleWaterer.GPIO.BCM)



def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    client.subscribe("garden/water/activate")
    client.subscribe("garden/water/activate/ping")
    client.publish("garden/water/activate/result","Connected;%s" %(datetime.now()))
    

def on_disconnect(client, userdata, rc):
    print("DISCON received with code %d." % (rc))


def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def run(client,on_time, delay):
    relay_pump  = simpleWaterer.Relay(17,active_low=True)
    time.sleep(delay)
    client.publish("garden/water/activate/result","Start;%s" %(datetime.now()))
    simpleWaterer.test1(on_time,relay_pump)
    client.publish("garden/water/activate/result","Done;%s" %(datetime.now()))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.topic == "garden/water/activate":
        try:
            vars = msg.payload.split(";")
            on_time = float(vars[1])
            delay   = float(vars[0])
            run(mqttc,on_time,delay)
        except Exception as e:
            print(e)
            client.publish("garden/water/activate/result","FAIL;%s;%e" %(datetime.now(),e))

    elif msg.topic == "garden/water/activate/ping":
        try:
            client.publish("garden/water/activate/result","Pong;%s" %(datetime.now()))
        except Exception as e:
            print(e)
            


client                = mqtt.Client("rpi2-02")
client.on_connect     = on_connect
client.on_disconnect  = on_disconnect
client.on_subscribe   = on_subscribe
client.on_message     = on_message
client.username_pw_set("mosquitto","12345")

client.connect(broker_address)



with client.loop_forever():
    pass

