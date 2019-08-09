#!/usr/bin/env bash
psql -f docker-entrypoint-initdb.d/create_database
psql -d smart_house -f docker-entrypoint-initdb.d/dump