import sys
import requests
import json
import numpy as np
import pandas as pd
import csv

if __name__ == "__main__":
    key = sys.argv[1]
    ref = sys.argv[2]

    def geturl(key, ref):
        url1 = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key="
        url2 = "&VehicleMonitoringDetailLevel=calls&LineRef="
        url = url1 + key + url2 + ref

        requrl = requests.get(url)
        return requrl.json()


    data = geturl(key, ref)
    businfo = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    busnum = np.size(businfo)
    
    bus_info = pd.DataFrame(columns=['Latitude', 'Longitude', 'Stop Name', 'Stop Status'], index=[0])

    filename = sys.argv[3]
    f = open(filename, 'wb')
    writer = csv.writer(f)
    writer.writerow(["Latitude", "Longitude", "Stop Name", "Stop Status"])
    for i in range(busnum):

        longitude = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
        latitude = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
        stopinfo = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['OnwardCalls']

        if 'OnwardCall' in stopinfo:
            stop_info1 = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall']
            if (np.size(stop_info1)>1):
                stopname = stop_info1[0]["StopPointName"]
                stopstatus = stop_info1[0]["Extensions"]["Distances"]["PresentableDistance"]
            else:
                stopname = 'N/A'
                stopstatus = 'N/A'
        else:
            stopname = 'N/A'
            stopstatus = 'N/A'

        writer.writerow([latitude, longitude, stopname, stopstatus])

    f.close()
    r = open(filename, 'rd')
    reader = csv.reader(r)
    for row in reader:
        print(row)
    r.close()