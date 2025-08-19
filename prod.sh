@echo off

echo Running in PRODUCTION mode...
docker-compose -f docker-compose.yml up --build -d
