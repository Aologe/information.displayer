#-*- coding:utf-8 -*-

import requests
import time

class Weather(object):
	def __init__(self):
		#weather part
		#now weather and information from https://console.heweather.com/my/service
		self.APIurlnow = "https://free-api.heweather.com/v5/now?city=anyang&key=22c62344cac143eb8570c35904ea55bb"
		#3 days forecast weahter URL
		self.APIurlforeshort = "https://free-api.heweather.com/v5/forecast?city=anyang&key=22c62344cac143eb8570c35904ea55bb"
		#5 days forecast weather URL
		self.APIurlforelong = "http://wthrcdn.etouch.cn/weather_mini?citykey=101180201"
		#AQI data
		self.APIurlaqi = "https://free-api.heweather.com/v5/aqi?city=anyang&key=22c62344cac143eb8570c35904ea55bb"

		#the date and time
		self.temp_time = list(time.localtime(time.time()))
		self.year = self.temp_time[0]
		self.mon = self.temp_time[1]
		self.day = self.temp_time[2]
		self.day_of_year = self.temp_time[7]

		#common information city
		apinow = requests.get(self.APIurlnow)
		now = apinow.json()
		comm_city = now['HeWeather5'][0]['basic']
		self.city = comm_city['city']
		self.city_lat = comm_city['lat']
		self.city_lon = comm_city['lon']
		self.city_loc = comm_city['update']['loc']

		#common information wind
		# 1 km/h == 0.277778 m/s 
		self.PER = 0.277778
		self.wind_fore = [0.0,0.2,1.5,3.3,5.4,7.9,10.7,13.8,17.1,20.7,24.4,28.4,32.6]
		self.wind_fore_level = ['无风','软风','轻风','微风','和风','轻劲风','强风',
		'疾风','大风','烈风','狂风','暴风','台风']

class WeatherNow(Weather):
	def __init__(self):
		super().__init__()

		self.apinow = None
		self.now = None
		self.result = None

	def getWeather(self):
		self.apinow = requests.get(self.APIurlnow)
		if self.apinow.status_code != 200:
			self.result = "the page has some problems"
			return self.result
		else:
			self.now = self.apinow.json()

		if self.now['HeWeather5'][0]['status'] != 'ok':
			self.result = self.now['HeWeather5'][0]['status']
			return self.result

		comm_now = self.now['HeWeather5'][0]['now']
		#condition
		now_cond = comm_now['cond']['txt']

		#somatosensory (℃)
		now_soma = comm_now['fl']
		now_hum = comm_now['hum']
		#precipitation (mm)
		now_pcpn = comm_now['pcpn']
		now_tmp = comm_now['tmp']
		#view (km)
		now_vis = comm_now['vis']
		now_wind_dir = comm_now['wind']['dir']
		#speed (mph)
		now_wind_spd = float(comm_now['wind']['spd']) * self.PER
		for i in list(range(13))[::-1]:
			if now_wind_spd >= self.wind_fore[i]:
				break
		now_wind_level = self.wind_fore_level[i]

		result = ("城市: " + self.city + "{feed}" + "经度: " + self.city_lon[:self.city_lon.find('.')+3]
			+ " 纬度: " + self.city_lat[:self.city_lat.find('.')+3] + "{feed}" + "更新时间: " + self.city_loc
			+ "{feed}" + "天气: " + now_cond + " 体感温度: " + now_soma + "℃{feed}" +"实时温度: " + now_tmp 
			+ "℃ 降水量: " + now_pcpn + "mm{feed}" + "湿度: " + now_hum + "% 能见度: " + now_vis + "km{feed}"
			+ "风向: " + now_wind_dir + " 风力等级: " + now_wind_level + "{feed}" + "风速: "
			+ str(now_wind_spd)[:str(now_wind_spd).find('.')+3] + "m/s")
		return result

class WeatherDay(Weather):
	def __init__(self):
		super().__init__()

	def getWeather(self):
		short = requests.get(self.APIurlforeshort).json()
		forecast = list()
		for i in range(3):
			temp = [
			short['HeWeather5'][0]['daily_forecast'][i]['date'], #0 日期
			short['HeWeather5'][0]['daily_forecast'][i]['astro']['mr'], #1 月升
			short['HeWeather5'][0]['daily_forecast'][i]['astro']['ms'], #2 月落
			short['HeWeather5'][0]['daily_forecast'][i]['astro']['sr'], #3 日升
			short['HeWeather5'][0]['daily_forecast'][i]['astro']['ss'], #4 日落
			short['HeWeather5'][0]['daily_forecast'][i]['cond']['code_d'], #5 白天天气代码
			short['HeWeather5'][0]['daily_forecast'][i]['cond']['code_n'], #6 黑夜天气代码
			short['HeWeather5'][0]['daily_forecast'][i]['cond']['txt_d'], #7 白天天气
			short['HeWeather5'][0]['daily_forecast'][i]['cond']['txt_n'], #8 黑夜天气
			short['HeWeather5'][0]['daily_forecast'][i]['hum'], #9 湿度
			short['HeWeather5'][0]['daily_forecast'][i]['pcpn'], #10 降水量
			short['HeWeather5'][0]['daily_forecast'][i]['pres'], #11 气压
			short['HeWeather5'][0]['daily_forecast'][i]['tmp']['max'], #12 最高温度
			short['HeWeather5'][0]['daily_forecast'][i]['tmp']['min'], #13 最低温度
			short['HeWeather5'][0]['daily_forecast'][i]['vis'], #14 能见度
			short['HeWeather5'][0]['daily_forecast'][i]['wind']['dir'], #15 风向
			short['HeWeather5'][0]['daily_forecast'][i]['wind']['sc'], #16 风力等级
			short['HeWeather5'][0]['daily_forecast'][i]['wind']['spd']] #17 风速
			forecast.append(temp)

		#flong = 
		return forecast

