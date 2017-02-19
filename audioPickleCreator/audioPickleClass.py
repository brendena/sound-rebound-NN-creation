import librosa
import pickle
from random import shuffle
import pandas as pd
import os
from os import listdir
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
#
#
#
#
#
#
#  Globals
#		- listAudioObject:
#			A audio Object is all the MFCC values,  
#			MelSpectrogram and audio data.
#			Its also the object that will 
#			be pickle for the classificatoin
#			alogrithms.
#		-labelLocations:
#			directly corisponds with the labelLocation.txt
#			its used to turn a directory into 
#			a labelNumber.
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class audioPickleClass:

	def __init__(self):
		self.listAudioObject = []
		self.labelLocations = self._getLabelLocations()

	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	#~~~~~~~~~~~~~~~definition~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#	grabs the elements from labelLocations
	#   and create a dictionary, out of them.
	#   This is usefull because you give this
	#   the parents directory of a audio file
	#   and it will give you a cordisponding
	#   label for it. 
	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	def _getLabelLocations(self):
		labelLocationFile =  "labelLocation.txt"
		f = open(  labelLocationFile, 'r')
		labelLocation = {}
		for line in f:
			seperatedLine  = line.replace("\n", '').split(" ")    
			labelLocation[seperatedLine[0]] = int(seperatedLine[1])
		print(labelLocation)
		f.close()
		return labelLocation 
		 


	def getCurrentDirectory(self):
		return os.path.dirname(os.path.abspath(__file__))


	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	#~~~~~~~~~~~~~~~definition~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#	loop through all file in the labels and is going to
	#   look for all the wave files with a corisponding
	#   label file.
	#	ex.
	#		[
	#			{"dir": "babyCrying",
	#			 "fileName": "babyCrying2" --stripped of file extensions
	#			}
	#		]
	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
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



	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	#~~~~~~~~~~~~~~~definition~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#	This function allows you to add the types of 
	#   labels you want to add to listAudioObject.  for pickle
	#   latter on.
	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	def addLabels(self,labels=[]):
		fileLocationsWithLabels = self.getListAudioFileWithLabels()
		if(len(labels) != 0 ):
			for label in range(len(fileLocationsWithLabels)-1,-1,-1):
				if(fileLocationsWithLabels[i]["dir"] not in self.labelLocations):
					del fileLocationWithLabs[i]


		

		print(fileLocationsWithLabels)
		
		
		for fileLocation in fileLocationsWithLabels:
			splittingPoints = self.getLabelTextData("labels/" + fileLocation["dir"] + "/" + fileLocation["fileName"] + ".txt")
			audioFile = "labels/" + fileLocation["dir"] + "/" + fileLocation["fileName"] + ".wav"
			self.addMusic(audioFile, splittingPoints,self.labelLocations[fileLocation["dir"]])


	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	get the label text data and convert
	it into a list of list like this
	ex.
		[
			[0.11111, 8.0000], - clipping 1
			[20.62311, 45.3434] - clippint 2
		]
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	def getLabelTextData(self,labelText):
		f = open(  labelText, 'r')
		splittingPoints = []

		for line in f:
				#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				#this create a list divided by \t and then
				#converts then to ints by the map(int and
				#then converts it back to a list
				#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				splittingPoints.append( list(map(float, line.split("\t")[0:2] )))
		return splittingPoints

	def addMusic(self,audioFile, labelsArray, target):
		limit = 100
		y0, sr0 = librosa.core.load(audioFile,44100, duration=limit)
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# number of data points you want per second.
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		numberPointsPerSecond = 2 
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# samplePerSecond/numberPointsPerSecond
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		lengthDataPoint = sr0 *(1/numberPointsPerSecond)
		for label in labelsArray:
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			#labels can be less then zero which will break
			# this program.this forces it to be at least zero.
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
