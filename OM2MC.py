import sys
import json
import requests
import logging
from datetime import datetime
from datetime import timedelta
import dex
import OMdata as ommc

#called as main method below
def runEmailLink():
    yesterday = datetime.now()  - timedelta (days=1)
    today = datetime.now()

    res = ommc.getSurveyAllData(yesterday, today)
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

    print mailchimpBatch


def printSurveyNameList(): 
    yesterday = datetime.now() - timedelta (days=1)
    today = datetime.now()

    res = ommc.getSurveyAllData(yesterday, today)
    resObject = res.json()

    for survey in resObject: 
        print '{} {}'.format(survey['Name'], survey['Id'])



if __name__ == "__main__":
    logging.basicConfig(filename='ombridge.log',level=logging.INFO)
    logging.info('RUN on {0}'.format(datetime.now().strfttime('%c')))
    runEmailLink()
