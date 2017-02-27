
from audioPickleClass import audioPickleClass
from classifyingClass import ClassifyingClass
import numpy as np
import pickle
#'''
#APC = audioPickleClass()
#print(APC.getListAudioFileWithLabels())
#APC.addLabels()
#PC.shuffle()
#APC.createPickle("test")
#'''

#'''
CC = ClassifyingClass()

data = pickle.load( open( "./test.pickle", "rb" ) )




for i in range(0,10):
	print("/n")
	print(len(data["mfcc"][i][0][0]))
	print(len(data["mfcc"][i][0]))
	print(len(data["mfcc"][i]))

'''
final = []
for dataPoint in data["mfcc"]:
	asdf = []
	print(len(dataPoint))
	for i in dataPoint:
		asdf.extend((x for sublist in i for x in sublist))
	
	final.append(asdf)
	break;
		

print(len(final))
print(len(final[0]))
print(final[0])
#CC.setData(final, data["target"])
#CC.one_class_svm()
#CC.cross_val()
#'''
