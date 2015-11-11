import OMdata
import dex
import requests
import json


"""
    Tests for OMdata.py
"""

def TESTgetSurveyList(): 

    results = OMdata.getSurveyList
    if (results != None):
        print 'getSurveyList() [PASSES]'
    else:
        print 'getSurveyList() [FAILED]'

def TESTgetEmailQuestionID():
    sur = {
        'LNGS': [
            {'QUES' : [
                    {'Id': 'wrong', 'Type': 7, 'Text': 'lorem ip', 'IsHiddenQues': False},
                    {'Id': 'wrong 2', 'Type': 5, 'Text': 'ringdingdingding', 'IsHiddenQues': False},
                    {'Id': 'correct', 'Type': 7, 'Text': 'I want email please', 'IsHiddenQues': False}
                ]
            }
        ]    
    }

    results = OMdata.getEmailQuestionID(sur)

    if (results == 'correct'): 
        print 'getEmailQuestionID() [PASSES]'
    else:
        print 'getEmailQuestionID() [FAILS]'

def TESTgetQuestionIdFromStrings(): 
    sur = {
        'LNGS': [
            {'QUES' : [
                    {'Id': 'wrong', 'Type': 7, 'Text': 'lorem ip', 'IsHiddenQues': False},
                    {'Id': 'wrong 2', 'Type': 5, 'Text': 'ringdingdi email ngding', 'IsHiddenQues': False},
                    {'Id': 'correct', 'Type': 7, 'Text': 'I want zip please', 'IsHiddenQues': False}
                ]
            }
        ]    
    }

    results = OMdata.getQuestionIdFromStrings(sur, 'zip', 'postal')

    if (results == 'correct'): 
        print 'getQuestionIdFromStrings() [PASSES]'
    else:
        print 'getQuestionIdFromStrings() [FAILS]'

def TESTgetEmailQuestionIndex():
    sur = {
        'LNGS': [
            {'QUES' : [
                    {'Id': 'wrong', 'Type': 7, 'Text': 'lorem ip', 'IsHiddenQues': False},
                    {'Id': 'wrong 2', 'Type': 5, 'Text': 'ringdingdingding', 'IsHiddenQues': False},
                    {'Id': 'correct', 'Type': 7, 'Text': 'I want email please', 'IsHiddenQues': False}
                ]
            }
        ]    
    }

    results = OMdata.getEmailQuestionIndex(sur)

    if (results == 2): 
        print 'getEmailQuestionIndex() [PASSES]'
    else:
        print 'getEmailQuestionIndex() [FAILS]'

def TESTgetQuestionIndexFromStrings():
    sur = {
        'LNGS': [
            {'QUES' : [
                    {'Id': 'wrong', 'Type': 7, 'Text': 'lorem ip', 'IsHiddenQues': False},
                    {'Id': 'wrong 2', 'Type': 5, 'Text': 'ringd zip dingding', 'IsHiddenQues': False},
                    {'Id': 'correct', 'Type': 7, 'Text': 'I want fjksd please', 'IsHiddenQues': False}
                ]
            }
        ]    
    }

    results = OMdata.getQuestionIndexFromStrings(sur, ['hnksf', 'zip'])

    if (results == 1): 
        print 'getQuestionIndexFromStrings() [PASSES]'
    else:  
        print 'getQuestionIndexFromStrings() [FAILS]'


def TESTextractFieldsFromResponses():
    surveySample = {
    "Id" : 48688, 
    "SurveyResponses": [
        {
            "SurveyResponseID": 1618161487,
            "Responses": [
                { "QId": 01561156, "Res": "dGVzdEB0ZXN0dHQuY29t"},
                { "QId": 1564, "Res": "0000"},
                { "QId": 456, "Res": "NDMyODc="}
            ]
        }, 
        {
            "SurveyResponseID": 4878456,
            "Responses": [
                { "QId": 445, "Res": "dGhpc0B0aGlzLmNvbQ=="},
                { "QId": 111222, "Res": "4444"},
                { "QId": 78, "Res": ""}
            ]
        }
    ]
}

    results = OMdata.extractFieldsFromResponses(surveySample, 0, {2:'ZIP'})


    '''should return:
    [
        {
            'merge_vars': {
                'LOCATION': 'Baltimore', 
                'zip': '43287'
            }, 

            'email': {'email': 'test@testtt.com'}, 
            'email_type': 'html'
        }, 
        {
            'merge_vars': {
                'LOCATION': 'Baltimore', 
                'zip': ''
            }, 

            'email': {'email': 'this@this.com'}, 
            'email_type': 'html'
        }
    ]
    '''

    if ( results[0]['merge_vars']['ZIP'] == '43287' and 
            results[1]['email']['email'] == 'this@this.com'):
        print 'OMdata.extractFieldsFromResponses() [PASSES]'
    else: 
        print 'OMdata.extractFieldsFromResponses() [FAILS]'


# def TESTgetEmailQuestionIndex(): 
#     res = requests.get('http://www.ripleys.com/test.json')
#     resObj = res.json()

#     for sur in resObj:
#         print sur['Name']
#         emailIndex = OMdata.getEmailQuestionIndex(sur)
#         print emailIndex

"""
    TESTS FOR dex.py
"""
def TESTgetLocationName(): 
    result = dex.getLocationName(48688)

    if (result == 'Baltimore'):
        print 'dex.getLocationName() [PASSES]'
    else:
        print 'dex.getLocationName() [FAILS]'





if __name__ == "__main__":    
    #OMdata
    print 'TESTS for OMdata.py ---------'
    TESTgetEmailQuestionID()
    TESTgetSurveyList()
    TESTgetQuestionIdFromStrings()
    TESTgetEmailQuestionIndex()
    TESTgetQuestionIndexFromStrings()
    TESTextractFieldsFromResponses()
    TESTgetEmailQuestionIndex()

    #dex
    print 'TESTS for dex.py-------------'
    TESTgetLocationName()