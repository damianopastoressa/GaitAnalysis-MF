import numpy as np
from FeaturesReader import FeaturesReader
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import pickle

class Train:
    
    def __init__(self, people_list):
        self.people_list = people_list
        self.features_dir = '../features'
        self.models_dir = '../models/'
        self.train_matrix = []
        self.std_train_matrix = []        
        self.train_labels = []
    


    # function to store results of a classifier's fitting
    def model_storage(self, clf, name):
        file = self.models_dir+'/'+name+'.sav'
        pickle.dump(clf, open(file, 'wb'))    
    


    # Support Vector Machin Train
    def SVM_Train(self, k):
        # initializing classifier
        clf = SVC(gamma='auto', kernel=k)
        # training the classifier
        clf.fit(self.std_train_matrix, self.train_labels)
        #storage train results
        self.model_storage(clf, k+'SVM')
    
    
    
    # Random Forest Train
    def RandomForest_Train(self):
        # initializing classifier
        clf = RandomForestClassifier(n_estimators=50, max_depth=5)
        # training the classifier
        clf.fit(self.train_matrix, self.train_labels)
        #storage train results
        self.model_storage(clf, 'RandomForest')
    
    
    
    # Adaboost Train
    def Adaboost_Train(self):
        # initializing classifier
        dt = tree.DecisionTreeClassifier(criterion='gini', min_samples_split=5, max_depth=10)  # min_samples_split=10, max_depth=8
        clf = AdaBoostClassifier(dt, n_estimators=10)
        # training the classifier
        clf.fit(self.train_matrix, self.train_labels)
        #storage train results
        self.model_storage(clf, 'Adaboost')

    
    
    # Naive Bayes Train
    def NaiveBayes_Train(self):
        # initializing classifier
        clf = GaussianNB()
        # training the classifier
        clf.fit(self.train_matrix, self.train_labels)
        #storage train results
        self.model_storage(clf, 'NaiveBayes')
        
        
    
    # function to rank the features        
    def features_ranking(self):
        # Features names
        features_array = ['h', 'cad', 'str len', 'str len n', 'hip xvel', 'hip yvel', 'hip vel', 'knee xvel', 'knee yvel', 'knee vel', 'ankle xvel', 'ankle yvel', 'ankle vel', 'hip flex', 'hip ext', 'knee ext bic', 'knee flex', 'knee ext', 'ankle flex', 'ankle ext']
        tree_clf = ExtraTreesClassifier(n_estimators=5000)
        tree_clf1 = tree_clf.fit(self.train_matrix, self.train_labels)
        # Normalizing the individual importances
        feature_importance_normalized = np.std([tree.feature_importances_ for tree in
                                        tree_clf1.estimators_],
                                        axis = 0)
        indices = np.argsort(feature_importance_normalized)[::-1]
        labels = []
        values = []
        for i in range(0, len(features_array)):
            labels.append(features_array[indices[i]].replace('_', '\n'))
            values.append(feature_importance_normalized[indices[i]])
        plt.figure(figsize=(19.2,10.8))
        plt.bar(labels, values)
        plt.xlabel('Feature Labels')
        plt.ylabel('Feature Importances')
        plt.title('Comparison of different Feature Importances')
        plt.savefig('../features_ranking.jpg')
        plt.close()  
        
        
        
    def training(self):
        #for each person
        for person in range(0, len(self.people_list)):
            # reading features
            fr = FeaturesReader(self.features_dir+'/'+self.people_list[person]+'.xlsx')
            features, labels = fr.train_reader()
            # adding features to test matrix
            self.train_matrix += features
            # adding labels to test labels
            self.train_labels += labels
        #standardization                
        stdscaler = StandardScaler()
        self.std_train_matrix = list(stdscaler.fit_transform(self.train_matrix))
        self.model_storage(stdscaler, 'StandardScalar')
        #training
        self.SVM_Train('linear')
        self.SVM_Train('rbf')
        self.RandomForest_Train()
        self.Adaboost_Train()
        self.NaiveBayes_Train()
        #features ranking
        self.features_ranking()        