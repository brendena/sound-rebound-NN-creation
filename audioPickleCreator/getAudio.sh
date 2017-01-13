#!/bin/bash

# doucmentation
# https://github.com/rg3/youtube-dl/blob/master/README.md#readme
#
# tells  it to make wav format
# --audio-format wav 
#
# tells it to remove video
# -x
#
# get the best audio.  Audio 0 is the best
# --audio-quality 0
#
# specifies the name of the file
# -o "audio.%(ext)s" or -o "audio.wave"
# http://askubuntu.com/questions/630134/how-to-specify-a-filename-while-extracting-audio-using-youtube-dl
#
#
#full example
#youtube-dl --audio-format wav -x --audio-quality 0 -o "audio.%(ext)s" https://www.youtube.com/watch?v=lmSmwPsWvII

#array logic
#https://www.cyberciti.biz/faq/finding-bash-shell-array-length-elements/

#There is no such thing multi arrays
#so for each itteration i just times it by 2


address=(
	"fingerSnapping" https://www.youtube.com/watch?v=lmSmwPsWvII
	"babyCrying" https://www.youtube.com/watch?v=qS7nqwGt4-I
	"babyLaughing" https://www.youtube.com/watch?v=j5-6bI3hR2M 
)

length=${#address[@]}
echo $length

for (( i=0; i<$length/2; i++));
do
	echo $i
	index=$i*2
	echo ${address[$index]}
	echo ${address[$index+1]}
	youtube-dl --audio-format wav -x --audio-quality 0 -o "${address[$index]}.%(ext)s" ${address[$index+1]}
done




