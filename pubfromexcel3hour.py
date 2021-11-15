# importing the library
import paho.mqtt.client as paho
import sys
import json
import xlrd
import signal
from time import sleep
from datetime import datetime, date
work=xlrd.open_workbook("sensor_3_hour.xls")
worksheet=work.sheet_by_index(0)

client=paho.Client()

if client.connect("localhost", 1883, 60)!=0:
	print("could not connect")
	sys.exit(-1)

data={
    "SetId": "Ratnagiri",
    "Position": {
        "Lat": 16.990012,
        "Lon": 73.350058,
        "Alt": 8000
    },
    "DateTime": "2021-09-24:12:36:00",
    "SensorInfo": {
        "ACC": {
            "ACC_X_BASE": "8",
            "ACC_Y_BASE": 8,
            "ACC_X": 1,
            "ACC_Y": 1
        },
        "MOI": {
            "MOI_BASE": 8,
            "MOI": 52.1
        },
        "FLEX": {
            "FLEX_BASE": 8,
            "FLEX": 52.1
        }
    }
}

data1={
    "SetId": "Rajapur",
    "Position": {
        "Lat": 16.6571,
        "Lon": 73.5211,
        "Alt": 8000
    },
    "DateTime": "2021-09-24:12:36:00",
    "SensorInfo": {
        "ACC": {
            "ACC_X_BASE": "8",
            "ACC_Y_BASE": 8,
            "ACC_X": 1,
            "ACC_Y": 1
        },
        "MOI": {
            "MOI_BASE": 8,
            "MOI": 52.1
        },
        "FLEX": {
            "FLEX_BASE": 8,
            "FLEX": 52.1
        }
    }
}

def sensor_data():
	while True:
		for i in range(2,458):
			data["SensorInfo"]["MOI"]["MOI"] = worksheet.cell_value(i,2)
			data["SensorInfo"]["FLEX"]["FLEX"] = worksheet.cell_value(i,3)
			data["SensorInfo"]["ACC"]["ACC_X"] = worksheet.cell_value(i,0)
			data["SensorInfo"]["ACC"]["ACC_Y"] = worksheet.cell_value(i,1)
			data["DateTime"]=str(datetime.now())
			data_out=json.dumps(data)
			client.publish("sensor",data_out)
			sleep(1)

			data1["SensorInfo"]["MOI"]["MOI"] = worksheet.cell_value(i,6)
			data1["SensorInfo"]["FLEX"]["FLEX"] = worksheet.cell_value(i,7)
			data1["SensorInfo"]["ACC"]["ACC_X"] = worksheet.cell_value(i,4)
			data1["SensorInfo"]["ACC"]["ACC_Y"] = worksheet.cell_value(i,5)
			data1["DateTime"]=str(datetime.now())
			data_out=json.dumps(data1)
			client.publish("sensor",data_out)
			sleep(1)

def signal_handler(sig,frame):
	print("pressed ctrl+c")
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT,signal_handler)
	sensor_data()
	client.disconnect()
