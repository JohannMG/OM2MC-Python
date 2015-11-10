import sys
import json
import requests
from datetime import datetime
from datetime import timedelta
import dex
import OMdata as ommc


if __name__ == "__main__":
    runEmailLink()

def runEmailLink():
    yesterday = datetime.now()  - timedelta (days=1)
    today = datetime.now()

    res = ommc.getSurveyAllData(yesterday, today)
    resObject = res.json()

    mergevars = dex.getMailchimpOtherMergeVars() 
    ''' e.g.: {  'POSTAL': ['zip', 'zipcode', 'postal']  }'''
    
    for survey in resObject: 
        print survey['Name']
        emailIndex = ommc.getEmailQuestionIndex(survey)
        if emailIndex == None:
            continue; 

        mergedict = {}
        for m in mergevars.keys():
            mmIndex = ommc.getQuestionIndexFromStrings(survey, mergevars[m])
            if mmIndex != None: 
                mergedict[mmIndex] = m
        

def printSurveyNameList(): 
    yesterday = datetime.now() - timedelta (days=1)
    today = datetime.now()

    res = ommc.getSurveyAllData(yesterday, today)
    resObject = res.json()

    for survey in resObject: 
        print '{} {}'.format(survey['Name'], survey['Id'])



