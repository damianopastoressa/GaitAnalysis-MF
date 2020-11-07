import numpy as np
from pykalman import KalmanFilter

class KalmanSmoother:
    
    def __init__(self, data):
        self.data = data
        self.bodyParts = ["nose", "neck", "rshoulder", "relbow", "rwrist", "lshoulder", "lelbow", "lwrist", "midhip", "rhip", "rknee", "rankle", "lhip", "lknee", "lankle", "lbigtoe", "lheel", "rbigtoe", "rheel"]
        
    
    
    #function to apply the kalman filter    
    def kalman_smoother(self): 
        # initializing temp variables which will contain x and y patient's coordinates
        x_coordinates_to_smooth = []
        y_coordinates_to_smooth = []
        # splitting all the coordinates from the array
        for i in range(0, len(self.data[0])):
            # splitting and appending to our variables
            x_coordinates_to_smooth.append([self.data[0][i][0], self.data[1][i][0], self.data[2][i][0], self.data[3][i][0], self.data[4][i][0], self.data[5][i][0], self.data[6][i][0], self.data[7][i][0], self.data[8][i][0], self.data[9][i][0], self.data[10][i][0], self.data[11][i][0], self.data[12][i][0], self.data[13][i][0], self.data[14][i][0], self.data[15][i][0], self.data[16][i][0], self.data[17][i][0], self.data[18][i][0]])
            y_coordinates_to_smooth.append([self.data[0][i][1], self.data[1][i][1], self.data[2][i][1], self.data[3][i][1], self.data[4][i][1], self.data[5][i][1], self.data[6][i][1], self.data[7][i][1], self.data[8][i][1], self.data[9][i][1], self.data[10][i][1], self.data[11][i][1], self.data[12][i][1], self.data[13][i][1], self.data[14][i][1], self.data[15][i][1], self.data[16][i][1], self.data[17][i][1], self.data[18][i][1]])
        # using smoother x
        # declaring filter (initial state = starting value for the filter to make his smoothing, n_dim_obs = length of values)
        kf = KalmanFilter(initial_state_mean=x_coordinates_to_smooth[0], n_dim_obs=len(self.bodyParts))
        measurements = x_coordinates_to_smooth
        # initializing filter, giving data to smooth and number of iterations
        kf = kf.em(measurements, n_iter=5)
        # calling the smoother, and saving smoothed files
        (smoothed_state_means, smoothed_state_covariances) = kf.smooth(measurements)
        # rounding values to a non decimal number
        for i in range(len(smoothed_state_means)):
            for j in range(len(smoothed_state_means[0])):
                smoothed_state_means[i][j] = np.round(smoothed_state_means[i][j])
        # re-assigning data to return
        x_coordinates_to_smooth = smoothed_state_means
        # using smoother y
        kf = KalmanFilter(initial_state_mean=y_coordinates_to_smooth[0], n_dim_obs=len(self.bodyParts))
        measurements = y_coordinates_to_smooth
        kf = kf.em(measurements, n_iter=5)
        (smoothed_state_means, smoothed_state_covariances) = kf.smooth(measurements)

        for i in range(len(smoothed_state_means)):
            for j in range(len(smoothed_state_means[0])):
                smoothed_state_means[i][j] = np.round(smoothed_state_means[i][j])
        y_coordinates_to_smooth = smoothed_state_means
        # cycle to build the return array
        for p in range(0, len(self.data)):
            for i in range(0, len(self.data[p])):
                self.data[p][i] = [int(x_coordinates_to_smooth[i][p]), int(y_coordinates_to_smooth[i][p])]
        return self.data