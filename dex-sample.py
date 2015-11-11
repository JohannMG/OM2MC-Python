"""
    Keys and passwords for the Opinion Meter and Mailchimp
    Called dex for rolodex auth is used and 'password-file.txt' is silly

    this in an example with fake keys for GitHub sake
"""

import mailchimp

omUser = 'userlogin'
omPass = 'passwordd'

mailchimpList = 'xxxxxxxxxx'

# Edit the merge tags for all Mailchimp additions here:
def mailchimp_merge_tags(): 
    return {
        'METER' : 'Opinion Meter'
    }

# Edit the location merge tag for Mailchimp additions here:
def GET_Mailchimp_Location_Tag(): 
    return "LOC"

 
# surveryID : Name to go into above location Merge Tag 
Mailchimp_Location_Ids = {
    00010 : "Baltimore", 
    00004 : "Baltimore",
    48654 : "Gatlinburg",
    54458 : "Gatlinburg", 
    78954 : "BION",
    13248 : "Orlando", 
    96345 : "Orlando"


}

#other vars to look for AND how to look for it
# <Mailchimp Merge Tag> : {strings, to, find, it}
#case insensitive

def getMailchimpOtherMergeVars():
    return {
        'ZIPPOSTAL': ['zip', 'zipcode', 'postal'],
    }

def get_mailchimp_api():
    return mailchimp.Mailchimp('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-us1')

def getLocationName(id):

    try:
        name = Mailchimp_Location_Ids[id]
        return name
    except:
        name = ""

    return ""




