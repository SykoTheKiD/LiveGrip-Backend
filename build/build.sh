#!/bin/bash
SETTINGS=../LiveGrip/app/LiveGrip/settings.py

while getopts bl:d FLAG; do
  case $FLAG in
    b)  
		sed -i "s/'PASSWORD': '1Drizzydrake'/'PASSWORD': ''/g" $SETTINGS
		echo "Changed MySQL Config to | BUILD |"
      ;;
    l)  
		sed -i "s/'PASSWORD': ''/'PASSWORD': '1Drizzydrake'/g" $SETTINGS
		echo "Changed MySQL Config to | PRODUCTION |"
      ;;
    d)
		rm -rf web/
		mkdir web/
		cp ../. web/ -R
      ;;
  esac
done
