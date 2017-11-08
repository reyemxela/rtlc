#!/bin/bash

clear

echo -n "Filename: " && read filename

echo -n "Title: " && read title
echo -n "Description: " && read description
echo -n "Date of message (format: 2016-04-24): " && read date

basefile=`basename "$filename"`
basedir=`dirname "$filename"`
size=`stat -f%z "$filename"`
duration=`exiftool -t -Duration "$filename" |cut -d ":" -f 2- |cut -d " " -f 1`
url="http://s3.amazonaws.com/RTLCPodcast/Media/$basefile"
currentdate=`date "+%a, %d %b %Y %T %z"`


echo "Uploading mp3..."
cd "$basedir" || exit
aws s3 cp "$basefile" s3://RTLCPodcast/Media/ --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers || exit
echo


cd /tmp || exit

cat <<EOF >podcast.tmp
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
EOF


echo "Downloading old xml feed..."
aws s3 cp s3://RTLCPodcast/itunesfeed.xml itunesfeed.old || exit
echo

sed '/text=\"Christianity\"/ r podcast.tmp' itunesfeed.old > itunesfeed.xml

echo "Uploading new xml feed..."
aws s3 cp itunesfeed.xml s3://RTLCPodcast/ --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers || exit
echo

echo "Done!"
