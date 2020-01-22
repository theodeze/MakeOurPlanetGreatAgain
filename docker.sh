#!/usr/bin/env sh
docker build -t makeourplanetgreatagain .
docker run -it -p 8000:8000 --rm --name makeourplanetgreatagain makeourplanetgreatagain