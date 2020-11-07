import numpy as np

class VelocitiesCalculator:
    
    def __init__(self, stride):
        self.stride = stride
        
        
    
    #function to calculate x, y and joint mean velocities in one stride
    def calculator(self, bodyPart):
        vel_x_array = []
        vel_y_array = []
        vel_joint_array = []
        delta_t = abs(self.stride[0][1] - self.stride[0][0])
        for frame in range (0, len(self.stride[1][0])-1):        
            delta_x = abs(self.stride[1][bodyPart][frame][0] - self.stride[1][bodyPart][frame+1][0])
            delta_y = abs(self.stride[1][bodyPart][frame][1] - self.stride[1][bodyPart][frame+1][1])
            vx = delta_x / delta_t
            vy = delta_y / delta_t
            vel_x_array.append(vx)
            vel_y_array.append(vy)
            vel_joint_array.append(np.sqrt(pow(vx, 2)+pow(vy, 2)))
        return np.round(np.mean(vel_x_array), 2), np.round(np.mean(vel_y_array), 2), np.round(np.mean(vel_joint_array), 2)