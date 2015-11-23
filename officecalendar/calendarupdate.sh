#!/bin/bash
#v3.0
#Eventual size check? ~155k when full
#~22k when completely blank

ROOTDIR="/home/pi"
LOCKFILE="$ROOTDIR/calendars/.lock"

if [ ! -f $LOCKFILE ]; then
touch $LOCKFILE


OUTFILE="$ROOTDIR/calendars/maincalendar.png"

export DISPLAY=:0
cutycapt --min-width=1920 --min-height=1080 --url="file://$ROOTDIR/yearcalendar.htm" --out=$OUTFILE.tmp --out-format=png --delay=30000
#cutycapt --min-width=1920 --min-height=1080 --url=http://sb.codeanywhere.com/~109139/FrontOfficeCalendar/yearcalendar_v2.0b.htm --out=$OUTFILE.tmp --out-format=png --delay=30000

mv $OUTFILE.tmp $OUTFILE



rm $LOCKFILE

fi
