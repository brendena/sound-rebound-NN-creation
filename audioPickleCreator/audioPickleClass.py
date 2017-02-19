import librosa
import pickle
from random import shuffle
import pandas as pd
import os
from os import listdir


class audioPickleClass:

	def __init__(self):
		self.pickleFileName = ""
		self.listAudioObject = []
		self.finalAudioObject = {}

	def getCurrentDirectory(self):
		return os.path.dirname(os.path.abspath(__file__))

	def getListAudioFileWithLabels(self):
		'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		get home directoy and then labels
		directory.  Then grabs all the directores
		from it.
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
		mypath = self.getCurrentDirectory()
		mypath = mypath + "/labels"

		labelsDir = listdir(mypath)
		listFilesDir = listdir(mypath + "/" + labelsDir[2])

		'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		get the files that have a unique file name.
		By file name i mean the file name with
		a extension
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
		uniqueFileName = []

		def append_IfNotIn(value, array):
			a = os.path.splitext(value)[0]

			if(a not in array):
				array.append(a)
		[append_IfNotIn(x, uniqueFileName) for x in listFilesDir]

		'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		Append all the files with both
		a label and a wav files.
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
		audioFilesWithExtensions = []
		for fNameWE in uniqueFileName:
			if(fNameWE + ".txt" in listFilesDir):
				if(fNameWE + ".wav" in listFilesDir):
					audioFilesWithExtensions.append({"dir":labelsDir[2], "fileName":fNameWE })
		return audioFilesWithExtensions

	

	def addMusic(self,audioFile, labelsArray, target):
		limit = 100
		y0, sr0 = librosa.core.load(audioFile,44100, duration=limit)

		numberPointsPerSecond = 2 
		lengthDataPoint = sr0 *(1/numberPointsPerSecond)
		for label in labelsArray:
			if(label[0] < 0):
				start = 0
			else:
				start = round(label[0])
			end = round(label[1])
			for i in range(start, end+1):  
				secondStartingPoint = i*sr0         
				'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
				this splits each second into
				multiple data points.  This is based off
				the amount of numberPointsPerSecond.
				%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
				for section in range(0,numberPointsPerSecond):

					startingPoint = int(secondStartingPoint + (section * lengthDataPoint))
					endingPoint = int(secondStartingPoint + (section * lengthDataPoint + 1))		
					ySample = y0[startingPoint: endingPoint]
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
