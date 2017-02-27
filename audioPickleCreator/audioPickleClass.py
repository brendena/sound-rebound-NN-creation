import librosa
import pickle
from random import shuffle
import pandas as pd
import LabelClass
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
		'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
		#   It works because of
		#	http://stackoverflow.com/questions/5514573/python-error-typeerror-module-object-is-not-callable-for-headfirst-python-co
		'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
		self.labelClass = LabelClass.LabelClass()
		self.labelLocations = self.labelClass._getLabelLocations()


	
	def loadAudioPickledClass(self):
		self.labelLocations = pickle.load( open( "./test.pickle", "rb" ) )


	


	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	#~~~~~~~~~~~~~~~definition~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#	This function allows you to add the types of 
	#   labels you want to add to listAudioObject.  for pickle
	#   latter on.
	'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
	def addLabels(self,labels=[]):
		fileLocationsWithLabels = self.labelClass.getListAudioFileWithLabels()
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
		f.close()
		return splittingPoints

	def addMusic(self,audioFile, labelsArray, target):
		#limit = 100 , duration=limit
		y0, sr0 = librosa.core.load(audioFile,44100, mono=True)#converts to singal to mono
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# number of data points you want per second.
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		numberPointsPerSecond = 1 #50ms
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# samplePerSecond/numberPointsPerSecond
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		lengthDataPoint = sr0 * float(1/numberPointsPerSecond)
		#print("length data points ")
		#print(lengthDataPoint)
		#print(sr0)
		#print(len(y0))
		#print(y0)
		for label in labelsArray:
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			#labels can be less then zero which will break
			# this program.this forces it to be at least zero
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
				mfccs = []
				melSpec = []
				data = []
				zcr = []
				rms = []

				
				for section in range(0,numberPointsPerSecond):
					startingPoint = int(secondStartingPoint + (section * lengthDataPoint))
					endingPoint = int(secondStartingPoint + ((section + 1) * lengthDataPoint))
					ySample = y0[startingPoint: endingPoint]
					data.append(ySample)
					mfccs.append(librosa.feature.mfcc(y=ySample, sr=sr0))
					melSpec.append(librosa.feature.melspectrogram(y=ySample, sr=sr0))
					#zcr.append(self.zero_crossing_rate_BruteForce(ySample))
					#rms.append(self.root_mean_square(ySample))
					
					

				self.listAudioObject.append({
					'mfcc' : mfccs,
					'mel': melSpec,
					'data': data,
					'zcr' : zcr,
					'rms' : rms,
					'target': target
				})
				break

	def zero_crossing_rate_BruteForce(self,wavedata):

		zero_crossings = 0

		for i in range(1, len(wavedata)):

			if ( wavedata[i - 1] <  0 and wavedata[i] >  0 ) or \
				( wavedata[i - 1] >  0 and wavedata[i] <  0 ) or \
				( wavedata[i - 1] != 0 and wavedata[i] == 0):

				zero_crossings += 1

		zero_crossing_rate = zero_crossings / float(len(wavedata) - 1)

		return zero_crossing_rate	

	def root_mean_square(self,wavedata):

		# how many blocks have to be processed?
		num_blocks = 1

		rms_seg = np.sqrt(np.mean(wavedata**2))
			

		return rms_seg
					
	
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

		pickle.dump(tmpArray, open(FilePickle + ".pickle", "wb"))
