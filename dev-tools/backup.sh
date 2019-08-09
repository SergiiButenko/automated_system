#!/usr/bin/env bash
sudo docker exec -t postgres pg_dumpall --database smart_house -c --if-exists -x -O -U postgres > ./create_database.sql
sudo docker exec -t postgres pg_dumpall --database smart_house -s -a --column-inserts -U postgres > ./dump.sql
