from Rcfalgorithm import rcfalgorithm
import xlrd
import requests
import numpy as np
from time import sleep
from sklearn.ensemble import IsolationForest
from math import isnan

'''
battery_data = []
hvac_cur_data = []
hvac_air_data = []


def battery_cond(datapoint):
	url = 'http://127.0.0.1:8080/iotpoc'
	global battery_data

	if len(battery_data)>100:
		del battery_data[0]
			
	anomaly = rcfalgorithm(battery_data, 10)

	anomalyround = anomaly

	if anomaly > 50:
		anomalyround = 50.0

	anomalyinvert = 52.0-anomalyround

	data_write = [{"measurement": "battery","fields": {"volatge": datapoint,"batteryanomaly": anomaly, "anomalyround": anomalyround, "batterystatus": anomalyinvert}}]


	if anomaly > 30:
		battery_data.pop()		

			
	x = requests.post(url, json = data_write)



def hvac_current_cond(datapoint):
	url = 'http://127.0.0.1:8080/iotpoc'
	global hvac_cur_data

	if len(hvac_cur_data)>100:
		del hvac_cur_data[0]
			
	anomaly = rcfalgorithm(hvac_cur_data, 10)

	anomalyround = anomaly

	if anomaly > 50:
		anomalyround = 50.0

	anomalyinvert = 52.0-anomalyround

	data_write = [{"measurement": "hvaccurrent","fields": {"current": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert}}]


	if anomaly > 30:
		hvac_cur_data.pop()		

			
	x = requests.post(url, json = data_write)


			

def hvac_airtemp_cond(datapoint):
	url = 'http://127.0.0.1:8080/iotpoc'
	global hvac_air_data

	if len(hvac_air_data)>100:
		del hvac_air_data[0]
			
	anomaly = rcfalgorithm(hvac_air_data, 10)

	anomalyround = anomaly

	if anomaly > 50:
		anomalyround = 50.0

	anomalyinvert = 52.0-anomalyround

	data_write = [{"measurement": "hvacairtemp","fields": {"airtemp": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert}}]


	if anomaly > 30:
		hvac_air_data.pop()		

			
	x = requests.post(url, json = data_write)

'''

if __name__ == "__main__":

	work=xlrd.open_workbook("rcfdata.xls")
	worksheet=work.sheet_by_index(0)
	url = 'http://127.0.0.1:8080/iotpoc'

	battery_data = np.array([])
	battery_np = np.array([])
	hvac_cur_data = []
	hvac_air_data = []

	while True:
		for i in range(1,100):
			datapoint = worksheet.cell_value(i,0)
			hvac_cur_data.append(datapoint)

			if len(hvac_cur_data)>100:
				del hvac_cur_data[0]
					
			anomaly = rcfalgorithm(hvac_cur_data, 10)

			anomalyround = anomaly

			if anomaly > 50:
				anomalyround = 50.0

			anomalyinvert = 52.0-anomalyround

			data_write = [{"measurement": "hvaccurrent","fields": {"current": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert}}]


			if anomaly > 30:
				hvac_cur_data.pop()		

					
			x = requests.post(url, json = data_write)

			

###########################################################################################
			datapoint = worksheet.cell_value(i,1)
			hvac_air_data.append(datapoint)
					
			if len(hvac_air_data)>100:
				del hvac_air_data[0]
					
			anomaly = rcfalgorithm(hvac_air_data, 10)

			anomalyround = anomaly

			if anomaly > 50:
				anomalyround = 50.0

			anomalyinvert = 52.0-anomalyround

			data_write = [{"measurement": "hvacairtemp","fields": {"airtemp": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert}}]


			if anomaly > 30:
				hvac_air_data.pop()		

					
			x = requests.post(url, json = data_write)

###########################################################################################
			datapoint = worksheet.cell_value(i,2)
			battery_data = np.append(battery_data, datapoint)
			#battery_cond(datapoint)

			if len(battery_data)>100:
				battery_data = battery_data[1:]
			
			battery_np = battery_data.reshape(-1,1)
			
			model = IsolationForest(n_estimators =100, max_samples ='auto',contamination=float(0.2),max_features=1.0)
			model.fit(battery_np)
			anomalylist = model.decision_function(battery_np)

			anomaly = list(anomalylist).pop()

			
			if isnan(anomaly):
				anomaly = 0.0

			anomalyround = anomaly + 1.0

			anomalyinvert = 2.0 - anomalyround

			data_write = [{"measurement": "battery","fields": {"volatge": datapoint,"batteryanomaly": anomaly, "anomalyround": anomalyround, "batterystatus": anomalyinvert}}]
			

			if anomaly < -0.3:
				battery_data = battery_data[:-1]	

			#print("battery",i)		
			x = requests.post(url, json = data_write)
				
			sleep(1)
