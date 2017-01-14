import numpy as np

import pickle


def to1hot(row):
    one_hot = np.zeros(2)
    one_hot[row]=1.0
    return one_hot







class MusicData:
	def __init__(self):

		data = pickle.load( open( "./audioForNeuralNetwork.pickle", "rb" ) )

		data["one_hot_encoding"] = data.target.apply(to1hot)

		data["mfcc_flatten"] = data.mfcc.apply(lambda mfcc: mfcc.flatten())




		train_data = data[0:160]
		test_data = data[160:]

		X = np.vstack(train_data.mfcc_flatten).reshape(train_data.shape[0],20, 87).astype(np.float32)
		Y = np.vstack(train_data["one_hot_encoding"])

		testX = np.vstack(test_data.mfcc_flatten).reshape(test_data.shape[0],20, 87).astype(np.float32)
		testY = np.vstack(test_data["one_hot_encoding"])




		self.X = X
		self.Y = Y
		self.testX = testX
		self.testY = testY
		self.myShape = [None, 20, 87] 


