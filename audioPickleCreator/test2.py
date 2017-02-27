import librosa


y0, sr0 = librosa.core.load("fingerSnapping.wav",44100, mono=True,duration = 5, offset=10)

asdf = librosa.feature.mfcc(y=y0, sr=sr0,n_mfcc=40)
print(len(asdf))

print(len(asdf[0]))
#print(asdf[0])
print(asdf[1][0:10])


