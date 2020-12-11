# Vedurspá
MQTT sensor for the icelandic weather forecast.
The sensor pulls information from xmlweather.vedur.is. More information about this API can be found here:
https://www.vedur.is/skjol/vefur/XML-thjonusta-090813.pdf

Available stations can be found here:
https://www.vedur.is/vedur/spar/stadaspar/
By clciking on one of sysmbols you can gather the weather station ID. Similar to: https://www.vedur.is/vedur/spar/stadaspar/#station=422 -> Akureyri

You will need:
1. A python script that reads the xml file and extract the data. In my example I extract the data for the next 6h and 12h weather forecast and push that information to a MQTT topic ("vedurspa.py").
2. Run the Python script from a Shell command ("shell_command.yaml"). Make sure you have all dependencies installed and make sure the script is executable.
3. A defined MQTT sensor ("sensor.yaml")
4. An automation ("automation.yaml") that pulls the information on a regular basis.

When you are all done you can use this sensor to adjust e.g. the floor heat (as I do). More on that later... 
