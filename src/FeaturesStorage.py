import openpyxl

class FeaturesStorage:
    
    def __init__(self, person, features):
        self.features_dir = '../features/'
        self.person = person
        self.file_name = person+'.xlsx'
        self.features = features
        self.coordL = self.enumerator()
        


    #function to enumerate excel column needed to store features array
    def enumerator(self):
        coordL = []
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        alphabetPlus = [''] + alphabet
        count = 0
        for j in range(0, len(alphabetPlus)):
            for k in range(0, len(alphabetPlus)):
                for i in range(0, len(alphabet)):
                    coordL.append(alphabetPlus[j]+alphabetPlus[k]+alphabet[i])
                    count += 1
        return coordL        
        
    
    
    #function to store some features
    def storage(self):
        fw = self.features_dir+self.file_name
        file = openpyxl.Workbook()
        sheet = file.worksheets[0]
        for i in range (0, len(self.features)):
            for j in range(0, len(self.features[i])):
                pos = self.coordL[j] + str(i + 1)
                sheet[pos] = self.features[i][j]        
        file.save(fw)
        print("Features calculated for " + self.person + " and stored in " + fw)