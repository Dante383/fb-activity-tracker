#!/usr/bin/python

# Facebook Activity Tracker 
# made by Dante383
# github.com/Dante383/fb-activity-tracker

import logging, os, sqlite3, time, datetime, json

class TrackerLogger:

	def __init__ (self, file):
		self.file = file
		self.connection = sqlite3.connect(self.file)
		self.connection.execute('''CREATE TABLE IF NOT EXISTS updates 
									(uid int NOT NULL,
									timestamp int NOT NULL,
									active int DEFAULT 1
									);''')
		self.connection.execute('''CREATE TABLE IF NOT EXISTS user_info
									(id int PRIMARY KEY,
									info TEXT NOT NULL
									)''')

	def log (self, change):
		for user, timestamp in change: 
			if (time.time() - int(timestamp) < 60):
				self.connection.execute("INSERT INTO updates VALUES ('{}', '{}', 1)".format(user, timestamp))
			else: 
				self.connection.execute("INSERT INTO updates VALUES ('{}', '{}', 0)".format(user, int(time.time())))
			self.connection.commit()

	def userdata (self, userdata):

		userId = userdata.uid
		userData = json.dumps({
			"affinity": userdata.affinity,
			"name": userdata.name, 
			"gender": userdata.gender,
			"photo": userdata.photo,
			"is_friend": userdata.is_friend,
			"last_message_timestamp": userdata.last_message_timestamp,
			"url": userdata.url
		})

		try:
			self.connection.execute("UPDATE user_info SET info = '{}' WHERE id = {}".format(userData, userId))
			self.connection.commit()
		except:
			self.connection.execute("INSERT INTO user_info (id, info) VALUES ({}, '{}')".format(userId, userData))
			self.connection.commit()
			pass