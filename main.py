# python 3.6

import random
import time
import random, threading, json
from datetime import datetime
from uart import*
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
# topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
MQTT_Topic_Humidity = "Home/Be1dRoom/DHT22/Humidity"
MQTT_Topic_Temperature = "Home/Be1dRoom/DHT22/Temperature"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# def publish_To_Topic(client, topic, message):
#     result = client.publish(topic, message)
#     status = result[0]
#     if status == 0:
#         print(f"Send `{message}` to topic `{topic}`")
#     else:
#         print(f"Failed to send message to topic {topic}")


# def publish(client,data1,data2):
#     # while True:
#         # global toggle
#         # time.sleep(2)
#     if data1 == "HUMI":
#         Humidity_Value = data2
#
#         Humidity_Data = {}
#         Humidity_Data['Sensor_ID'] = "Dummy-1"
#         Humidity_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
#         Humidity_Data['Humidity'] = Humidity_Value
#         humidity_json_data = json.dumps(Humidity_Data)
#
#         print("Publishing fake Humidity Value: " + str(Humidity_Value) + "...")
#         #publish_To_Topic(client, MQTT_Topic_Humidity, humidity_json_data)
#         result = client.publish(MQTT_Topic_Humidity, humidity_json_data)
#         status = result[0]
#         if status == 0:
#             print(f"Send `{humidity_json_data}` to topic `{MQTT_Topic_Humidity}`")
#         else:
#             print(f"Failed to send message to topic {MQTT_Topic_Humidity}")
#
#     elif data1 == "TEMP":
#         Temperature_Fake_Value = data2
#
#         Temperature_Data = {}
#         Temperature_Data['Sensor_ID'] = "Dummy-2"
#         Temperature_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
#         Temperature_Data['Temperature'] = Temperature_Fake_Value
#         temperature_json_data = json.dumps(Temperature_Data)
#
#         print("Publishing fake Temperature Value: " + str(Temperature_Fake_Value) + "...")
#         #publish_To_Topic(MQTT_Topic_Temperature, temperature_json_data)
#         result = client.publish(MQTT_Topic_Temperature, temperature_json_data)
#         status = result[0]
#         if status == 0:
#             print(f"Send `{temperature_json_data}` to topic `{MQTT_Topic_Temperature}`")
#         else:
#             print(f"Failed to send message to topic {MQTT_Topic_Temperature}")
toggle = 0


# def publish_Fake_Sensor_Values_to_MQTT():
    #threading.Timer(3.0, publish_Fake_Sensor_Values_to_MQTT).start()




#def run():
client = connect_mqtt()
client.loop_start()
while True:
    time.sleep(1)
    readSerial(client)
pass
#publish_Fake_Sensor_Values_to_MQTT()
# client.loop_stop()



# if __name__ == '__main__':
#     run()
