
from audioPickleClass import audioPickleClass

APC = audioPickleClass()


'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   get the label text data and convert
   it into a list of list like this
   ex.
        [
            [0.11111, 8.0000], - clipping 1
            [20.62311, 45.3434] - clippint 2
        ]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
fileLocation = APC.getListAudioFileWithLabels()[0]
labelText = "labels/" + fileLocation["dir"] + "/" + fileLocation["fileName"] + ".txt"
f = open(  labelText, 'r')
splittingPoints = []

for line in f:
	    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		#this create a list divided by \t and then
		#converts then to ints by the map(int and
		#then converts it back to a list
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		splittingPoints.append( list(map(float, line.split("\t")[0:2] )))

audioFile = "labels/" + fileLocation["dir"] + "/" + fileLocation["fileName"] + ".wav"
APC.addMusic(audioFile, splittingPoints,1)



