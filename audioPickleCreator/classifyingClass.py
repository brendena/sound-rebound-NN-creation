from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import OneClassSVM 
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import numpy as np
from sklearn import datasets

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
import itertools
import numpy as np
import matplotlib.pyplot as plt
'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ToDo next
        See if i can save the models for RandomForestClassifier random
        the others

        be able to give a small chunk of the data to knn model.


        eval the modal
    http://scikit-learn.org/stable/modules/model_evaluation.html
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

class ClassifyingClass:
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
            scores = cross_validation.cross_val_score(clf, self.X, self.Y, cv=2)
            print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
            #print(cross_val_score(clf,self.X,self.Y))
            #print(cross_val_score(clf,self.X,self.Y, scoring='wrong_choice'))
            #self.test(clf,label)
        #plt.show()

    def predict(self, data, all = False):
        #cross val predict
        #http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_predict.html
        if all == True:
            print(self.clf1.predict(data))
            print(self.clf1Type)
            print(self.clf2.predict(data))
            print(self.clf2Type)
            print(self.clf3.predict(data))
            print(self.clf3Type)
        print(self.eclSoft.predict(data))
        print("soft voting")

    def test(self,classifier,label):
        kf = cross_validation.KFold(len(self.Y), n_folds=2)
        for train_index, test_index in kf:

            X_train, X_test = self.X[train_index[0]:train_index[-1]], self.X[test_index[0]:test_index[-1]]
            y_train, y_test = self.Y[train_index[0]:train_index[-1]], self.Y[test_index[0]:test_index[-1]]

            classifier.fit(X_train, y_train)
            cf = confusion_matrix(y_test, classifier.predict(X_test))
            alist = ["cryingBaby","laughingBaby"]
            plt.figure()
            self.plot_confusion_matrix(cf,alist,title=label)
            

    def plot_confusion_matrix(self,cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        print(cm)

        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, cm[i, j],
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    ''' 
        ensmble
    '''
    def one_class_svm(self):
        #passdef
        #OneClassSvm
        clf = OneClassSVM()
        
        firstPosition = 0; 
        for i in range(0, len(self.Y)):
            if(self.Y[i] == 2):
                firstPosition = i
                break
        laughingBaby = self.X[0 : firstPosition - 1]
        cryingBaby = self.X[firstPosition + 1 : -1]

        clf.fit(laughingBaby)
        falseValue = 0
        trueValue = 0

  
        outcome = clf.predict(laughingBaby)
        print(outcome[outcome == -1].size)
        print(outcome[outcome == 1].size)
        



