#!/usr/bin/env bash
# Prática 2 (Aula 8): MySQL em contêiner com volume persistente.
set -e
docker volume create mysql_dados

docker run -d --name mysql-tarefas \
    -e MYSQL_ROOT_PASSWORD=troque-root \
    -e MYSQL_DATABASE=tarefas_db \
    -e MYSQL_USER=app \
    -e MYSQL_PASSWORD=troque-app \
    -v mysql_dados:/var/lib/mysql \
    -p 3307:3306 \
    mysql:9.7

echo "Aguarde a mensagem 'ready for connections':  docker logs mysql-tarefas"
echo "Cliente:  docker exec -it mysql-tarefas mysql -uapp -p tarefas_db   (senha: troque-app)"
