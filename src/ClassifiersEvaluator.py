import random
import numpy as np
import math
from FeaturesReader import FeaturesReader
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix

class ClassifiersEvaluator:
    
    def __init__(self, people_list):
        self.people_list = people_list
        self.features_dir = '../features'
        self.results_dir = '../models'
        self.linearSVM = []
        self.rbfSVM = []
        self.RandomForest = []
        self.Adaboost = []
        self.NaiveBayes = []
    
    
    
    # rating of a classifier
    def classifier_rating(self, pred):
        # creating the confusion matrix based on classification
        cm = confusion_matrix(self.test_labels, pred, labels=[0, 1])
        # normalizing confusion matrix
        cm = cm.astype('float')
        for i in range(0, len(cm)):
            s = 0
            for j in range(0, len(cm[i])):
                s += cm[i][j]
            if s != 0:
                for j in range(0, len(cm[i])):
                    cm[i][j] = cm[i][j] / s 
        # extracting data from confusion matrix
        true_negative, false_positive, false_negative, true_positive = cm.ravel()
        #calculating indexes based on confusion matrix
        # Sensitivity or true positive rate
        if true_positive==0 and false_negative==0:
            true_positive_rate = math.nan
        else:
            true_positive_rate = true_positive/(true_positive+false_negative)
        # Specificity or true negative rate
        if true_negative==0 and false_positive==0:
            true_negative_rate = math.nan
        else:
            true_negative_rate = true_negative/(true_negative+false_positive)
        # Precision or positive predictive value
        if true_positive==0 and false_positive==0:
            positive_predictive_value = math.nan
        else:
            positive_predictive_value = true_positive/(true_positive+false_positive)
        # Overall accuracy
        if true_positive==0 and false_positive==0 and false_negative==0 and true_negative==0:
            accuracy = math.nan
        else:
            accuracy = (true_positive+true_negative)/(true_positive+false_positive+false_negative+true_negative)    
        return [true_positive_rate, true_negative_rate, positive_predictive_value, accuracy]
    
    
    
    # Support Vector Machin Classifier
    def SVM_Classifier(self, k):
        # initializing classifier
        clf = SVC(gamma='auto', kernel=k)
        # training the classifier
        clf.fit(self.std_train_matrix, self.train_labels)
        # classifying testing set
        y = clf.predict(self.std_test_matrix)
        #evaluation
        indexes = self.classifier_rating(y)
        #if linear kernel
        if k == 'linear':
            self.linearSVM.append(indexes)
        else:
            self.rbfSVM.append(indexes)
    
    
    
    # Random Forest Classifier
    def RandomForest_Classifier(self):
        # initializing classifier
        clf = RandomForestClassifier(n_estimators=50, max_depth=5)
        # training the classifier
        clf.fit(self.train_matrix, self.train_labels)
        # classifying testing set
        y = clf.predict(self.test_matrix)            
        #evaluation
        self.RandomForest.append(self.classifier_rating(y))
    
    
    
    # Adaboost Classifier
    def Adaboost_Classifier(self):   
        # initializing classifier
        dt = tree.DecisionTreeClassifier(criterion='gini', min_samples_split=5, max_depth=10)  # min_samples_split=10, max_depth=8
        clf = AdaBoostClassifier(dt, n_estimators=10)
        # training the classifier
        clf.fit(self.train_matrix, self.train_labels)
        # classifying testing set
        y = clf.predict(self.test_matrix) 
        #rating of classifier
        self.Adaboost.append(self.classifier_rating(y))
    
    
    
    # Naive Bayes Classifier
    def NaiveBayes_Classifier(self):
        # initializing classifier
        clf = GaussianNB()
        # training the classifier
        clf.fit(self.train_matrix, self.train_labels)
        # classifying testing set
        y = clf.predict(self.test_matrix) 
        #rating of classifier
        self.NaiveBayes.append(self.classifier_rating(y))



    #function to calculate mean of each index of evaluation about a classifier
    def calc_mean(self, multi_array):
        ind1 = []
        ind2 = []
        ind3 = []
        ind4 = []
        for i in range(0, len(multi_array)):
            ind1.append(multi_array[i][0])
            ind2.append(multi_array[i][1])
            ind3.append(multi_array[i][2])
            ind4.append(multi_array[i][3])
        return np.round(np.mean(ind1), 2), np.round(np.mean(ind2), 2), np.round(np.mean(ind3), 2), np.round(np.mean(ind4), 2)



    #function to store results of evaluation
    def results_storage(self):
        results = '\t\t\tClassifiers Evaluation'
        results += '\n\nSVM with linear kernel:'
        i1, i2, i3, i4 = self.calc_mean(self.linearSVM)
        results += '\nSensitivity = '+str(i1)+'\nSpecificity = '+str(i2)+'\nPrecision = '+str(i3)+'\nAccuracy = '+str(i4)
        results += '\n\nSVM with rbf kernel:'
        i1, i2, i3, i4 = self.calc_mean(self.rbfSVM)
        results += '\nSensitivity = '+str(i1)+'\nSpecificity = '+str(i2)+'\nPrecision = '+str(i3)+'\nAccuracy = '+str(i4)
        results += '\n\nRandom Forest:'
        i1, i2, i3, i4 = self.calc_mean(self.RandomForest)
        results += '\nSensitivity = '+str(i1)+'\nSpecificity = '+str(i2)+'\nPrecision = '+str(i3)+'\nAccuracy = '+str(i4)
        results += '\n\nAdaboost:'
        i1, i2, i3, i4 = self.calc_mean(self.Adaboost)
        results += '\nSensitivity = '+str(i1)+'\nSpecificity = '+str(i2)+'\nPrecision = '+str(i3)+'\nAccuracy = '+str(i4)
        results += '\n\nNaive Bayes:'
        i1, i2, i3, i4 = self.calc_mean(self.NaiveBayes)
        results += '\nSensitivity = '+str(i1)+'\nSpecificity = '+str(i2)+'\nPrecision = '+str(i3)+'\nAccuracy = '+str(i4)
        file = open(self.results_dir+'/ClassifiersEvaluation.txt', "w")
        file.write(results)
        file.close()
        print('\n\n\n'+results)

            
    
    def evaluator(self):
        for i in range(0, 10):
            #random selection of people to test
            random_list1 = random.sample(range(0, 25), 10)
            random_list2 = random.sample(range(25, 50), 10)
            index_list = random_list1+random_list2
            #initialization
            self.train_matrix = []
            self.std_train_matrix = []        
            self.train_labels = []
            self.test_matrix = []
            self.std_test_matrix = []
            self.test_labels = []
            #for each person
            for person in range(0, len(self.people_list)):
                # reading features
                fr = FeaturesReader(self.features_dir+'/'+self.people_list[person]+'.xlsx')
                features, labels = fr.train_reader()
                # verify if person is in test list
                if person in index_list:
                    # adding features to test matrix
                    self.test_matrix += features
                    # adding labels to test labels
                    self.test_labels += labels
                else:
                    # adding features to train matrix
                    self.train_matrix += features
                    # adding labels to train labels
                    self.train_labels += labels
            #standardization                
            stdscaler = StandardScaler()
            self.std_train_matrix = list(stdscaler.fit_transform(self.train_matrix))
            self.std_test_matrix = list(stdscaler.transform(self.test_matrix))
            #classification
            self.SVM_Classifier('linear')
            self.SVM_Classifier('rbf')
            self.RandomForest_Classifier()
            self.Adaboost_Classifier()
            self.NaiveBayes_Classifier()
        #storing results of evaluation
        self.results_storage()                