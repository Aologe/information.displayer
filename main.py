#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-03 17:47:15
# @Author  : The carver (aologe@qq.com)
# @Link    : 
# @Version : 0.0.0

import os, sys, time, json
from PyQt5.QtWidgets import (QApplication, QWidget,
	QLabel, QFrame, QPushButton, QStatusBar, 
	QHBoxLayout, QVBoxLayout, QLineEdit)
from PyQt5.QtGui import QFont, QPalette, QPixmap, QBrush, QIcon, QFontDatabase
from PyQt5.QtCore import QPoint, QSize, Qt, QCoreApplication, QBasicTimer

VERSION = "0.0.0"
UNIT = 1000
MINSUNIT = 900
WEEK = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
SCHEDULE = {
	"星期一":{"forenoon": ["英语"], "afternoon": ["程序"]},
	"星期二":{"forenoon": ["概率论", "体育"], "afternoon": ["接口"]},
	"星期三":{"forenoon": ["数据结构"], "afternoon": ["英语"]},
	"星期四":{"forenoon": ["概率论", "导论"], "afternoon": ["接口"]},
	"星期五":{"forenoon": ["数据结构"], "afternoon": []},
	"星期六":{"forenoon": [], "afternoon": []},
	"星期日":{"forenoon": [], "afternoon": []},
}

class MyButton(QPushButton):
	def __init__(self, path, father=None):  #path is a list
		super().__init__(father)

		self.path = tuple(path)
		self.setFocusPolicy(Qt.NoFocus)
		self.setStyleSheet("QPushButton {background-color: transparent}")
		self.setIcon(QIcon(QPixmap(self.path[0])))
		self.setFlat(True)

	def enterEvent(self, *args, **kwargs):
		self.setIcon(QIcon(QPixmap(self.path[1])))

	def leaveEvent(self, *args, **kwargs):
		self.setIcon(QIcon(QPixmap(self.path[0])))

class myLine(QFrame):
	def __init__(self, type=QFrame.Sunken, dire=QFrame.HLine, father=None):
		super().__init__(father)

		self.setFrameShape(dire)
		self.setFrameShadow(type)

class myFont(object):
	def __init__(self, path, size):
		fontID = QFontDatabase.addApplicationFont(path)
		tempfont = QFontDatabase.applicationFontFamilies(fontID)[0]
		self.font = QFont(tempfont)
		self.font.setPointSize(size)

class Example(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		self.flush = 1 #初始化基本图像刷新值，由于首次启动程序背景图像从0开始，所以确保更新为下一张，从而直接从1开始
		with open("./weather.txt", 'r') as f:
			self.weather = json.loads(f.read())['day']
			self.todaycode = self.weather[0][5]
			self.todaymax = self.weather[0][12]
			self.todaymin = self.weather[0][13]
			self.tomorrowcode = self.weather[1][5]
			self.tomorrowmax = self.weather[1][12]
			self.tomorrowmin = self.weather[1][13]

		self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口标记，使其解除标题栏

		self.palette = QPalette()
		self.palette.setBrush(QPalette.Background, QBrush(QPixmap("./icon/background/0.jpg")))
		self.setAutoFillBackground(True)  # 设置自动填充满背景图
		self.setPalette(self.palette)

		hox = QHBoxLayout()
		wordhox = QHBoxLayout()
		imagehox = QHBoxLayout()
		vox = QVBoxLayout()

		self.btnclose = MyButton(["./icon/close.png", "./icon/close.png"])

		cfont = myFont("./font/ariblk.ttf", 28)
		self.lbltime = QLabel(self)
		self.lbltime.setFont(cfont.font)
		self.lbltime.setGeometry(35, 195, 161, 61)
		self.lbltime.setStyleSheet("QLabel {color: white}")

		#cfont = myFont("./font/simhei.ttf", 16)
		self.lbldate = QLabel(self)
		self.lbldate.setFont(QFont("黑体", 18))
		self.lbldate.setGeometry(10, 240, 210, 41)
		self.lbldate.setStyleSheet("QLabel {color: white}")

		self.lblwordl = QLabel(self)
		self.lblwordl.setFont(QFont("黑体", 16))
		self.lblwordl.setMaximumSize(180, 21)
		self.lblwordl.setMinimumSize(180, 21)
		self.lblwordl.setStyleSheet("QLabel {color: white}")

		self.lblwordr = QLabel(self)
		self.lblwordr.setFont(QFont("黑体", 16))
		self.lblwordl.setMaximumSize(180, 21)
		self.lblwordl.setMinimumSize(180, 21)
		self.lblwordr.setStyleSheet("QLabel {color: white; text-align: right;}")

		self.imagel = QLabel(self)
		self.imagel.setPixmap(QPixmap("./icon/weather/" + self.todaycode + ".png").scaled(50, 50))
		self.imager = QLabel(self)
		self.imager.setPixmap(QPixmap("./icon/weather/" + self.tomorrowcode + ".png").scaled(50, 50))
		#self.imagel.setMinimumSize(100, 100)
		#self.imager.setMinimumSize(100, 100)
		self.imagel.setGeometry(290, 200, 50, 50)
		self.imager.setGeometry(410, 200, 50, 50)

		self.lblweatherl = QLabel(self)
		self.lblweatherl.setFont(QFont("黑体", 16))
		self.lblweatherl.setGeometry(265, 235, 160, 61)
		self.lblweatherl.setStyleSheet("QLabel {color: white}")

		self.lblweatherr = QLabel(self)
		self.lblweatherr.setFont(QFont("黑体", 16))
		self.lblweatherr.setGeometry(380, 235, 160, 61)
		self.lblweatherr.setStyleSheet("QLabel {color: white}")

		self.lblweatherl.setText(self.todaymax + "℃~" + self.todaymin + '℃')
		self.lblweatherr.setText(self.tomorrowmax + "℃~" + self.tomorrowmin + '℃')

		self.timer = QBasicTimer()
		self.timer.start(UNIT, self)

		hox.addStretch(1)
		hox.addWidget(self.btnclose)
		wordhox.addWidget(self.lblwordl)
		wordhox.addStretch(1)
		wordhox.addWidget(self.lblwordr)
		vox.addLayout(hox)
		vox.addStretch(1)
		vox.addLayout(wordhox)

		self.btnclose.clicked.connect(self.close)

		self.setLayout(vox)
		self.setMinimumSize(480, 320)
		self.setMaximumSize(480, 320)
		self.move(0, 0)
		self.show()
		#self.showFullScreen()

	def timerEvent(self, *args, **kwargs):
		self.flush += 1

		if self.flush % MINSUNIT == 0:
			n = int(self.flush / MINSUNIT)
			self.palette.setBrush(QPalette.Background, QBrush(QPixmap("./icon/background/" + str(n) + ".jpg")))
			self.setPalette(self.palette)

			if n == len(os.listdir("./icon/background"))-1:
				self.flush = 0

			with open("./weather.txt", 'r') as f:
				self.weather = json.loads(f.read())['day']
				self.todaycode = self.weather[0][5]
				self.todaymax = self.weather[0][12]
				self.todaymin = self.weather[0][13]
				self.tomorrowcode = self.weather[1][5]
				self.tomorrowmax = self.weather[1][12]
				self.tomorrowmin = self.weather[1][13]

			self.lblweatherl.setText(self.todaymax + "℃~" + self.todaymin + '℃')
			self.lblweatherr.setText(self.tomorrowmax + "℃~" + self.tomorrowmin + '℃')

		localtime = list(time.localtime(time.time()))
		mon = localtime[1]
		day = localtime[2]
		hour = localtime[3]
		mins = localtime[4]
		sec = localtime[5]
		wday = localtime[6]

		forenoon = SCHEDULE[WEEK[wday]]["forenoon"]
		afternoon = SCHEDULE[WEEK[wday]]["afternoon"]

		forestr = str()
		for i in forenoon:
			forestr += (i + ' ')
		afterstr = str()
		for i in afternoon:
			afterstr += (i + ' ')

		self.lbltime.setText("%02d:%02d" % (hour, mins))
		self.lbldate.setText("%d月%d日, %s" % (mon, day, WEEK[wday]))
		self.lblwordl.setText(forestr)
		self.lblwordr.setText(afterstr)

if __name__ == '__main__':

	app = QApplication(sys.argv)
	app.setOverrideCursor(Qt.BlankCursor)  #when you put your cursor over the app,hide your cursor
	ex = Example()
	sys.exit(app.exec_())
