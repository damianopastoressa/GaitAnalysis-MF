import os
from DataReader import DataReader
from FeaturesCalculator import FeaturesCalculator
from FeaturesStorage import FeaturesStorage

class FeaturesExtractor:
    
    def __init__(self, data_list):
        self.strides_dir = '../strides/'
        #lisrt of data to analize
        self.data_list = data_list
        #array in which to store data of each stride
        self.strides_info = []


                
    #function to extract all features to analize about each person
    def extractor(self):
        #array in which to store people list
        people_list = []
        #initialization of prev_person
        prev_person = ""
        #for each person
        for i in range (0, len(self.data_list)):
            #identification of current person
            curr_person = self.data_list[i].split("_")[0]
            #if a new person is found
            if curr_person != prev_person:
                #if a previuous person exists
                if prev_person != "":
                    #function to calculate features about a person
                    fc = FeaturesCalculator(self.strides_info)
                    #identification of gender: 0 for male, 1 for female
                    if prev_person[0] == 'M':
                        features = fc.calculator(0)                        
                    elif prev_person[0] == 'F':
                        features = fc.calculator(1)
                    else:
                        features = fc.calculator(-1)
                    #function to store features about a person
                    fs = FeaturesStorage(prev_person, features)
                    fs.storage()
                    #addind prev_person to list
                    people_list.append(prev_person)
                    #to free array with strides data
                    self.strides_info = []
                #updating prev_person
                prev_person = curr_person
                #list of strides about current person
                strides_list = os.listdir(self.strides_dir+self.data_list[i])
                for j in range(0, len(strides_list)):
                    #reading data of the selected stride 
                    dr = DataReader(self.strides_dir+self.data_list[i]+'/'+strides_list[j]+'/kalman/txt/')
                    data, time = dr.reader()
                    #adding stride data to strides_info array
                    self.strides_info.append([time, data])
            else:
                #list of strides about current person
                strides_list = os.listdir(self.strides_dir+self.data_list[i])
                for j in range(0, len(strides_list)):
                    #reading data of the selected stride 
                    dr = DataReader(self.strides_dir+self.data_list[i]+'/'+strides_list[j]+'/kalman/txt/')
                    data, time = dr.reader()
                    #adding stride data to strides_info array
                    self.strides_info.append([time, data])
                #if the last folder is rerached up 
                if i == len(self.data_list)-1:
                    #function to calculate features about a person
                    fc = FeaturesCalculator(self.strides_info)
                    #identification of gender: 0 for male, 1 for female
                    if prev_person[0] == 'M':
                        features = fc.calculator(0)                        
                    elif prev_person[0] == 'F':
                        features = fc.calculator(1)
                    else:
                        features = fc.calculator(-1)
                    #function to store features about a person
                    fs = FeaturesStorage(prev_person, features)
                    fs.storage()
                    #addind prev_person to list
                    people_list.append(prev_person)
        return people_list