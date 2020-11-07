import numpy as np
import math
import copy

class AnglesCalculator:
    
    def __init__(self, stride):
        self.stride = stride
        
    
    
    #function to calculate the angular coefficient of the straight line passing through two points
    def angularCoefficient(self, p1, p2):
        num = p2[1]-p1[1]
        den = p2[0]-p1[0]
        if den == 0:
            return math.inf
        else:
            return num/den
    
    
    
    #function to calculate the acute angle between two straight lines
    def get_angle(self, p1, p2, p3):
        alfa = 0
        m1 = self.angularCoefficient(p1, p2)
        m2 = self.angularCoefficient(p2, p3)
        if m1 == math.inf and m2 == math.inf:
            alfa = 0
        elif m1 == math.inf:
            m2 = self.angularCoefficient([-p2[1], p2[0]], [-p3[1], p3[0]])
            alfa = np.arctan(np.abs(m2))
        elif m2 == math.inf:
            m1 = self.angularCoefficient([-p1[1], p1[0]], [-p2[1], p2[0]])
            alfa = np.arctan(np.abs(m1))
        else:            
            num = m1-m2
            den = 1 +(m1*m2)
            if den != 0:
                fraz = num/den
                alfa = np.arctan(np.abs(fraz))
            else:
                alfa = math.pi/2
        return alfa


    
    #function to translate a point by a center of translation
    def translation(self, p, center):
        p[0] -= center[0]
        p[1] -= center[1]
        return p
        
    
    #function to rotate a point by a corner
    def rotation(self, p, angle):
        x = p[0]*np.cos(angle)-p[1]*np.sin(angle)
        y = p[0]*np.sin(angle)+p[1]*np.cos(angle)
        return [x, y]
    


    #function to symmetrize a point respect to y axis
    def symmetrize(self, p):
        return [-p[0], p[1]]

    
    
    #function to calculate one angle in one stride
    def calculator(self, bodyPart1, bodyPart2, bodyPart3):
        angles = []
        for frame in range(0, len(self.stride[1][0])):
            #acquisition of the points that determine the angle
            p1 = copy.deepcopy(self.stride[1][bodyPart1][frame])
            p2 = copy.deepcopy(self.stride[1][bodyPart2][frame])
            p3 = copy.deepcopy(self.stride[1][bodyPart3][frame])
            #traslation of p1 and p2
            p1 = self.translation(p1, p3)
            p2 = self.translation(p2, p3)
            p3 = self.translation(p3, p3)
            #verify if a rotation is needed
            rotation = False
            if p2[0] < p3[0]:
                rotation = True
                #angle of rotation
                tetha = - (math.pi/2-self.get_angle(p2, p3, [p2[0],0]))
            elif p2[0] > p3[0]:
                rotation = True
                #angle of rotation
                tetha = (math.pi/2-self.get_angle(p2, p3, [p2[0],0]))
            if rotation == True:
                p1 = np.round(self.rotation(p1, tetha), 2)
                p2 = np.round(self.rotation(p2, tetha), 2)
            # a symmetry respect to y axis is needed for p1
            p1 = self.symmetrize(p1)
            #verify if the acute or obtuse angle is needed
            if p1[1] <= p2[1]:
                angles.append(np.round(np.degrees(self.get_angle(p1, p2, p3)), 2))
            elif p1[0] < p2[0]:
                angles.append(np.round(180 + np.degrees(self.get_angle(p1, p2, p3)), 2))
            elif p1[0] == p2[0]:
                angles.append(np.round(180, 2))
            else:
                angles.append(np.round(180 - np.degrees(self.get_angle(p1, p2, p3)), 2))
        return angles