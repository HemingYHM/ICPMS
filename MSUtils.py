import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

#This function imports the file, and skips the first numsSkip rows
def importFile(fileName, numSkip):
    return pd.read_csv(fileName, delimiter=',', skiprows=numSkip)

#This function imports the file, without skipping the first rows
def imrportFileWithHeader(fileName):
    return pd.read_csv(fileName, delimiter=',')




#This function keeps track of how many different samples are run
#Count the amout of "Average counts from 3 runs" in "Run" column
#Probably useless function, but I'll keep it here for now
def countSamples(df):
    sampleCount = 0
    for i in df['Run']:
        if i == 'Average counts from 3 runs':
            sampleCount += 1
    return sampleCount

#Create a dictionary of dictionaries, where the keys are the sample names, and the values are the dataframes of the sample
#Loop through the rows, whenever the the third column contians a string with the string PM or AM in it, extract out the unique sample name

def createDict(df, sampleRunCount):
    sampleDict = {}
    #print the name of column 3 
    col3 = df.columns[2]
    for i in range(len(df)):
        if type(df[col3][i]) == str:
            if 'PM' in df[col3][i] or 'AM' in df[col3][i]:
                sampleDict[df[col3][i]] = df.iloc[i:i+ sampleRunCount + 3]
    return sampleDict


#Loop through the keys to change the key name, the key name is the sample name, but it also contains the date and time, which is not needed
#Key looks like [TEXTEXTEXT 4/24/2023 5:24:50 PM]
#Remove latter parts
#Create a new dictionary with the same value, but new keys

def trimDictionary(sampleDict):
    newDict = {}
    #Cant split by spaces because some name has spaces in it
    #Loop through the 
    for i in sampleDict.keys():

        match = re.match(r'.+?(?=/)', i)
        word = match.group(0)
        #Remove the last index, and replace all spaces with nothing
        word = word[:-1].replace(' ', '')
        #add to new dict
        newDict[word] = sampleDict.get(i)

    return newDict



#Create a new dictionary where only names includng PPM is included, with the same value
def calibrationCurvesDict(sampleDict):
    calibrationCurvesdict = {}
    for i in sampleDict.keys():
        if 'ppm' in i:
            match = re.match(r'.+?(?=ppm)', i)
            word = match.group(0)

            
            calibrationCurvesdict[word] = sampleDict.get(i)
    return calibrationCurvesdict


def fixSyntax(dataFrame):
    return dataFrame.dropna(subset=['Run'])


#Each value in the diciontary is a pandas table with 6 rows of information, with the last 3 being the average counts, standard deviation, and %RSD
#Create objects for each sample, with the name, average counts, standard deviation, and %RSD

#Sample Dict is from CREATEDICTI function !!!!!!
def extractColumnEleNames(sampleDict):
    for i in sampleDict.keys():
        elelist = sampleDict.get(i).columns[2:].tolist()
        break
    return elelist

def extractCalibrationName(trimmedDict):
    a = []
    for i in trimmedDict.keys():
        if 'ppm' in i:
            a.append(i)

    return a 
        

def ccurve(eleName, trimmedDict):
    calibrationSampleNames = extractCalibrationName(trimmedDict)
    xarr = []
    yarr = []
    #This loop gets the calibration x numbers out of the array 
    for ppmNames in calibrationSampleNames:
        match = re.match(r'^(.*?)(p|$)', ppmNames)
        if match:
            xarr.append(float(match[1]))
    for ppmNames in calibrationSampleNames:
        #Potential bug: the iloc4 might not awlasy be the average !!
        a = float(trimmedDict.get(ppmNames).iloc[4][eleName].replace(' ', '').replace(',', ''))
        yarr.append(a)
    #record the mx + b and return later

    coef = np.polyfit(xarr,yarr,1)
    poly1d_fn = np.poly1d(coef) 
    slope = coef[0]
    intercept = coef[1]
    #Have a caption box with slope and intercept at the UPPER corner with a box around it
    #plt.text(0.5, 0.5, 'Slope: ' + str(slope) + '\n' + 'Intercept: ' + str(intercept), bbox=dict(facecolor='red', alpha=0.5))
    #plt.plot(xarr, yarr, 'yo', xarr, poly1d_fn(xarr), '--k')


    #plt.title("Calibration Curve for " + eleName)
    #plt.ylabel("Average Counts from 3 runs")
    #return (slope, intercept)
    return xarr, yarr, slope, intercept



def concentrationCalculation(trimmedDict, sampleName, element):

    curve = ccurve(element, trimmedDict)
    #Find the sample name in the trimmedDict and get the average counts
    y = float(trimmedDict.get(sampleName).iloc[4][element].replace(' ', '').replace(',', ''))
    #given the Y, find the X
    x = (y- curve[3]) / curve[2]
    return x, y



def errorCalculation(m,k,n, intercept, xarr,yarr, elementConcentraionX, elementConcentrationY):
    #M is slope 
    #k is number of replicate measurements of the unknown
    #n is number of replicate measurements of the calibration curve
    #xarr is the x values of the calibration curve
    #yarr is the y values of the calibration curve
    #fix can't multiply sequence by non-int of type 'numpy.float64'
    #DEFINITLY SOMETHING WRONG WITH THE ERROR CALCULATION CONSULT WITH GURUS ON SEP 20!
    m = float(m)
    k = float(k)
    n = float(n)
    S_y = 0
    S_x = 0
    yCurve = []
    for i in xarr:
        yCurve.append(m*i + intercept)
    
    ydiffSquared = []
    for i in range(len(yarr)):
        ydiffSquared.append((yarr[i] - yCurve[i])**2)
    xsquareDiff = []
    for i in range(len(xarr)):
        xsquareDiff.append((xarr[i] - np.mean(xarr))**2)

    xdiffSQ = np.sum(xsquareDiff)
    ydiffSQ = np.sum(ydiffSquared)
    


    S_y = np.sqrt(ydiffSQ / (n - 2))
    S_x = (S_y/abs(m))*np.sqrt( (1/k) + (1/n) + ( ydiffSQ/(m**2)*xdiffSQ   )       )


    return S_x, S_y




def cCurveWithSample(eleName, trimmedDict, sampleName, sampleFittedX, sampleFittedY, xError, yError):
    calibrationSampleNames = extractCalibrationName(trimmedDict)
    xarr = []
    yarr = []
    #This loop gets the calibration x numbers out of the array 
    for ppmNames in calibrationSampleNames:
        match = re.match(r'^(.*?)(p|$)', ppmNames)
        if match:
            xarr.append(float(match[1]))
    for ppmNames in calibrationSampleNames:
        #Potential bug: the iloc4 might not awlasy be the average !!
        a = float(trimmedDict.get(ppmNames).iloc[4][eleName].replace(' ', '').replace(',', ''))
        yarr.append(a)
    #record the mx + b and return later

    coef = np.polyfit(xarr,yarr,1)
    poly1d_fn = np.poly1d(coef) 
    slope = coef[0]
    intercept = coef[1]
    #Have a caption box with slope and intercept at the UPPER corner with a box around it
    plt.plot(xarr, yarr, 'yo', xarr, poly1d_fn(xarr), '--k')
    plt.plot(sampleFittedX, sampleFittedY, 'ro')


    #Legend to show dotted line is the calibration curve, slope and intercept, as well as the calculated errors
    plt.legend(['Standard Points', 'Sample', "Fitted Sample" + '\n' + 'X Error: ' + str(xError) + '\n' + 'Y Error: ' + str(yError)])


    print("Current X values are " + str(xarr), "which are the standard ppm values")
    print("Current Y values are " + str(yarr), "which are the average counts from 3 runs")
    print("The fitted sample is " + sampleName + " with the fitted X value of " + str(sampleFittedX) + " and concentration value of " + str(sampleFittedY))

    plt.title("Calibration Curve for " + eleName)
    plt.ylabel("Average Counts from 3 runs")
    plt.show()






def tableFormatter(trimmedDict, numRuns, df):
    colnames = df.columns[2:].insert(0, 'ele')
    
    transformed = pd.DataFrame(columns = colnames)
    for keys in trimmedDict.keys():
        for i in range(numRuns):
            a = trimmedDict.get(keys).iloc[1 + i][2:].tolist()
            
            a.insert(0, keys)
            transformed.loc[keys + ' run ' + str(i)] = a
            


    return transformed

