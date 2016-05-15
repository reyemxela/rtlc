#!/bin/bash

clear

watchfolder="/Users/video/Documents/__Video projects/_SundayService/Exports/"
donefolder="_Done/"

cd "$watchfolder" || exit

echo -n "Title: " && read title
echo -n "Description: " && read description

filename="`ls *.m4v |cut -d '.' -f 1`.mp4"

echo -n "Is this the file? $filename [Y/n]: " && read answer
if [ "$answer" == "n" ]; then
  echo -n "Enter filename:" && read filename
fi
echo -e "\n\n----------------------\n\nWatching for $filename..."

while true; do
  if [ -s "$filename" ]; then
  	sleep 60
    youtube-upload --title="$title" --description="$description" --privacy="unlisted" "$filename" |tee /tmp/output && \
    mv "$filename" $donefolder
    break
  else
    sleep 5
  fi
done

url=`tail -1 /tmp/output`

echo
cat <<EOF
<div class="embed-video">
<iframe id="ytplayer" src="https://www.youtube.com/embed/$url?rel=0&showinfo=0&autohide=1" width="1110" height="624.375" frameborder="0" allowfullscreen></iframe>
</div>
EOF
