#!/bin/bash
#cd /usr/share/figlet/fonts
#toilet -f cosmic "Horus" --rainbow
sudo wall -n Running Program
cd /mnt/c/Users/notes/Documents/Programming/Horus
python alert.py
python driver.py
sudo wall -n dailyStats.txt

#FILES_WATCHING=$(jq ".stats[].filesWatching" dailyStats.json)
#TRADES_ADDED=$(jq ".stats[].filesWatching" dailyStats.json)
#CALLS_MADE=$(jq ".stats[].filesWatching" dailyStats.json)

#echo "Files Watching:\t" $FILES_WATCHING
#echo "Trades Added:\t" $FILES_WATCHING
#echo "Calls Made:\t" $FILES_WATCHING

#python alert.py
#echo $Files_Watching
#echo Trades_Added
#echo Calls_Made
