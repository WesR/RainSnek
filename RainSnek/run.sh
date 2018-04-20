#!/bin/sh

while true; do
  nohup python RainSnek.py >> nohup.out
  sleep 2
  echo "reloading"
done &