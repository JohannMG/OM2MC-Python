import OMdata


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
                    {'Id': 'wrong', 'type': 7, 'text': 'lorem ip', 'IsHiddenQues': False},
                    {'Id': 'wrong 2', 'type': 5, 'text': 'ringdingdingding', 'IsHiddenQues': False},
                    {'Id': 'correct', 'type': 7, 'text': 'I want email please', 'IsHiddenQues': False}
                ]
            }
        ]    
    }

    results = OMdata.getEmailQuestionID(sur)

    if (results == 'correct'): 
        print 'getEmailQuestionID() [PASSES]'
    else:
        print 'getEmailQuestionID() [FAILS]'



if __name__ == "__main__":
    TESTgetEmailQuestionID();
    TESTgetSurveyList();