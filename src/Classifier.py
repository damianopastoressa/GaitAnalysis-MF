import numpy as np
from FeaturesReader import FeaturesReader
import pickle

class Classifier:
    
    def __init__(self, people_list):
        self.people_list = people_list
        self.features_dir = '../features'
        self.models_dir = '../models'
        self.results_dir = '../results/'
        self.test_matrix = []
        self.std_test_matrix = []
        
    
    
    # function to read results of a classifier's fitting
    def model_reader(self, name):
        file = self.models_dir+'/'+name+'.sav'
        clf = pickle.load(open(file, 'rb'))
        return clf
    
    
    
    # Support Vector Machin Test
    def SVM_Test(self, k):
        #reading train results
        clf = self.model_reader(k+'SVM')
        # classifying testing set
        y = clf.predict(self.std_test_matrix)
        return list(y)
    
    
    
    # Random Forest Test
    def RandomForest_Test(self):
        #reading train results
        clf = self.model_reader('RandomForest')
        # classifying testing set
        y = clf.predict(self.test_matrix)            
        return list(y)
    
    
    
    # Adaboost Classifier
    def Adaboost_Test(self):
        #reading train results
        clf = self.model_reader('Adaboost')
        # classifying testing set
        y = clf.predict(self.test_matrix) 
        return list(y)
    
    
    
    # Adaboost Classifier
    def NaiveBayes_Test(self):
        #reading train results
        clf = self.model_reader('NaiveBayes')
        # classifying testing set
        y = clf.predict(self.test_matrix) 
        return list(y)    
    
    
    
    #to store results of classification
    def results_storage(self, pred, person):
        counter = 0
        for p in range(0, len(pred)):
            if pred[p] == 0:
                counter += 1
        m = np.round(counter/len(pred)*100, 2)
        f = np.round(100-m, 2)
        results_string = person+' is: '+str(m)+'% male and '+str(f)+'% female.'        
        file = open(self.results_dir+person+'.txt', "w")
        file.write(results_string)
        file.close()
        print('\n\n'+results_string)
    
    
    
    def classifier(self):
        for person in range(0, len(self.people_list)):
            # reading features
            fr = FeaturesReader(self.features_dir+'/'+self.people_list[person]+'.xlsx')
            features = fr.test_reader()
            # adding features to test matrix
            self.test_matrix = features
            #testing
            stdscaler = self.model_reader('StandardScalar')
            self.std_test_matrix = list(stdscaler.transform(self.test_matrix))
            pred = self.SVM_Test('linear')
            pred += self.SVM_Test('rbf')
            pred += self.RandomForest_Test()
            pred += self.Adaboost_Test()
            pred += self.NaiveBayes_Test()
            #store the results
            self.results_storage(pred, self.people_list[person])