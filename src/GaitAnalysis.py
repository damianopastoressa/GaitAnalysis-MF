import os
from DataExtractor import DataExtractor
from StridesIdentifier import StridesIdentifier
from FeaturesExtractor import FeaturesExtractor
from ClassifiersEvaluator import ClassifiersEvaluator
from Train import Train
from InfluxCalculator import InfluxCalculator
from Classifier import Classifier

models_dir = '../models'
# if train models folder is empty
if len(os.listdir(models_dir)) == 0:
    # train phase
    #function to extract frames from videos and to create txt files with data of interest from each video
    de = DataExtractor('train')
    videos_list = de.extractor()
    #function to identifier strides from data (in txt files) about each video and to store strides informations in txt files
    si = StridesIdentifier(videos_list)
    si.identifier()
    #function to extract all features to analize about each person
    fe = FeaturesExtractor(videos_list)
    people_list = fe.extractor()
    #function to evaluate classifiers
    ce = ClassifiersEvaluator(people_list)
    ce.evaluator()
    #function to train classifiers
    t = Train(people_list)
    t.training()
#test phase
#function to extract frames from videos and to create txt files with data of interest from each video
de = DataExtractor('test')
videos_list = de.extractor()
#function to identifier strides from data (in txt files) about each video and to store strides informations in txt files
si = StridesIdentifier(videos_list)
si.identifier()
#function to extract all features to analize about each person
fe = FeaturesExtractor(videos_list)
people_list = fe.extractor()
#function to classify people
c = Classifier(people_list)
c.classifier()
#function to calculate influx of people
ic = InfluxCalculator()
ic.calculator()