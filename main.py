import MSUtils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DF = df = pd.read_csv('rawDataMS.csv', delimiter=',', skiprows=2)
SAMPLE_COUNT = 3
elename = '50Cr'
sampleName = 'UndigCrF3' 

#Error calculation values
#n = 
#k = 





#Read in the raw data DF
sampleDict = MSUtils.createDict(df, 3)
#Remove NAN
df_removed_name = df.dropna(subset=['Run'])
df_removed_name.head(1)
#Trimmed dictionary 
trimmedDict = MSUtils.trimDictionary(sampleDict)
trimmedDict



#Getting the calibration curve 
calibrationDict = MSUtils.calibrationCurvesDict(trimmedDict)


xarr, yarr  = MSUtils.ccurve(elename, trimmedDict)[0], MSUtils.ccurve(elename, trimmedDict)[1]

xarr = xarr[1:]
yarr = yarr[1:]

elementConcentrationX = MSUtils.concentrationCalculation(trimmedDict, sampleName, elename)[0]
elementConcentrationY = MSUtils.concentrationCalculation(trimmedDict, sampleName, elename)[1]
xError = MSUtils.errorCalculation(MSUtils.ccurve(elename, trimmedDict)[2], 3, 12, MSUtils.ccurve(elename, trimmedDict)[3], xarr, yarr, elementConcentrationX, elementConcentrationY)[0]
yError = MSUtils.errorCalculation(MSUtils.ccurve(elename, trimmedDict)[2], 3, 12, MSUtils.ccurve(elename, trimmedDict)[3], xarr, yarr, elementConcentrationX, elementConcentrationY)[1]
MSUtils.cCurveWithSample(elename, trimmedDict, sampleName, elementConcentrationX, elementConcentrationY, xError, yError)







#Intercept and slope