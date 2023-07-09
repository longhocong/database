import json
from datetime import datetime

import serial.tools.list_ports
import time
import threading




# from main import*




def getPort():
    # ports = serial.tools.list_ports.comports()
    # N = len(ports)
    # commPort = "None"
    # for i in range(0, N):
    #     port = ports[i]
    #     strPort = str(port)
    #     print(strPort)
    #     if "CP210x" in strPort:
    #         splitPort = strPort.split(" ")
    #         commPort = (splitPort[0])
    # return commPort
    return "COM4"
if getPort() != "None" :
        ser = serial.Serial( port=getPort(), baudrate=9600)
        print(ser)
mess = ""
MQTT_Topic_Humidity = "Home/Be1dRoom/DHT22/Humidity"
MQTT_Topic_Temperature = "Home/Be1dRoom/DHT22/Temperature"

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    publish(client, splitData[1],splitData[2])
    print(splitData)
    # if splitData[1] == "couter":
    #     publish(client, splitData[2])
    #     # temp_label.config(text="Nhiệt độ hiện tại: {}°C".format(splitData[2]))
    # elif splitData[1] == "LIGHT":
    #     client.publish("cambien2", splitData[2])
    #     # Light_label.config(text="Nhiệt độ hiện tại: {}°C".format(splitData[2]))
    # elif splitData[1] == "button2":
    #     config.setName(config,1)
    #
    #     if splitData[2]=="0":
    #         writeData("5")
    #         client.publish("nutnhan2", "0")
    #     elif   splitData[2]=="1":
    #             writeData("6")
    #             client.publish("nutnhan2", "1")
mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        print(mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client,mess[start:end + 1])
            if (end == len(mess)):
                mess = ""

            else:
                mess = mess[end+1:]
def writeData(data):
    ser.write(str(data).encode())

lock = threading.Lock()
def readSerialWithAck(ack, timer):
    start_time = time.time()
    ack_received =""
    # with lock:
    while time.time() - start_time < timer:
            bytesToRead = ser.inWaiting()
            if bytesToRead > 0:
                ack_received = ack_received + ser.read(bytesToRead).decode("UTF-8")
                if ack_received == ack:
                    print("Ack received: " + ack_received)
                    return True
                else:
                    print("Invalid ack received: " + ack_received)
                    return False
    print("Timed out waiting for ack.")
    return False

# def readSerialWithAck():
#     start_time = time.time()
#     while time.time() - start_time < 2:
#         bytesToRead = ser.inWaiting()
#         if bytesToRead > 0:
#             ack = ser.read(1).decode('UTF-8')
#             if ack == 0:
#                 return 0
#             elif ack == '1':
#                 print(ack)
#                 return 1
#             print(ack)
#     return 0
def publish(client,data1,data2):
    # while True:
        # global toggle
        # time.sleep(2)
    if data1 == "HUMI":
        Humidity_Value = data2

        Humidity_Data = {}
        Humidity_Data['Sensor_ID'] = "Dummy-1"
        Humidity_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        Humidity_Data['Humidity'] = Humidity_Value
        humidity_json_data = json.dumps(Humidity_Data)

        print("Publishing fake Humidity Value: " + str(Humidity_Value) + "...")
        #publish_To_Topic(client, MQTT_Topic_Humidity, humidity_json_data)
        result = client.publish(MQTT_Topic_Humidity, humidity_json_data)
        status = result[0]
        if status == 0:
            print(f"Send `{humidity_json_data}` to topic `{MQTT_Topic_Humidity}`")
        else:
            print(f"Failed to send message to topic {MQTT_Topic_Humidity}")

    elif data1 == "TEMP":
        Temperature_Fake_Value = data2

        Temperature_Data = {}
        Temperature_Data['Sensor_ID'] = "Dummy-2"
        Temperature_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        Temperature_Data['Temperature'] = Temperature_Fake_Value
        temperature_json_data = json.dumps(Temperature_Data)

        print("Publishing fake Temperature Value: " + str(Temperature_Fake_Value) + "...")
        #publish_To_Topic(MQTT_Topic_Temperature, temperature_json_data)
        result = client.publish(MQTT_Topic_Temperature, temperature_json_data)
        status = result[0]
        if status == 0:
            print(f"Send `{temperature_json_data}` to topic `{MQTT_Topic_Temperature}`")
        else:
            print(f"Failed to send message to topic {MQTT_Topic_Temperature}")