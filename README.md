# Wehrlab Datajoint Models


## Running SQL docker

Create an `.env` file in whatever directory you're running this from with
`MYSQL_ROOT_PASSWORD=<some password>`, or else pass it explicitly like 
`-e MYSQL_ROOT_PASSWORD=tutorial` (not recommended since stdin is not encrypted lol)

` docker-compose -f ./wehrlab-datajoint/config/dj_docker.yaml --project-directory ./ up -d
`

## Python

### Connect to database

Use the `wehrdj.connect.connect()` function to open a database connection. It will prompt you for 
connection information when first run, and then will stash those credentials in `~/.djcredentials.json`

```python
>>> from wehrdj import connect
>>> connect()
host ip and port: 127.0.0.1:3307
username: root
password: <password>
Connecting root@127.0.0.1:3307
>>> 
```

### Activate schema

This part is in flux. Now we need to register all the schema objects that we'll use.
For now, this is done with `wehrdj.elements.activate`, but as we make our own schema
we'll have to adapt this to include the rest of our own.

```python
from wehrdj.elements import activate
activate()
```

# Reference

## workflow-session

Examples of ingesting data and basic usage of session information

* https://github.com/datajoint/workflow-session/blob/main/notebooks/1_Explore_Workflow.ipynb
* https://github.com/datajoint/workflow-session/blob/main/workflow_session/ingest.py
