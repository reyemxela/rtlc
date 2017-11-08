#!/bin/bash

clear

watchfolder="/Users/video/Documents/__Video projects/_SundayService/Exports/"
donefolder="_Done/"

cd "$watchfolder" || exit

echo -n "Title: " && read title
echo -n "Description: " && read description
echo -n "Filename: " && read filename
echo -e "\n\n----------------------\n\nWatching for $filename..."

while true; do
  if [ -s "$filename" ]; then
  	echo -e "\n-----Video Found:-----"
  	ls
  	sleep 600
  	echo "\n-----After waiting:-----"
  	ls
    youtube-upload --title="$title" --description="$description" --privacy="unlisted" "$filename" && \
    mv "$filename" $donefolder
    break
  else
    sleep 10
  fi
done
