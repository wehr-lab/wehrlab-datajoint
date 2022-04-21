import datajoint as dj
import json

def connect(host=None, user=None, password=None, file=None):
	if file is not None:
		with open(file, 'r') as cfgfile:
			cfg = json.load(cfgfile)
		host = cfg['host']
		user = cfg['user']
		password = cfg['password']
	else:
		if host is None:
			host = input('host ip and port')
		if user is None:
			user = input('username')
		if password is None:
			password = input('password')

	dj.config['database.host'] = host
	dj.config['database.user'] = user
	dj.config['database.password'] = password
