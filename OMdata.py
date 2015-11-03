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
	add docs in a few
'''
def getSurveyAllData(startDate, endDate):
	apiUrl = 'https://www.opinionmeter.com/OMDataExchangeRestAPI/api/Survey/GetMultipleSurveyDetailsByDate/'
	headers = {'Content-Type': 'application/json'}
	params = {}
	paramsAddToUrl = "";

	surveysFromAPI = getSurveyList()
	for i in surveysFromAPI:
		paramsAddToUrl += 'Survey_LocId' + '=' + str( i['SurveyId'] ) + ';' + str( i['LocationId'] );
		paramsAddToUrl += '&' 

	params['StartDate'] = startDate.strftime('%m/%d/%Y');
	params['EndDate'] = endDate.strftime('%m/%d/%Y');

	


if __name__ == "__main__":
    getSurveyAllData( datetime.now() - timedelta (days=2), datetime.now()  )


