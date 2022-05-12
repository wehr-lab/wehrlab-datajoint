import datajoint as dj
import json
from pathlib import Path
import typing
if typing.TYPE_CHECKING:
    from datajoint.connection import Connection


def connect(host=None, user=None, password=None,
            file=Path.home()/'.djcredentials.json', **kwargs) -> 'Connection':
    """
    Connect to datajoint database.

    Wrapper around :func:`datajoint.conn`, but loads credentials from an (unencrypted) file.

    A bit less implicit than using environment variables, and less manual than typing them
    in every time.

    Please for the love of god do not commit any passwords to a git repo ever.

    Args:
        host (str): IP Address
        user (str): Username ( typically "root" by default )
        password (str): uh Password
        file (:class:`pathlib.Path`): file to load/save credentials to
        **kwargs: passed to dj.conn

    Returns:
        :class:`datajoint.connection.Connection`
    """

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
                json.dump({'host': host, 'user': user, 'password': password}, cfgfile)

    dj.config['database.host'] = host
    dj.config['database.user'] = user
    dj.config['database.password'] = password

    return dj.conn(**kwargs)
