
from audioPickleClass import audioPickleClass
from classifyingClass import ClassifyingClass
import numpy as np
import pickle
#'''
APC = audioPickleClass()
#print(APC.getListAudioFileWithLabels())
APC.addLabels()
#PC.shuffle()
APC.createPickle("test")
#'''

#'''
CC = ClassifyingClass()

data = data = pickle.load( open( "./test.pickle", "rb" ) )


final = []
for dataPoint in data["mfcc"]:
    final.append([x for sublist in dataPoint for x in sublist])

CC.setData(final, data["target"])
CC.cross_val()
#'''
