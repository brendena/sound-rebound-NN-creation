from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import numpy as np
from sklearn import datasets
'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ToDo next
    See if i can save the models for RandomForestClassifier random
    the others

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''


'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

voiting link here
http://scikit-learn.org/stable/modules/ensemble.html
http://sebastianraschka.com/Articles/2014_ensemble_classifier.html

fastdtw
https://pypi.python.org/pypi/fastdtw


'''
#/////////////////////////////////////////////////////////
#differnt type of algorithms i can UserWarning
#http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
# i can play with the distance
# dtw page
# https://pypi.python.org/pypi/fastdtw
#/////////////////////////////////////////////////////////

class classifyingClass:
    def __init__(self):
        np.random.seed(123)
        self.clf1 = RandomForestClassifier()
        self.clf1Type = "Random Forest"
        self.clf2 = GaussianNB()
        self.clf2Type = "Naiye Bayes"                                         
        self.clf3 = KNeighborsClassifier(metric=lambda x,y: fastdtw(x, y, dist=euclidean)[0]) #[0] grabs just the distance
        self.clf3Type = "KNN DTW"
        self.eclfSoft = VotingClassifier(estimators=[('rf', self.clf1), ('gnb', self.clf2), ('knn', self.clf3)], voting='soft')
        self.eclSoftType = "soft voting"

    def setData(self, x,y):
        self.X = x
        self.Y = y

    def cross_val(self):
        for clf, label in zip([self.clf1, self.clf2, self.clf3, self.eclfSoft], [self.clf1Type, self.clf2Type, self.clf3Type,"soft voiting"]):
            scores = cross_validation.cross_val_score(clf, self.X, self.Y, cv=5, scoring='accuracy')
            print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

    def predict(self, data, all = False):
        if all == True:
            print(self.clf1.predict(data))
            print(self.clf1Type)
            print(self.clf2.predict(data))
            print(self.clf2Type)
            print(self.clf3.predict(data))
            print(self.clf3Type)
        print(self.eclSoft.predict(data))
        print("soft voting")
