#!/usr/bin/python
# -*- coding: utf-8 -*-


import argparse, os, sqlite3, json, datetime, time, webbrowser, sys
from jinja2 import Environment, PackageLoader, select_autoescape

class ReportGenerator:
	def generateUserReport (self, userId):
		print('--- Generating report for user {} ---'.format(userId))

		print('Querying database..')

		# first, lets check if there is a userdata in database for this user ID
		self.cursor.execute('SELECT * FROM user_info WHERE id = {}'.format(userId))
		userData = self.cursor.fetchone()

		if (not userData):
			print('User data for this ID not found!')
		else: 
			userData = json.loads(str(userData[1]))
			print('User: {}'.format(userData['name']))

		# now, lets query the last-active times for this user
		self.cursor.execute('SELECT * FROM updates WHERE uid = {}'.format(userId))
		updates = self.cursor.fetchall()
		processed_updates = []

		for update in updates:
			processed_updates.append([update[1], update[2]])

		processed_updates = json.dumps(processed_updates)

		if (not updates):
			print('No data found for this ID!')
		else: 
			filename = 'reports/report {}.html'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
			template = self.env.get_template('user.html').stream(userdata=userData, updates=processed_updates).dump(filename)
			print ('Report generated and saved to {}'.format('reports/report {}.html'.format(filename)))	
			print ('--- Report generated successfuly ---')
			if (not 'do-not-open-browser' in self.args):
				webbrowser.open(filename)

	def generateUsersReport (self, users):
		if (users == 'all'):
			print('--- Generating report for all users (possibly huge output)... ---')
		else:
			users = users.split(',')

		users_data = []

		if (users == 'all'):
			self.cursor.execute('SELECT id FROM user_info WHERE 1')
			users = self.cursor.fetchall()

		for user in users:
			try:
				userId = int(user)
			except:
				userId = int(user[0])
				pass

			print('--- Generating report for user {} ---'.format(userId))

			# first, lets check if there is a userdata in database for this user ID
			self.cursor.execute('SELECT * FROM user_info WHERE id = {}'.format(userId))
			userData = self.cursor.fetchone()

			if (not userData):
				print('Userdata not found!')
			else: 
				userData = json.loads(userData[1])
				print('User: {}'.format(userData['name']))

			# now, lets query the last-active times for this user
			self.cursor.execute('SELECT * FROM updates WHERE uid = {}'.format(userId))
			updates = self.cursor.fetchall()
			processed_updates = []

			for update in updates:
				processed_updates.append([update[1], update[2]])

			processed_updates = json.dumps(processed_updates)

			users_data.append({'userdata': userData, 'updates': processed_updates})

		filename = 'reports/report {}.html'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
		template = self.env.get_template('users.html').stream(users=users_data,users_json=json.dumps(users_data)).dump(filename)
		print ('Report generated and saved to {}'.format('reports/report {}.html'.format(filename)))	
		print ('--- Report generated successfuly ---')
		if (not 'do-not-open-browser' in self.args):
			webbrowser.open(filename)



	def __init__ (self):
		parser = argparse.ArgumentParser()
		parser.add_argument('--db', type=str, default='updates.db', help='Database file path')
		parser.add_argument('--do-not-open-browser')
		parser.add_argument('--user', type=int, help='User ID you want to generate report of')
		parser.add_argument('--users', type=str, help='Users ID you want to generate report of, separated by commas, or "all" (warning: possibly huge report)')
		self.args = vars(parser.parse_args())

		if (not os.path.exists(self.args['db'])):
			print('Error: Database does not exists! Exitting..')
			sys.exit(1)

		if (not os.path.exists('reports')):
			os.mkdir('reports')

		self.connection = sqlite3.connect(self.args['db'])
		self.cursor = self.connection.cursor()

		self.env = Environment(
			loader=PackageLoader('templates', ''),
			autoescape=select_autoescape(['html', 'xml'])
		)

		if (self.args['user']):
			self.generateUserReport(self.args['user'])

		if (self.args['users']):
			self.generateUsersReport(self.args['users'])

if __name__ == '__main__':
	ReportGenerator()