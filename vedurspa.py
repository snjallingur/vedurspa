# -*- coding: utf-8 -*-
#with the @service defined you will get an option in HA to call the script with a service in the pyscript domain
@service
def vedurspa_rvk():
    update_vedurspa_rvk()

#the @time_trigger will call this script according to the time pattern defined
@time_trigger("cron(*/30 * * * *)")
def update_vedurspa_rvk():
    import logging
    try: 
        import requests
        import re
        import xmltodict
        from bs4 import BeautifulSoup
        import time
        from datetime import datetime
        import xml.etree.ElementTree as ET
        import paho.mqtt.client as paho
        import json
        logging.basicConfig(filename = '/usr/share/hassio/homeassistant/snjallingur_scripts/pythonscripts.log',format='%(asctime)s %(message)s', level = logging.DEBUG)
        logging.info('logger for pyscript started')
    except (ImportError,ModuleNotFoundError) as i:
        logging.exception('Import error: ' + str(i)) 
    #amend the weather station ID. Refer to https://www.vedur.is/vedur/stodvar
    weather_station_id = "1"
    url = "https://xmlweather.vedur.is/?op_w=xml&type=forec&lang=is&view=xml&ids=" + weather_station_id
    
    try:
        #document = requests.get(url, verify=False)
        document = task.executor(requests.get, url)
        vedurspa = BeautifulSoup(document.content,"lxml-xml")
        content = vedurspa.find_all("station")       
    except (IOError,NameError) as e:
        logging.exception(str(e)) 
        logging.error('Error occurred ' + str(e)) 
    
    reykjavik_6h = {}
    reykjavik_12h = {}
    #reykjavik_18h = {}
    sensor6h = 'sensor.vedurspa_reykjavik_6h'
    sensor12h = 'sensor.vedurspa_reykjavik_12h'
    #sensor18h = 'sensor.vedurspa_reykjavik_18h'
    
    for station in content:
        # print(content['station'])
        name = station.find("name").string
        forecasts = station.find_all("forecast")
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
                    #forecast_temperature = forecast_element.find("T").string
                    reykjavik_6h['temperature'] = forecast_element.find("T").string
                    reykjavik_6h['wind_speed'] = forecast_element.find("F").string
                    reykjavik_6h['wind_direction'] = forecast_element.find("D").string
                    reykjavik_6h['forecast'] = forecast_element.find("W").string
                    reykjavik_6h['forecasttime'] = forecast_time
                    #log.info("Temperature Forecast for " + forecast_time + " is " + reykjavik_6h['temperature'] + " degrees")
                    state.set(sensor6h, f"{reykjavik_6h['temperature']}", reykjavik_6h)

                if str(timedelta_hours) in ['12.0']:
                    #forecast_temperature = forecast_element.find("T").string
                    reykjavik_12h['temperature'] = forecast_element.find("T").string
                    reykjavik_12h['wind_speed'] = forecast_element.find("F").string
                    reykjavik_12h['wind_direction'] = forecast_element.find("D").string
                    reykjavik_12h['forecast'] = forecast_element.find("W").string
                    reykjavik_12h['forecasttime'] = forecast_time
                    #log.info("Temperature Forecast for " + forecast_time + " is " + reykjavik_12h['temperature'] + " degrees")
                    state.set(sensor12h, f"{reykjavik_12h['temperature']}", reykjavik_12h)
                    
                #Repeat...
                #if str(timedelta_hours) in ['18.0']:
                #    #forecast_temperature = forecast_element.find("T").string
                #    reykjavik_18h['temperature'] = forecast_element.find("T").string
                #    reykjavik_18h['wind_speed'] = forecast_element.find("F").string
                #    reykjavik_18h['wind_direction'] = forecast_element.find("D").string
                #    reykjavik_18h['forecast'] = forecast_element.find("W").string
                #    reykjavik_18″h['forecasttime'] = forecast_time
                #    #log.info("Temperature Forecast for " + forecast_time + " is " + reykjavik_18h['temperature'] + " degrees")
                #    state.set(sensor18h, f"{reykjavik_18h['temperature']}", reykjavik_18h)