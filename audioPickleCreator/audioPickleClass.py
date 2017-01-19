import librosa
import matplotlib.pyplot as plt
import pickle
from random import shuffle
import numpy as np
import pandas as pd

class audioPickleClass:
	def __init__(self):
		self.pickleFileName = ""
		self.listAudioObject = []
		self.finalAudioObject ={};

	def addMusic(self,audioFile, target):
		limit = 100;
		y0, sr0 = librosa.core.load(audioFile,44100, duration=limit)

		for x in range(0, int(limit)):
			ySample = y0[x*sr0: (x+1)*sr0]
			mfccs = librosa.feature.mfcc(y=ySample, sr=sr0)
			melSpec = librosa.feature.melspectrogram(y=ySample, sr=sr0)
			
			self.listAudioObject.append({
				'mfcc' : mfccs,
				'mel': melSpec,
				'data': ySample,
				'target': target
			})

	def shuffle(self):
		shuffle(self.listAudioObject)

	def createPickle(self, FilePickle):
		tmpArray = {
			'mfcc' : [],
			'mel': [],
			'data': [],
			'target': []
		}
		print("lens of list Audio Object")
		print(len(self.listAudioObject))
		for x in range(0, len(self.listAudioObject)):
			tmp = self.listAudioObject[x]
			tmpArray["mfcc"].append(tmp["mfcc"])
			tmpArray["mel"].append(tmp["mel"])
			tmpArray["data"].append(tmp["data"])
			tmpArray["target"].append(tmp["target"])
		
		junk2 = {		
			'mfcc'   : pd.Series(tmpArray['mfcc']),
    		'target' : pd.Series(tmpArray['target'])
		}

		dataframe = pd.DataFrame({
	        'mfcc'   : junk2['mfcc'],
	        'target' : junk2['target'],
	    })

		pickle.dump(dataframe, open(FilePickle + ".pickle", "wb"))