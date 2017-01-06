#using this example
#https://github.com/tflearn/tflearn/blob/master/examples/images/dnn.py
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tflearn.datasets.mnist as mnist

import pickle
import numpy as np
data = pickle.load( open( "./sentiment_set.pickle", "rb" ) )



X = data[0]
Y = data[1]
testX = data[2]
testY = data[3]

n_nodes_hl1 = 1500
n_nodes_hl2 = 1500
n_nodes_hl3 = 1500

n_classes = 2
batch_size = 20
hm_epochs = 10


input_layer = tflearn.input_data(shape=[None, 1740], name='input')

dense1 = tflearn.fully_connected(input_layer, n_nodes_hl1, activation='tanh',
								regularizer='L2', weight_decay=0.001)



dropout1 = tflearn.dropout(dense1, 0.8)
dense2 = tflearn.fully_connected(dropout1, n_nodes_hl2, activation='tanh',
                                 regularizer='L2', weight_decay=0.001)




dropout2 = tflearn.dropout(dense2, 0.8)
softmax = tflearn.fully_connected(dropout2, n_classes, activation='softmax')



# Regression using SGD with learning rate decay and Top-3 accuracy
sgd = tflearn.SGD(learning_rate=0.1, lr_decay=0.96, decay_step=1000)
top_k = tflearn.metrics.Top_k(3)
net = tflearn.regression(softmax, optimizer=sgd, metric=top_k,
                         loss='categorical_crossentropy')



# Training
model = tflearn.DNN(net, tensorboard_verbose=3)
model.fit(X, Y, n_epoch=20, validation_set=(testX, testY),
			show_metric=True, run_id="dense_model")
