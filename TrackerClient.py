#!/usr/bin/python

# Facebook Activity Tracker 
# made by Dante383
# github.com/Dante383/fb-activity-tracker

from fbchat import log, Client
from fbchat.models import *

import logging, datetime, time
import TrackerLogger

class TrackerClient:

	def __init__ (self, options, logger, config):
		self.options = options
		self.logger = logger
		self.trackerLogger = TrackerLogger.TrackerLogger(config['db'])
		self.config = config

		# let's try to login into that account
		self.client = Client(self.options['username'], self.options['password'], None, 5, None, logging.CRITICAL)

	# I'm not sure why, but Facebook API sometimes does return a "historical" data (2-3 hours old)

	def onChatTimestamp (self, **kwargs):
		updatedUsers = kwargs['buddylist'].items()
		self.trackerLogger.log(updatedUsers)

		for user, timestamp in updatedUsers:
			userInfo = self.client.fetchUserInfo(user)[user]
			self.trackerLogger.userdata(userInfo)

			if (self.config['env'] == 'dev'): #and time.time() - int(timestamp) < 60): # to save some unneeded requests
				self.logger.info('{}: {} updated: {}'.format(self.options['username'], userInfo.name, datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')))

	def listen (self):
		if (not self.client):
			self.logger.error('%s: FBChat client not detected!', self.options['username'])
			return False

		if (not self.client.isLoggedIn()):
			self.client.login(self.options['username'], self.options['password'])

		# monkey patching. not sure if this is a good idea
		self.client.onChatTimestamp = self.onChatTimestamp

		self.client.listen()
