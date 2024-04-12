#!/bin/bash

platform=''

while getopts 'p:' flag; do
  case "${flag}" in
    p) platform="${OPTARG}" ;;
    *) exit 1 ;;
  esac
done

mkdir -p art

if [ $platform = "macos-latest" ]; then
  tar -czf art/LiveBeatMonitor.tar.gz dist/LiveBeatMonitor.app
fi

if [ $platform = "windows-latest" ]; then
  zip -r art/LiveBeatMonitor.zip dist
fi

if [ $platform = "ubuntu-latest" ]; then
  tar -czf art/LiveBeatMonitor.tar.gz dist
fi