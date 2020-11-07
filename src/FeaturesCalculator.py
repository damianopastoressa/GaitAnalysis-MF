import numpy as np
from VelocitiesCalculator import VelocitiesCalculator
from AnglesCalculator import AnglesCalculator

class FeaturesCalculator:
    
    def __init__(self, strides_info):
        self.strides_info = strides_info
        #array in which to store all features of each stride about one person:
        #each row for a stride
        #each column for a feature: 
        # 1) height (pixel)
        # 2) cadence (strides/min)
        # 3) stride length (pixel)
        # 4) stride length normalized for height
        # 5) x hip velocity (pixel/sec)
        # 6) y hip velocity (pixel/sec)
        # 7) joint hip velocity (pixel/sec)
        # 8) x knee velocity(pixel/sec)
        # 9) y knee velocity(pixel/sec)
        # 10) joint knee velocity(pixel/sec)
        # 11) x ankle velocity(pixel/sec)
        # 12) y ankle velocity(pixel/sec)
        # 13) joint ankle velocity(pixel/sec)
        # 14) hip flexion: min shoulder, hip, knee angle
        # 15) hip extension: max shoulder, hip, knee angle
        # 16) knee extension before initial contact: hip, knee, ankle angle in the last frame of a stride
        # 17) knee flexion: min hip, knee, ankle angle
        # 18) knee extension: max hip, knee, ankle angle
        # 19) ankle plantar flexion: min ankle, heel, big toe angle
        # 20) ankle plantar extension: max ankle, heel, big toe angle
        self.features = []         
    
    
    def calculator(self, gender):
        # 2) cadence (strides/min)
        n_strides = len(self.strides_info)
        time = 0
        for i in range(0, len(self.strides_info)):
            time += self.strides_info[i][0][len(self.strides_info[i][0])-1]+(self.strides_info[i][0][1]-self.strides_info[i][0][0])
        cadence = int(n_strides/time*60)
        #calculating features for each stride
        for i in range(0, len(self.strides_info)):
            f = []
            # 1) height (pixel)
            h = []
            for j in range(0, len(self.strides_info[i][1][0])):
                h.append(abs(self.strides_info[i][1][0][j][1]-self.strides_info[i][1][16][j][1]))
            f.append(np.round(np.amax(h), 2))
            # 2) cadence (strides/min)
            f.append(cadence)
            # 3) stride length (pixel)
            l = []
            for j in range(0, len(self.strides_info[i][1][0])):
                l.append(abs(self.strides_info[i][1][14][j][0]-self.strides_info[i][1][11][j][0]))
            f.append(np.round(np.amax(l), 2))
            # 4) stride length normalized for height
            f.append(np.round(f[2]/f[0], 2))
            # velocities
            vc = VelocitiesCalculator(self.strides_info[i])
            # 5,6,7) hip velocities (pixel/sec)
            vel_x_hip, vel_y_hip, vel_joint_hip = vc.calculator(12)
            f.append(vel_x_hip)
            f.append(vel_y_hip)
            f.append(vel_joint_hip)
            # 8,9,10) knee velocities (pixel/sec)
            vel_x_knee, vel_y_knee, vel_joint_knee = vc.calculator(13)
            f.append(vel_x_knee)
            f.append(vel_y_knee)
            f.append(vel_joint_knee)
            # 11,12,13) ankle velocities (pixel/sec)
            vel_x_ankle, vel_y_ankle, vel_joint_ankle = vc.calculator(14)
            f.append(vel_x_ankle)
            f.append(vel_y_ankle)
            f.append(vel_joint_ankle)
            # angles
            ac = AnglesCalculator(self.strides_info[i])
            # shoulder, hip, knee angle
            angles = ac.calculator(5, 12, 13)
            # 14) hip flexion: min shoulder, hip, knee angle
            f.append(np.round(np.amin(angles), 2))
            # 15) hip extension: max shoulder, hip, knee angle
            f.append(np.round(np.amax(angles), 2))
            # hip, knee, ankle angle
            angles = ac.calculator(12, 13, 14)
            # 16) knee extension before initial contact: hip, knee, ankle angle in the last frame of a stride
            f.append(np.round(angles[len(angles)-1], 2))
            # 17) knee flexion: min hip, knee, ankle angle
            f.append(np.round(np.amin(angles), 2))
            # 18) knee extension: max hip, knee, ankle angle
            f.append(np.round(np.amax(angles), 2))
            # ankle, heel, big toe angle
            angles = ac.calculator(14, 16, 15)
            # 19) ankle plantar flexion: min ankle, heel, big toe angle            
            f.append(np.round(np.amin(angles), 2))
            # 20) ankle plantar extension: max ankle, heel, big toe angle
            f.append(np.round(np.amax(angles), 2))
            #gender
            if gender != -1:
                f.append(gender)
            self.features.append(f)
        return self.features