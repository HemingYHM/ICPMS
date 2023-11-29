import MSUtils as msu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
    #Import the file
    df = msu.importFile('rawDataMS.csv', 2)
    sampleDict = msu.createDict(df, 4)
    trimmedDict = msu.trimDictionary(sampleDict)
    

    #graph mode, argv[1] is the is G 
    if sys.argv[1] == '-G':
        #To be fixed later to take input -S from the formatted table and eventaully use the concentration calculation to find the concentration
        #However, the old methods uses raw data to compute
        #TODO: make this take in the formatted table rather than raw
        calibrationCurve = msu.calibrationCurvesDict(trimmedDict)
        elename = sys.argv[2]
        sampleName = sys.argv[3]
        xarr, yarr  = msu.ccurve(elename, trimmedDict)[0], msu.ccurve(elename, trimmedDict)[1]
        elementConcentrationX = msu.concentrationCalculation(trimmedDict, sampleName, elename)[0]
        elementConcentrationY = msu.concentrationCalculation(trimmedDict, sampleName, elename)[1]
        xError = msu.errorCalculation(msu.ccurve(elename, trimmedDict)[2], 3, 12, msu.ccurve(elename, trimmedDict)[3], xarr, yarr, elementConcentrationX, elementConcentrationY)[0]
        yError = msu.errorCalculation(msu.ccurve(elename, trimmedDict)[2], 3, 12, msu.ccurve(elename, trimmedDict)[3], xarr, yarr, elementConcentrationX, elementConcentrationY)[1]
        msu.cCurveWithSample(elename, trimmedDict, sampleName, elementConcentrationX, elementConcentrationY, xError, yError)
    
    if sys.argv[1] == '-S':
        
        a = msu.tableFormatter(trimmedDict, int(sys.argv[2]), df)
        #Export the a to a csv file
        a.to_csv('output.csv')
        print("The output has been saved to output.csv")




main()



    


