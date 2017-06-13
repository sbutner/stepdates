import os
import time
import pandas as pd

import secret

#for each folder in TLG Reports
        #validate folder is a customer folder
            #valid folders have iReview, Final Review and Final Invoice Review folders
        #for each month in customer folder
                #grab the step 1 date: iReview folder creation
                    #exclude the iReview folders made on run of step 3
                #assume step 2 same day as step 3 
                #grab the step 3 date: Final Invoice Review file ctime OR iReview folder parsing
                #grab the step 4 date: Final Review file ctime
        #return the CUSTOMER_NAME|MONTH|STEP|DATE collected above
#return a table of CUSTOMER_NAME|MONTH|STEP|DATE
#print table as csv


def walkThroughFolders(root):
    stageDatesResults = pd.DataFrame()
    for path in os.listdir(root):
        if validateFolder(root+path):
            stageDatesResults = stageDatesResults.append(compileCustomer(path))
    return stageDatesResults

def validateFolder(path):
    if os.path.isdir(path):
        return (secret.VALID_SUBFOLDER in os.listdir(path))

def compileCustomer(path):
    customerName = path
    path = secret.ROOT_PATH + customerName
    customerResults = pd.DataFrame({'customerName' : customerName,
                                    'firstStage' : getFirstStage(path),
                                    'thirdStage' : getThirdStage(path),
                                    'fourthStage' : getFourthStage(path)})
    return customerResults

def getFirstStage(path):
    path = path+'prior months/'
    dates = [file for file in os.listdir(path) if isReviewSheet(file, "First")]
    dates = {(file[0:5],getTime(path+file)) for file in dates}
    return dates

def getThirdStage(path):
    path = path+'Final Invoice Review'
    dates = {(file[0:5],getTime(file) for file in os.listdir(path) if isReviewSheet(file, "Third")}
    return dates    

def getFourthStage(path):
    path = path+'ireview'
    dates = {(folder[0:5],parseDate(folder)) for folder in os.listdir(path)}
    return dates

def parseDate(folder):
    month, day, year, time = (folder[8:10], folder[11:13], folder[14:18],folder[20:])
        if (int(time) < 600):
                day = int(day) - 1
    dateString = month+'/'+str(day)+'/'+year
    return dateString

def isReviewSheet(path, stage):
    if stage == "First":
        return '.xls' in path and ' - Final' not in path
    else if stage == "Third":
        return '.xls' in path and ' - Final Invoice Review' in path        
    else if stage == "Fourth":
        return '.xls' in path and ' - Final' in path
def getTime(path, mode="c"):
    if (mode == "c" or mode == "created"):
        date = time.gmtime(os.path.getctime(path))
    else:
        date = time.gmtime(os.path.getmtime(path))
    if (date[3] < 7):
        day = date[2] - 1
    else:
        day = date[2]
    strDate = str(date[1])+'/'+str(day)+'/'+str(date[0])
    return strDate

if __name__ == "__main__":
    walkThroughFolders(secret.ROOT_PATH).to_csv()
