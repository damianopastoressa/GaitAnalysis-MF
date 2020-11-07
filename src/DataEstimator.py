import numpy as np

class DataEstimator:
    
    def __init__(self):
        self.bodyParts = ["nose", "neck", "rshoulder", "relbow", "rwrist", "lshoulder", "lelbow", "lwrist", "midhip", "rhip", "rknee", "rankle", "lhip", "lknee", "lankle", "lbigtoe", "lheel", "rbigtoe", "rheel"]
      
        
        
    #function to calculate the index of undetected values in a coordinates array
    def calcIndex(self, coordinates):
        index = []
        for i in range(len(coordinates)):
            if coordinates[i][0] != 0 and coordinates[i][1] != 0:
                index.append(i)
        return index



    #function to estimate the undetected values in a coordinates array        
    def estimation(self, coordinates):
        #calculate indexes of undetected values                
        index = self.calcIndex(coordinates)
        # if in the array weren't detected null values, there's no need to do the estimation
        if len(index) > 0:
            # if there are some missing value at then beginning of the array
            if index[0] != 0:
                # cycle to fill every missing value
                for j in range(0, index[0]):
                    # storing values
                    coordinates[j][0] = coordinates[index[0]][0]
                    coordinates[j][1] = coordinates[index[0]][1]
            # if there are some missing value at then ending of the array
            if index[len(index)-1] != len(coordinates)-1:
                # cycle to fill every missing value
                for j in range(index[len(index)-1], len(coordinates)):
                    # storing values
                    coordinates[j][0] = coordinates[index[len(index)-1]][0]
                    coordinates[j][1] = coordinates[index[len(index)-1]][1]                
            # saving the first index
            before_index = index[0]
            # cycle for every index
            for i in range(1, len(index)):
                # if between this index and the previous one there is a distance greater than one, it means there are some values not identified
                if (index[i] - before_index) != 1:
                    # saving the index over the 'gap' between the two correct values
                    after_index = index[i]
                    # estimating every point in this gap, by using linspace method
                    estimated_values_x = np.linspace(coordinates[before_index][0], coordinates[after_index][0], after_index-before_index+2, endpoint=False, dtype=int)
                    estimated_values_y = np.linspace(coordinates[before_index][1], coordinates[after_index][1], after_index-before_index+2, endpoint=False, dtype=int)
                    # cycle to fill every missing value
                    for j in range(before_index, after_index+2):
                        # storing values
                        coordinates[j-1][0] = estimated_values_x[j-before_index]
                        coordinates[j-1][1] = estimated_values_y[j-before_index]
                # next step
                before_index = index[i]
        return coordinates
    
    
    
    def estimator(self, coordinates, visibilities):
        for p in range(0, len(self.bodyParts)):
            # building arrays for interpolations
            coords = []
            # storing coordinates by appending them in correspondent arrays
            for i in range(0, len(coordinates)):
                coords.append(coordinates[i][p])
            #estimation of the undetected values        
            coords = self.estimation(coords)
            #update patient coordinates and visibilities after estimation of undetected values        
            for i in range(0, len(coordinates)):
                coordinates[i][p] = coords[i]
                visibilities[i][p] = True       
        return coordinates, visibilities    