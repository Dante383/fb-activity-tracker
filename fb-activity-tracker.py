#!/usr/bin/python

# Facebook Activity Tracker 
# made by Dante383
# github.com/Dante383/fb-activity-tracker

# USAGE: python fb-activity-tracker.py
#	[--config=<path to a config file>]
#	[--env=<dev or prod>]
#	[--user=<account email>]
#	[--password=<account password>]
#
# CLI variables have bigger priority than the config file

import logging, argparse, yaml, sys
import TrackerClient

class ActivityTracker:

	defaultConfig = {
		'env': 'dev',
		'db': 'updates.db'
	}

	clients = []


	def __init__ (self):
		parser = argparse.ArgumentParser()
		parser.add_argument('--env', type=str, default='dev', help='prod or dev')
		parser.add_argument('--config', type=str, default='config.yaml', help='Config file path')
		parser.add_argument('--db', type=str, default='updates.db', help='Database file')
		parser.add_argument('--user', type=str, help='User email (optional)')
		parser.add_argument('--password', type=str, help='User password (optional)')
		args = vars(parser.parse_args())

		logging.basicConfig(format="%(asctime)s %(message)s")
		self.logger = logging.getLogger('fb-activity-tracker')

		self.config = self.parseConfig(args)

		if (self.config['env'] == 'dev'):
			self.logger.setLevel('DEBUG')
		else:
			self.logger.setLevel('CRITICAL');

		if (not 'accounts' in self.config):
			self.logger.error('No accounts found!')
			self.exit(1)

		for account in self.config['accounts']: 
			client = TrackerClient.TrackerClient(account, self.logger, self.config)
			client.listen()
			self.clients.append(client)


	def parseConfig (self, args):
		
		# is config set?
		if (args['config']):
			stream = False

			try:
				stream = open(args['config'], 'r')
			except FileNotFoundError:
				self.logger.warning('Config not found! Using default variables')
				config = self.defaultConfig
				pass

			if (stream != False):
				config = yaml.load(stream)

		else:
			config = self.defaultConfig

		# but, if we have --user and --password, we will want to set it as accounts[0]
		if (not 'accounts' in config):
			if (args['user']):
				# no password? lets ask for it interactively 
				if (not args['password']):
					args['password'] = input('Password for ' + args['user'] + ':')

				# okay, but its not going to work like this. 
				config['accounts'] = [{'username': args['user'], 'password': args['password']}]
				del args['user'], args['password']


		del args['config']

		# merge config and our command line arguments
		config = {**config, **args}
		return config


	def exit (self, status=0):
		self.logger.info('Exitting...')
		sys.exit(status)
	

if (__name__ == '__main__'):
	ActivityTracker()