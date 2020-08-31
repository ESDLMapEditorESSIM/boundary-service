# BoundaryService

This service is a helper service for the ESDL mapeditor and gives boundary information
for provinces, municipalities, neighbourhoods, and so on.

If you've updated this code, recreated your docker container image, change the docker-compose yaml file from
the docker-toolsuite project to link to the local container image and start the stack using `docker-compose up -d`

## Create local docker container image

```
docker build -t boundary-service:latest .
```

## Adding shapefile to postgis database

The BaseInfrastructure docker-compose file loads all shapefiles into the postgres database. However, if you
want to use other shapefiles, you'll find example commands below to update your boundary information.

Example

```
shp2pgsql -s 4326 prov_obv_gem_2018_land_wgs.shp public.prov_2018_wgs | psql -h localhost -d boundaries -U postgres
shp2pgsql -s 4326 buurt_2018_wgs.shp public.buurt_2018_wgs | psql -h localhost -d boundaries -U postgres
```

## License

