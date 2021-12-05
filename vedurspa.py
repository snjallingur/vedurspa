import logging
# initialize the log settings
#logging.basicConfig(filename = '/usr/share/hassio/homeassistant/snjallingur_scripts/pythonscripts.log', level = logging.DEBUG)
logging.basicConfig(filename = '/usr/share/hassio/homeassistant/snjallingur_scripts/pythonscripts.log',format='%(asctime)s %(message)s', level = logging.DEBUG)
logging.info('logger for vedurspa started')

try: 
    import requests
    from bs4 import BeautifulSoup
    import time
    from datetime import datetime
    import xml.etree.ElementTree as ET
    import paho.mqtt.client as paho
    import json
except (ImportError,ModuleNotFoundError) as i:
    logging.exception('Import error: ' + str(i))  


# MQTT Broker
broker="localhost"
# create client and connect to broker
try:
    client= paho.Client("client-vedurspa")
    client.username_pw_set(username="homeassistant",password="kjbsldvnæamv")
    client.connect(broker)
    client.loop_start()  #Start loop 
    time.sleep(4) # Wait for connection setup to complete
    client.publish("homeassistant/vedurspa","running")
except Exception as e:
    print(e)
    logging.exception(str(e)) 
    logging.error('Couldn´t connect to MQTT broker ' + str(e)) 
    
# Frekari upplýsingar um skiluð svör:
# https://www.vedur.is/skjol/vefur/XML-thjonusta-090813.pdf
#
url = 'https://xmlweather.vedur.is/?op_w=xml&type=forec&lang=is&view=xml&ids=1;1779'

try:
    document = requests.get(url, verify=False)
    vedurspa = BeautifulSoup(document.content,"lxml-xml")
    content = vedurspa.find_all("station")       
except (IOError,NameError) as e:
    logging.exception(str(e)) 
    logging.error('Error occurred ' + str(e)) 

reykjavik_6h = {}
reykjavik_12h = {}
hvanneyri_6h = {}
hvanneyri_12h = {}

for station in content:
    # print(content['station'])
    name = station.find("name").string
    forecasts = station.find_all("forecast")
    #print(name)
    if name == 'Reykjavík':
        for forecast_element in forecasts:
            forecast_time = forecast_element.find("ftime").string
            time_now = datetime.now()
            forecast_timespamp = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S")
            timedelta_seconds = (forecast_timespamp - time_now).seconds
            timedelta_hours = round(timedelta_seconds/3600,0)
            timedelta_days = (forecast_timespamp - time_now).days
            if timedelta_days == 1:
                #print("Timedelta in hours: " + str(timedelta_hours))
                #print(forecast_time)
                if str(timedelta_hours) in ['6.0']:
                    forecast_temperature = forecast_element.find("T").string
                    reykjavik_6h['temperature'] = forecast_element.find("T").string
                    reykjavik_6h['wind_speed'] = forecast_element.find("F").string
                    reykjavik_6h['wind_direction'] = forecast_element.find("D").string
                    reykjavik_6h['forecast'] = forecast_element.find("W").string
                    #print("Temperature Forecast for " + forecast_time + " is " + forecast_temperature + " degrees")
                    reykjavik_6h = json.dumps(reykjavik_6h, separators=(',', ':'))
                    #print(reykjavik_6h)
                    client.publish("homeassistant/vedurspa/reykjavik/6h",str(reykjavik_6h))
                if str(timedelta_hours) in ['12.0']:
                    forecast_temperature = forecast_element.find("T").string
                    reykjavik_12h['temperature'] = forecast_element.find("T").string
                    reykjavik_12h['wind_speed'] = forecast_element.find("F").string
                    reykjavik_12h['wind_direction'] = forecast_element.find("D").string
                    reykjavik_12h['forecast'] = forecast_element.find("W").string
                    #print("Temperature Forecast for " + forecast_time + " is " + forecast_temperature + " degrees")
                    reykjavik_12h = json.dumps(reykjavik_12h, separators=(',', ':'))
                    #print(reykjavik_6h)
                    client.publish("homeassistant/vedurspa/reykjavik/12h",str(reykjavik_12h))
    if name == 'Hvanneyri':
        for forecast_element in forecasts:
            forecast_time = forecast_element.find("ftime").string
            time_now = datetime.now()
            forecast_timespamp = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S")
            timedelta_seconds = (forecast_timespamp - time_now).seconds
            timedelta_hours = round(timedelta_seconds/3600,0)
            timedelta_days = (forecast_timespamp - time_now).days
            if timedelta_days == 1:
                #print("Timedelta in hours: " + str(timedelta_hours))
                #print(forecast_time)
                if str(timedelta_hours) in ['6.0']:
                    forecast_temperature = forecast_element.find("T").string
                    hvanneyri_6h['temperature'] = forecast_element.find("T").string
                    hvanneyri_6h['wind_speed'] = forecast_element.find("F").string
                    hvanneyri_6h['wind_direction'] = forecast_element.find("D").string
                    hvanneyri_6h['forecast'] = forecast_element.find("W").string
                    #print("Temperature Forecast for " + forecast_time + " is " + forecast_temperature + " degrees")
                    hvanneyri_6h = json.dumps(hvanneyri_6h, separators=(',', ':'))
                    #print(reykjavik_6h)
                    client.publish("homeassistant/vedurspa/hvanneyri/6h",str(hvanneyri_6h))
                if str(timedelta_hours) in ['12.0']:
                    forecast_temperature = forecast_element.find("T").string
                    hvanneyri_12h['temperature'] = forecast_element.find("T").string
                    hvanneyri_12h['wind_speed'] = forecast_element.find("F").string
                    hvanneyri_12h['wind_direction'] = forecast_element.find("D").string
                    hvanneyri_12h['forecast'] = forecast_element.find("W").string
                    #print("Temperature Forecast for " + forecast_time + " is " + forecast_temperature + " degrees")
                    hvanneyri_12h = json.dumps(hvanneyri_12h, separators=(',', ':'))
                    #print(reykjavik_6h)
                    client.publish("homeassistant/vedurspa/hvanneyri/12h",str(hvanneyri_12h))     

client.loop_stop()    #Stop loop 
client.disconnect()
