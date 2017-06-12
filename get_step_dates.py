import os
import time

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
    for path in os.listdir(root):
        if validateFolder(root+path):
            #do something
    return #returnvalue

def validateFolder(path):
    if os.path.isdir(path):
        return not set(os.listdir(path)).isdisjoint(secret.VALID_SUBFOLDERS)
    

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
    pass
