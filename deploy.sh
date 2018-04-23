docker-compose down

docker image rm $(docker image ls -f "dangling=true" -q)

docker-compose build

docker-compose up -d
