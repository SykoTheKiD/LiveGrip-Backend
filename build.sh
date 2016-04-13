#!/bin/bash
SETTINGS=LiveGrip/LiveGrip/settings.py

while getopts b:l FLAG; do
  case $FLAG in
    b)  
		sed -i "s/'PASSWORD': '1Drizzydrake'/'PASSWORD': ''/g" $SETTINGS
		echo "Changed MySQL Config to | BUILD |"
      ;;
    l)  
		sed -i "s/'PASSWORD': ''/'PASSWORD': '1Drizzydrake'/g" $SETTINGS
		echo "Changed MySQL Config to | PRODUCTION |"
      ;;
  esac
done