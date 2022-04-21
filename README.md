# Wehrlab Datajoint Models


## Running SQL docker

Create an `.env` file in whatever directory you're running this from with
`MYSQL_ROOT_PASSWORD=<some password>`, or else pass it explicitly like 
`-e MYSQL_ROOT_PASSWORD=tutorial` (not recommended since stdin is not encrypted lol)

` docker-compose -f ./wehrlab-datajoint/config/dj_docker.yaml --project-directory ./ up -d
`