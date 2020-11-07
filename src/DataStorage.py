import os
import matplotlib.pyplot as plt
from DataEstimator import DataEstimator

class DataStorage:

    def __init__(self, video_name, pose_estimation):
        self.video = video_name
        self.pose2d = pose_estimation['pose2d']
        self.time = pose_estimation['time']
        self.visibilities = pose_estimation['visibilities']
        self.width = pose_estimation['width']
        self.height = pose_estimation['height']
        self.data_dir = "../data/"+ video_name
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
            print("Directory " , self.data_dir ,  " Created ")
        self.bodyParts = ["nose", "neck", "rshoulder", "relbow", "rwrist", "lshoulder", "lelbow", "lwrist", "midhip", "rhip", "rknee", "rankle", "lhip", "lknee", "lankle", "lbigtoe", "lheel", "rbigtoe", "rheel"]
        
        
        
    def write(self, directory, body_type, coordinates, endTime):
        file = open(directory +"/txt/"+ body_type+".txt","w")
        time = []
        x_coords = []
        y_coords = []
        for i in range(len(coordinates)):
            t = coordinates[i][0]
            x = coordinates[i][1]
            y = coordinates[i][2]
            file.write('%f' % (t)+" "+str(x)+" "+str(y)+"\n")
            time.append(t)
            x_coords.append(x)
            y_coords.append(y)
        file.close()
        plt.plot(time, x_coords, c="blue")
        plt.scatter(time, x_coords, c="black", s=7)
        plt.xlabel('time (s)')
        plt.ylabel('x')
        plt.axis((0, endTime, 0, self.width))
        plt.savefig(directory+'/plots/'+body_type+'X.jpeg')
        plt.close()
        plt.plot(time, y_coords, c="blue")
        plt.scatter(time, y_coords, c="black", s=7)
        plt.xlabel('time (s)')        
        plt.ylabel('y')
        plt.axis((0, endTime, 0, self.height))
        plt.savefig(directory+'/plots/'+body_type+'Y.jpeg')
        plt.close()



    def saveData(self, data_dir):
        for p in range(0, len(self.bodyParts)):
            coordinates = []
            for frame in range(0, len(self.pose2d)):
                if self.visibilities[frame][p] == True: coordinates.append((self.time[frame], self.pose2d[frame][p][0],self.height-self.pose2d[frame][p][1]))
            if not os.path.exists(data_dir+'/txt'):
                os.mkdir(data_dir+'/txt')
                print("Directory " , data_dir+'/txt' ,  " Created ")
            if not os.path.exists(data_dir+'/plots'):
                os.mkdir(data_dir+'/plots')
                print("Directory " , data_dir+'/plots' ,  " Created ")
            endTime = self.time[len(self.time)-1]+(self.time[1]-self.time[0])
            self.write(data_dir, self.bodyParts[p], coordinates, endTime)
        print("Data and plots stored")



    def originalData(self):
        data_dir = self.data_dir + '/original'
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("Directory " , data_dir ,  " Created ")
        self.saveData(data_dir)



    def estimatedData(self):
        est = DataEstimator()
        self.pose2d, self.visibilities = est.estimator(self.pose2d, self.visibilities)
        data_dir = self.data_dir + '/estimated'
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
            print("Directory " , data_dir ,  " Created ")
        self.saveData(data_dir)
       


    def storage(self):
        self.originalData()
        self.estimatedData()
 
        
