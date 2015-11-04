import requests
import dex
import json
from requests.auth import HTTPBasicAuth
import datetime
from datetime import *


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
    except:
        print ('Error getting the survey list from the opinion meter api')


'''
    Pass the range (API max is about 60 days. Not tested, but script should only run 1-day range)
    startDate : Python datetime object
    endDate : Python datetime object

    uses getSurveyList() and calls ALL active locations > This is a SLOW method. 10-120s depending on range and size
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
        res = requests.get(apiUrl, params=params , auth=authHeader, timeout=60)
    except Exception, e:
        print 'Error with Getting all Survey Data'
        raise e

    return res.json(); 


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



if __name__ == "__main__":
    # print getSurveyAllData( datetime.now() - timedelta (days=2), datetime.now()  )
    batch = [
        {
            'email': {'email': 'hello@johannmg.com'},
            'email_type': 'html', 
            'merge_vars': {}
        }, 
        {
            'email': {'email': 'hubbard@ripleys.com'},
            'email_type': 'html', 
            'merge_vars': {}
        }, 
    ]
    subcribeNewUsers(batch)














