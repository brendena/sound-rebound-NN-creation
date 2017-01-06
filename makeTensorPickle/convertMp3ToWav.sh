#!/bin/bash
#removing extension http://unix.stackexchange.com/questions/180271/remove-a-specific-extension-from-all-the-files-in-a-directory

#this will convert all mp3 into wav and delete the mp3 files

for file in *.mp3; do
    filename="${file%.*}"
    wavextension=".wav"
    filename=$filename$wavextension
    mpg321 -w $filename $file
    chmod 777 fingerSnapping.wav
    rm $file
done
