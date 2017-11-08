#!/bin/bash

clear

uploadingaudio=false
uploadingvideo=false

videowatchfolder="/Users/video/Documents/__Video projects/_SundayService/Exports/"
videodonefolder="$videowatchfolder/_Done/"
audiowatchfolder="/Users/video/Documents/__Audio projects/_Podcast/_Exports"
audiodonefolder="$audiowatchfolder/_Archive/"

#cd "$videowatchfolder" || exit

echo -n "Title: " && read title
echo -n "Description: " && read description
echo -n "Date of message (format: 2016-04-24): " && read date

videofilename="$date.mp4"
audiofilename="$date.mp3"

#videofilename="`ls \"$videowatchfolder\"/*.m4v |cut -d '.' -f 1`.mp4"
#audiofilename="`ls \"$audiowatchfolder\"/*.mp3`"

#echo -n "Is this the video file? $videofilename [Y/n]: " && read answer
# if [ "$answer" == "n" ]; then
#   echo -n "Enter filename:" && read videofilename
# fi
#
# echo -n "Is this the audio file? $audiofilename [Y/n]: " && read answer
# if [ "$answer" == "n" ]; then
#   echo -n "Enter filename:" && read audiofilename
# fi

videofullpath="$videowatchfolder/$videofilename"
audiofullpath="$audiowatchfolder/$audiofilename"

function uploadaudio() {
  sleep 1200
  size=`stat -f%z "$audiofullpath"`
  duration=`exiftool -t -Duration "$audiofullpath" |cut -d ":" -f 2- |cut -d " " -f 1`
  url="http://s3.amazonaws.com/RTLCPodcast/Media/$audiofilename"
  currentdate=`date "+%a, %d %b %Y %T %z"`
  echo "-- Uploading MP3 --"
  aws s3 cp "$audiofullpath" s3://RTLCPodcast/Media/ --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers
  mv "$audiofullpath" "$audiodonefolder"
  echo
  cd /tmp || exit

  cat <<EOF1 >podcast.tmp
<item>
  <title>$title</title>
  <itunes:subtitle>$date Sun</itunes:subtitle>
  <itunes:summary><![CDATA[ $description ]]></itunes:summary>
  <description>$date Sun</description>
  <link>$url</link>
  <enclosure url="$url" length="$size" type="audio/mpeg"/>
  <guid>$url</guid>
  <itunes:duration>$duration</itunes:duration>
  <author>info@roadtolifechurch.com (Pastor Mike Schoeplein)</author>
  <itunes:author>Pastor Mike Schoeplein</itunes:author>
  <itunes:explicit>no</itunes:explicit>
  <pubDate>$currentdate</pubDate>
</item>
EOF1

  echo "Downloading old xml feed..."
  aws s3 cp s3://RTLCPodcast/itunesfeed.xml itunesfeed.old || exit
  echo

  sed '/text=\"Christianity\"/ r podcast.tmp' itunesfeed.old > itunesfeed.xml

  echo "Uploading new xml feed..."
  aws s3 cp itunesfeed.xml s3://RTLCPodcast/ --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers || exit
  echo

  echo "Done!"
  echo "MP3 URL: $url"
  echo
}

function uploadvideo() {
  sleep 600
  echo "-- Uploading video --"
  youtube-upload --title="$title" --description="$description" --privacy="unlisted" "$videofullpath" |tee /tmp/videooutput && \
  mv "$videofullpath" "$videodonefolder"

  videourl=`tail -1 /tmp/videooutput`
  echo

  cat <<EOF2
Video embed code:

<div class="embed-video">
<iframe id="ytplayer" src="https://www.youtube.com/embed/$videourl?rel=0&showinfo=0&autohide=1" width="1110" height="624.375" frameborder="0" allowfullscreen></iframe>
</div>

EOF2
}


echo -e "\n\n----------------------\n\nWatching for files..."

while true; do
  if [ -s "$audiofullpath" ] && [ $uploadingaudio == false ]; then
      uploadingaudio=true
      uploadaudio &
  fi

  if [ -s "$videofullpath" ] && [ $uploadingvideo == false ]; then
      uploadingvideo=true
      uploadvideo &
  fi
  
  if [ $uploadingvideo == true ] && [ $uploadingaudio == true ]; then
    break
  else
    sleep 10
  fi
done
