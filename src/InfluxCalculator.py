import os 

class InfluxCalculator:
    
    def __init__(self):
        self.results_dir = '../results'
        
        
        
    #function to read results
    def results_reader(self, myfile):
        fr = open(self.results_dir+'/'+myfile, "r")
        for line in fr:
            data = line.split(" ")
            pm = float(data[2].replace('%', ''))
            pf = float(data[5].replace('%', ''))
        fr.close
        return pm, pf

    
    
    #function to calculate influx of people
    def calculator(self):
        M_count = 0
        F_count = 0
        #list of results
        results_list = os.listdir(self.results_dir)
        for i in range(0, len(results_list)):
            pm, pf = self.results_reader(results_list[i])
            if pm > pf:
                M_count += 1
            else:
                F_count += 1
        print('\n\n\n\n!!!!\tInflux of people consists of ' + str(M_count) + ' men and ' + str(F_count) + ' women\t!!!!')