import sys
import OMdata as ommc
import response
import datetime
from datetime import timedelta

if __name__ == "__main__":

	yesterday = datetime.now()  - timedelta (days=1)
	today = datetime.now()

    res = ommc.getSurveyAllData(yesterday, today)
    print res