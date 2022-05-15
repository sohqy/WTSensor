#!/bin/bash

git config --global user.name "RPi"
git config --global user.email "northshoredeployment@gmail.com"
git config --global core.editor nano

git remote add origin git@github.com:sohqy/WTSensor.git

cd DataFiles
git add --all
git commit -am date+"%Y-%m-d"

git push -u origin master
