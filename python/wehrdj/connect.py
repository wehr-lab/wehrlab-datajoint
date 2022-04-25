import datajoint as dj
import json
from pathlib import Path

def connect(host=None, user=None, password=None, file=Path.home()/'.djcredentials.json'):
	file = Path(file)
	if file.exists() and all(field is None for field in [host, user, password]):
		with open(file, 'r') as cfgfile:
			cfg = json.load(cfgfile)
		host = cfg['host']
		user = cfg['user']
		password = cfg['password']
	else:
		if host is None:
			host = input('host ip and port: ')
		if user is None:
			user = input('username: ')
		if password is None:
			password = input('password: ')

		if not file.exists():
			with open(file, 'w') as cfgfile:
				json.dump({'host':host, 'user':user, 'password':password}, cfgfile)

	dj.config['database.host'] = host
	dj.config['database.user'] = user
	dj.config['database.password'] = password

	dj.conn()
