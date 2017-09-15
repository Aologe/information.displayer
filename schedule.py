# -*- coding:utf-8 -*-

import modules, json

def mydesk():
	now = modules.WeatherNow()
	weanow = now.getWeather()
	day = modules.WeatherDay()
	weaday = day.getWeather()
	with open("/home/pi/Documents/project/display/weather.txt",'w') as f:
		s = "{'now':'%s'" %weanow + ',' + "'day':" + json.dumps(weaday) + '}'
		s = eval(s)
		f.write(json.dumps(s))

if __name__ == "__main__":
	mydesk()
