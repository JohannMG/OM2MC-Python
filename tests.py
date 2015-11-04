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



if __name__ == "__main__":    
    TESTgetEmailQuestionID();
    TESTgetSurveyList();
    TESTgetQuestionIdFromStrings();