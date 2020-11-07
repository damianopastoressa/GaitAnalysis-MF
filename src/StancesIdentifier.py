class StancesIdentifier:
    
    def __init__(self, ankle, framesRange):
        self.ankle = ankle
        self.framesRange = framesRange
        #list of frames in which a stance phase of right foot begins
        self.beginsList = []
        #duration of each right stance phase (number of frames)
        self.occList = []


    #function to merge phases of successive stances that are not interspersed with a swing phase
    def mergeNoSwingStances(self):        
        if len(self.beginsList) > 1:
            end = False
            while (end==False):
                end = True
                i = 0
                while(i<len(self.beginsList)-1):
                    merged = True
                    error = 0
                    while error < (self.framesRange-2) and merged==True:
                        if((self.beginsList[i]+self.occList[i]+error) == self.beginsList[i+1]):
                            self.occList[i] += self.occList[i+1]+error
                            del self.beginsList[i+1]
                            del self.occList[i+1]
                            merged = False
                            end = False
                        error += 1
                    i += 1



    #function to merge two phases of stance, in which the second begins at the same point where the first ends
    def mergeNoDisplacementStances(self):
        if len(self.beginsList) > 1:
            end = False
            while (end==False):
                end = True
                i = 0
                while(i<len(self.beginsList)-1):
                    if (self.ankle[self.beginsList[i]+self.occList[i]-1] == self.ankle[self.beginsList[i+1]]):
                        self.occList[i] += self.occList[i+1]+(self.beginsList[i+1]-(self.beginsList[i]+self.occList[i]))
                        del self.beginsList[i+1]
                        del self.occList[i+1]
                        end = False
                    i += 1
        
        
        
    #function to eliminate the the stance phase that begins in the first frame (if there is it), because it could be incomplete 
    def zeroStanceElimination(self):
        if(len(self.beginsList) > 0):
            if self.beginsList[0] == 0 or self.beginsList[0] == 1:
                del self.beginsList[0]        
                del self.occList[0]
        
        
        
    #function to display stance phases       
    def displayStancePhases(self):
        for i in range(0, len(self.beginsList)):
            print(str(i+1) + " stance")
            beg = self.beginsList[i]
            occ = self.occList[i]
            for j in range(0, occ):
                print("Frame " + str(beg+j) + " ->\t" + str(self.ankle[beg+j]))
                


    #function to extract the points in which a foot begins his stance phase
    def identifier(self):
        prev = self.ankle[0]
        occ = 1
        for k in range (1, len(self.ankle)):
            if self.ankle[k] == prev:
                occ += 1
                if k == len(self.ankle)-1:
                    if occ >= self.framesRange:
                        self.occList.append(occ)
                        self.beginsList.append(k - occ + 1)
            elif self.ankle[k][0] == prev[0]:
                occ += 1
                if k == len(self.ankle)-1:
                    if occ >= self.framesRange:
                        self.occList.append(occ)
                        self.beginsList.append(k - occ + 1)                          
            else:
                if occ >= self.framesRange:
                    self.occList.append(occ)
                    self.beginsList.append(k - occ)
                prev = self.ankle[k]
                occ = 1  
        #merge phases of successive stances that are not interspersed with a swing phase
        self.mergeNoSwingStances()
        #merge two phases of stance, in which the second begins at the same point where the first ends
        self.mergeNoDisplacementStances()
        #eliminate the the stance phase that begins in the first frame (if there is it), because it could be incomplete
        self.zeroStanceElimination()
        #display stance phases
        self.displayStancePhases()
        return self.beginsList