class mObject:
    def __init__(self, name, dict):
        self.name = name
        self.dict = {}


    def getName(self):
        return self.name
    
    def getAvg(self, sampleElement):
        return self.dict[sampleElement]['Average counts from 3 runs']
    
    def getStd(self,samepleElement):
        return self.dict[samepleElement]['Std. Deviation']

