import os
import matplotlib.pyplot as plt
from KalmanSmoother import KalmanSmoother

class StridesStorage:

    def __init__(self, video_name, data, time, strides):
        self.video_name = video_name
        self.data = data
        self.time = time
        self.strides = strides
        self.strides_dir = "../strides/"+self.video_name
        if not os.path.exists(self.strides_dir):
            os.mkdir(self.strides_dir)
            print("Directory " , self.strides_dir ,  " Created ")
        self.bodyParts = ["nose", "neck", "rshoulder", "relbow", "rwrist", "lshoulder", "lelbow", "lwrist", "midhip", "rhip", "rknee", "rankle", "lhip", "lknee", "lankle", "lbigtoe", "lheel", "rbigtoe", "rheel"]
        
        
        
    def write(self, txt_dir, plots_dir, body_type, coordinates, endTime):
        file = open(txt_dir +"/"+ body_type+".txt","w")
        time = []
        x_coords = []
        y_coords = []
        for i in range(0, len(coordinates)):
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
#        plt.axis((0, endTime, 0, self.width))
        plt.savefig(plots_dir+'/'+body_type+'X.jpeg')
        plt.close()
        plt.plot(time, y_coords, c="blue")
        plt.scatter(time, y_coords, c="black", s=7)
        plt.xlabel('time (s)')        
        plt.ylabel('y')
 #       plt.axis((0, endTime, 0, self.height))
        plt.savefig(plots_dir+'/'+body_type+'Y.jpeg')
        plt.close()



    def saveData(self, data_type):
        for i in range(0, len(self.strides)):
            stride_dir = self.strides_dir + '/' + str(i+1)
            if not os.path.exists(stride_dir):
                os.mkdir(stride_dir)
                print("Directory " , stride_dir ,  " Created ")
            type_dir = stride_dir + '/' + data_type
            if not os.path.exists(type_dir):
                os.mkdir(type_dir)
                print("Directory " , type_dir ,  " Created ")
            txt_dir = type_dir + '/txt'
            if not os.path.exists(txt_dir):
                os.mkdir(txt_dir)
                print("Directory " , txt_dir ,  " Created ")
            plots_dir = type_dir + '/plots'
            if not os.path.exists(plots_dir):
                os.mkdir(plots_dir)
                print("Directory " , plots_dir ,  " Created ")
            for p in range(0, len(self.bodyParts)):
                coordinates = []
                for frame in range(self.strides[i][0], self.strides[i][1]+1):
                    coordinates.append([self.time[frame], self.data[p][frame][0], self.data[p][frame][1]])
                endTime = self.time[len(self.time)-1]+(self.time[1]-self.time[0])
                self.write(txt_dir, plots_dir, self.bodyParts[p], coordinates, endTime)
            print("Txt and plots stored for " + str(i+1) + " stride of " + self.video_name + " video.")



    def storage(self):
        #storing data separated by steps
        self.saveData("estimated")
        #function to apply kalman filter to data
        ks = KalmanSmoother(self.data)
        self.data = ks.kalman_smoother()
        #storing data separated by steps after kalman filter
        self.saveData("kalman")