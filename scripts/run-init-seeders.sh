#!/bin/bash
# Change the name of your docker container if you need, by default it is flask-api-boilerplate-backend-1

# Run flask command to seed admin account
docker exec flask-api-boilerplate-backend-1 flask seed:admin