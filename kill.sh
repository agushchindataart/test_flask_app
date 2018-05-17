#! /bin/bash

for pid in $(ps -ef | grep aggregated_service/env/bin/python | grep -v grep | awk '{print $2}'); do
    kill -9 $pid;
done
