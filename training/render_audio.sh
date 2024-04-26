#!/bin/bash

startup_shutdown_duration=5
play_duration=60

for source_file in data/**/*.rb ; do
  echo "Rendering $source_file"
  destination_file=${source_file}.wav
  ((sleep $play_duration && echo) | sonic-pi-tool record $PWD/$destination_file) &
  echo "Waiting for recording to start"
  sleep $startup_shutdown_duration
  echo "Evaluating $source_file"
  sonic-pi-tool eval-file $source_file
  echo "Waiting for $play_duration"
  sleep $play_duration
  echo "Stopping"
  sonic-pi-tool stop
  sleep $startup_shutdown_duration
done
