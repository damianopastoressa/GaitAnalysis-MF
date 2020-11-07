class DataReader:
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.bodyParts = ["nose", "neck", "rshoulder", "relbow", "rwrist", "lshoulder", "lelbow", "lwrist", "midhip", "rhip", "rknee", "rankle", "lhip", "lknee", "lankle", "lbigtoe", "lheel", "rbigtoe", "rheel"]

    
    
    def getTime(self, myfile):
        time = []
        fr = open(myfile, "r")
        for line in fr:
            data = line.split(" ")
            time.append(float(data[0]))
        fr.close
        return time

    
    
    def getCoords(self, myfile):
        coordinates = []
        fr = open(myfile, "r")
        for line in fr:
            data = line.split(" ")
            point = [int(data[1]), int(data[2])]
            coordinates.append(point)            
        fr.close
        return coordinates

       
    
    def reader(self):
        time = self.getTime(self.data_dir+'nose.txt')
        data = []
        for p in range(0, len(self.bodyParts)):
            data.append(self.getCoords(self.data_dir+self.bodyParts[p]+'.txt'))
        return data, time