import requests
import dex
import json
from requests.auth import HTTPBasicAuth
import datetime
from datetime import *
import base64


baseApiUrl = 'https://www.opinionmeter.com/OMDataExchangeRestAPI/api/Survey/'
authHeader = HTTPBasicAuth(dex.omUser, dex.omPass)

"""
    pass no arguments
    returns a array of dictionaries for each survey+location
"""
def getSurveyList():
    try: 
        url = 'https://www.opinionmeter.com/OMDataExchangeRestAPI/api/Survey/GetSurveyList/' 
        headers = {'Content-Type': 'application/json'}
        req = requests.get(url, headers = headers, auth=authHeader)
        res = req.json()

        if res['ErrorMessage'] == None: 
            return res['ListSurvey']
        else: 
            print 'Error returned ' + res['ErrorMessage']
            return None
    except:
        print ('Error getting the survey list from the opinion meter api')
        return None


'''
    Pass the range (API max is about 60 days. Not tested, but script should only run 1-day range)
    startDate : Python datetime object
    endDate : Python datetime object

    NOTE:  it's not in the Opionion Meter documentation, but endDate is NON exclusive
            in fancier notation: [startDate, endDate)

    uses getSurveyList() and calls ALL active locations > This is a SLOW method. 10-120s depending on range and size

    returns: response object  [http://docs.python-requests.org/en/latest/]
'''
def getSurveyAllData(startDate, endDate):
    apiUrl = 'https://www.opinionmeter.com/OMDataExchangeRestAPI/api/Survey/GetMultipleSurveyDetailsByDate/'
    headers = {'Content-Type': 'application/json'}
    params = {}
    paramsAddToUrl = "";

    surveysFromAPI = getSurveyList()
    for i in surveysFromAPI:
        paramsAddToUrl += 'Survey_LocId' + '=' + str( i['SurveyId'] ) + ';' + str( i['LocationId'] )
        paramsAddToUrl += '&' 

    params['StartDate'] = startDate.strftime('%m/%d/%Y')
    params['EndDate'] = endDate.strftime('%m/%d/%Y')

    apiUrl = apiUrl + '?' + paramsAddToUrl

    try:
        res = requests.get(apiUrl, params=params , auth=authHeader, timeout=240)
    except Exception, e:
        print 'Error with Getting all Survey Data'
        raise e

    return res


'''
    Pass proper email dict to method as described in the Mailchimp API v2 docs for batch-subscribe
    https://apidocs.mailchimp.com/api/2.0/lists/batch-subscribe.php

    batch = [
        {
            'email': {'email': 'hello@johannmg.com'},
            'email_type': 'html', 
            'merge_vars': {
                'MMERGE1': 'value',
                'CAMPAIGN' : 'opinionmeter'
            }
        }, 
        {//etc...}
    ]

    Run daily, this should be a pretty small call for Mailchimp. < 7 seconds 
    Uses the Mailchimp package, requires: API Key + ListId to be in dex/keys file
         Mailchimp method -> def batch_subscribe(self, id, batch, double_optin=True, update_existing=False, replace_interests=True):
    will also print out success and errors (now to console. TODO: later to a log file)

    return boolean True if successful
'''

def subcribeNewUsers(batchList):
    try: 
        mc = dex.get_mailchimp_api()
        res = mc.lists.batch_subscribe(dex.mailchimpList, batchList, double_optin= True, update_existing=True)
        print 'Added {0} new email(s), {1} update(s) to Mailchimp. {2} Error(s)'.format(res['add_count'], res['update_count'] ,res['error_count'])

        for item in res['adds']:
            print 'added: {0}'.format(item['email'])
        for item in res['updates']:
            print 'updated: {0}'.format(item['email'])
        for item in res['errors']:
            print '{0}: {1}, {2}'.format(item['email'],  item['code'], item['error'])

        return True
    except Exception, e:
        print 'Error Batch Adding to Mailchimp'
        print e
        return False

"""
    Provide the returned survey struct from opinionmeter, will return the QuetionID where email is likely found
    {ErrorMessage: ..., Name:"", QUES... }
    return: NUMBER(None if not found)
"""

def getEmailQuestionID(survey):
    questions = survey["LNGS"][0]["QUES"]

    for question in questions: 
        if question['Type'] != 7: 
            continue
        if question['IsHiddenQues'] == True: 
            continue
        if ('EMAIL' in question['Text'].upper() or 'E-MAIL' in question['Text'].upper()): 
            return question['Id']

    print None

"""
    Provide the returned survey struct from opinionmeter, will return the QuetionID where email is likely found
    {ErrorMessage: ..., Name:"", QUES... }
    return: NUMBER (None if not found) representing the index of the question
"""

def getEmailQuestionIndex(survey):
    questions = survey["LNGS"][0]["QUES"]
    for index, question in enumerate(questions):
        if question['Type'] != 7: 
            continue
        if question['IsHiddenQues'] == True: 
            continue
        if ('EMAIL' in question['Text'].upper() or 'E-MAIL' in question['Text'].upper()): 
            return index
    return

"""
    Provide the returned survey struct from opinionmeter, 
    will return the first QuetionID where ANY of the keys are found in the question text
    {ErrorMessage: ..., Name:"", QUES... }
    return: NUMBER (None if not found)
"""

def getQuestionIdFromStrings(survey, *strings):
    questions = survey["LNGS"][0]["QUES"]

    for question in questions:
        if question['Type'] != 7:
            continue 

        for key in strings:
            if key in question['Text']:
                return question['Id']

    return None

"""
    arg1: provide the returned survey struct from opinionmeter, 
    will return the first index of the question where ANY of the keys are found in the question text
    {ErrorMessage: ..., Name:"", QUES... }
    arg2: provide an array with all the strings to identify the field by
    return: NUMBER (None if not found)
"""

def getQuestionIndexFromStrings(survey, strings):
    questions = survey["LNGS"][0]["QUES"]

    for index, question in enumerate(questions):
        for key in strings: 
            if key.lower() in question['Text'].lower(): 
                return index
    return None

"""
    arg 1: entire array from each location response in the OM API 
        e.g. {ErrorMessage: '', IdSpecified: , Name, Id, SurveyResponses, ...}
    arg 2: Question ID that contains email
    arg 3+: send extraction vars as a dictionary with NAME and the QuestionID to fetch it from
        {7 = 'zip'}

    returns: array with emails + extracted merge tags
    [{
        'email': 'emailema@il.com'
        'merge_vars': { 'ZIP': 62378, LOCATION: 'B'}   #from the passed in args
        'email_type': 'html'
    ]
"""

def extractFieldsFromResponses(survey, emailQuestionIndex, mergeDict ): 
    indicesToCheck = mergeDict.keys()
    capturedData = []
    locationName = dex.getLocationName(survey['Id']);

    surveyResponses = survey['SurveyResponses'] #should be an array
    

    for response in surveyResponses: 
        #new user obj w/ embedded structs
        userObj = {}
        userObj['email'] = {}
        userObj['merge_vars'] = dex.mailchimp_merge_tags() #incl default merge tags

        extractedEmail = response['Responses'][emailQuestionIndex]['Res']

        if ( isinstance(extractedEmail, str) and len(extractedEmail) > 2): 
            extractedEmail = base64.decodestring(extractedEmail)
            userObj['email']['email'] = extractedEmail
        else: 
            #no email found, continue to next :(
            continue

        #add location tag set in dex.py 
        userObj['merge_vars'][dex.Mailchimp_Location_Tag] = locationName
        userObj['email_type'] = 'html'

        #get merge tags
        for indexOfTag, tag in enumerate (indicesToCheck):
            extracted = response['Responses'][tag]['Res']
            if (isinstance (extracted, str)): 
                extracted = base64.decodestring(extracted)
            userObj['merge_vars'][mergeDict[tag]] = extracted

        #if all went well, add to the returned oject array
        capturedData.append(userObj)
    #END FOR LOOP

    return capturedData

        
        

    


if __name__ == "__main__":
    print 'hi there'








