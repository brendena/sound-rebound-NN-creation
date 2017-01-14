import librosa
import matplotlib.pyplot as plt
import pickle
#need to pickle the data with as pumpy object
import numpy as np
import pandas as pd
import random
import sys

limit = 100

# 0 means crying 1 mean not crying
y0, sr0 = librosa.core.load("./babyCrying.wav",44100, duration=limit)
y1, sr1 = librosa.core.load("./babylaughing.wav",44100, duration=limit)

junk = {
	'mfcc' : [],
	'mel': [],
	'data': [],
	'target': []
}

'''
set the file name and
stops the program if it is not set
'''
FilePickle = ""
try:
    if(len(sys.argv) >= 2):
        FilePickle = sys.argv[1]
    else:
        raise
except : 
    print("Please specifiy the file name")
    sys.exit(2)



for x in range(0, int(limit)):
    print(x);
    ySample = y0[x*sr0: (x+1)*sr0]
    mfccs = librosa.feature.mfcc(y=ySample, sr=sr0)
    melSpec = librosa.feature.melspectrogram(y=ySample, sr=sr0)

    ySample1 = y1[x*sr1: (x+1)*sr1]
    mfccs1 = librosa.feature.mfcc(y=ySample1, sr=sr1)
    melSpec1 = librosa.feature.melspectrogram(y=ySample1, sr=sr1)

    junk['data'].append(ySample)
    junk['mel'].append(melSpec)
    junk['mfcc'].append(mfccs)
    junk['target'].append(0);

    junk['data'].append(ySample1)
    junk['mel'].append(melSpec1)
    junk['mfcc'].append(mfccs1)
    junk['target'].append(1);


#for x in range(0, int(limit)):
#	print(x);
#	ySample = y1[x*sr1: (x+1)*sr1]
#	mfccs = librosa.feature.mfcc(y=ySample, sr=sr0)
#	melSpec = librosa.feature.melspectrogram(y=ySample, sr=sr0)
#	junk['data'].append(ySample)
#	junk['mel'].append(melSpec)
#	junk['mfcc'].append(mfccs)
#	junk['target'].append(1);



    
junk2 = {
    'mfcc'   : pd.Series(junk['mfcc']),
    'target' : pd.Series(junk['target'])
}

dataframe = pd.DataFrame({
        'mfcc'   : junk2['mfcc'],
        'target' : junk2['target']
    })


print("making pickle \n")

pickle.dump(dataframe, open(FilePickle + ".pickle", "wb"))

