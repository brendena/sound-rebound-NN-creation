import librosa
import pandas as pd

hopLength = (int(44100/8))

types = ['mfcc','mel','zcr','rms']
'''
loops through these
numberFramePerSection
hopLength
'''

#'''
APC = audioPickleClass()
#print(APC.getListAudioFileWithLabels())
APC.addLabels()
#PC.shuffle()
APC.createPickle("test")
#'''




data = pickle.load( open( "./test.pickle", "rb" ) )



#'''
final = []
for dataPoint in data["rms"]:
	asdf = []
	for i in dataPoint:
		#asdf.extend((x for sublist in i for x in sublist))
		asdf.extend((x for x in i))	
	final.append(asdf)

		

print(len(final))
print(len(final[0]))
print(final[0][0])
#'''

#'''
CC = ClassifyingClass()
CC.setData(final, data["target"])
CC.one_class_svm()
CC.cross_val()
#'''
