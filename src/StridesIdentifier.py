from DataReader import DataReader
from StancesIdentifier import StancesIdentifier
from StridesStorage import StridesStorage

class StridesIdentifier:
    
    def __init__(self, data_list):
        self.data_dir = '../data/'
        #list of data folder to analize
        self.data_list = data_list



    #function to check if there is a deburring
    def isDeburring(self, ankle, k, j, framesToCompare):
        decision = False
        #cycle to analize each frame in a specific range to check if there is a deburring
        for x in range (0, framesToCompare):
            if ankle[k+x][j] == ankle[k-1][j]:
                decision = True
        return decision



    #deburrings elimination
    def deburringsElimination(self, ankle, framesRange):
        #cycle to analize each frame
        for k in range(1, len(ankle)-framesRange+2):
            #cycle to analize each coordinate (x and y)
            for j in range(0, len(ankle[k])):
                #checking if there is a variation in the coordinate values
                if ankle[k][j] != ankle[k-1][j]:
                    #function to check if the variation is a deburring
                    if self.isDeburring(ankle, k, j, framesRange-1):
                        #deburring elimination
                        ankle[k][j] = ankle[k-1][j]
        return ankle



    #function to individuate the beginning and the end of each stride
    def stridesIdentification(self, stanceBeginnings):
        strides = []
        #cycle to analize each stance phase
        for i in range(0, len(stanceBeginnings)-1):
            #starting frame of each stride
            start = stanceBeginnings[i]
            #ending frame of each stride
            end = stanceBeginnings[i+1]-1
            #storing starting and ending frame of each stride 
            strides.append([start, end])
        return strides
    
            

    #function to identifier strides from data (in txt files) about each video and to store strides informations in txt files
    def identifier(self):
        #for each data folder
        for i in range (0, len(self.data_list)):
            data_folder = self.data_dir + self.data_list[i] + '/estimated/txt/'
            #reading data from txt files
            dff = DataReader(data_folder)
            data, time = dff.reader()
            #calculation of the number of frame to individuate a stance fase
            frameTime = float(time[1])-float(time[0])
            framesRange = round(0.15/frameTime)
            #extracting right ankle coordinates
            lankle = []
            for k in range(0, len(data[14])):
                lankle.append([data[14][k][0], data[14][k][1]])
            #deburrings elimination
            lankle = self.deburringsElimination(lankle, framesRange)
            #individuation of points in which a stance phase begins
            stanceId = StancesIdentifier(lankle, framesRange)
            print("\n\n\t"+self.data_list[i])
            stanceBeginnings = stanceId.identifier()
            #identification of the beginning and the end of each stride
            strides = self.stridesIdentification(stanceBeginnings)
            #store the information about each stride
            ss = StridesStorage(self.data_list[i], data, time, strides)
            ss.storage()