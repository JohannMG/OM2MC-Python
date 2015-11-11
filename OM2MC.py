import sys
import json
import requests
import logging
from datetime import datetime
from datetime import timedelta
import dex
import OMdata as ommc

'''
    called as main method below
    Note: [startDate, endDate) b/c the endDate is non-inclusive
'''
def runEmailLink(startDate, endDate):
    

    res = ommc.getSurveyAllData(startDate, endDate)
    resObject = res.json()

    mergevars = dex.getMailchimpOtherMergeVars() 
    ''' e.g.: {  'POSTAL': ['zip', 'zipcode', 'postal']  }'''
    
    mailchimpBatch = []

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
        
        
        extracted = ommc.extractFieldsFromResponses(survey, emailIndex, mergedict) 
        mailchimpBatch = mailchimpBatch + extracted
    ommc.subcribeNewUsers( mailchimpBatch )


def printSurveyNameList(): 
    today = datetime.now()

    #no gap, just to get list info
    res = ommc.getSurveyAllData(today, today)
    resObject = res.json()

    for survey in resObject: 
        print '{} {}'.format(survey['Name'], survey['Id'])

def runForLength(daysPrevious):
    start = datetime.now() - timedelta(days=daysPrevious)
    end = datetime.now()

    runEmailLink(start, end)


if __name__ == "__main__":
    logging.basicConfig(filename='ombridge.log',level=logging.INFO)
    logging.info('RUN on {0}'.format(datetime.now().strftime('%c')))

    yesterday = datetime.now()  - timedelta (days=1)
    today = datetime.now()

    runEmailLink(yesterday, today)
