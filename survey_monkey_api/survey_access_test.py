#Testing script for survey_monkey_api.py and survey_access.py
#NOTE: Do not copy api key or access token into any python script! Create a
#text file in a different directory with the api key on line 1 and the
#access token on line 2

from survey_monkey_api import *
from survey_access import *

###############
# Definitions #
###############
local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
my_dict = {"price": 542.23, "name": "ACME", "shares": 100, 'names':
           ['steve', 'sara', 'bob']}
survey1 = '47476967'
survey2 = '46658731'
survey3 = '48173850'
respondent_fields = ['ip_address']
survey_fields = ['title', 'date_created', 'question_count', 'num_responses']

#####################
# Create api object #
#####################

auth = credentials(local_file)
api = ApiService(auth['key'], auth['token'])

###############
# Survey list #
###############

#data = {'fields': survey_fields}
#survey_list = api.get_survey_list(data)
#api.save_survey_list(survey_fields)

##################
# Survey details #
##################

##data = {}
##data['survey_id'] = survey3
##survey_details = api.get_survey_details(data)

###Need to write a function to get question and answer ids

###################
# Respondent list #
###################

#data = {}
data = {'fields': respondent_fields}
data['survey_id'] = survey3
respondents = api.get_respondent_list(data)
respondent_ids = list_respondents(respondents)

#############
# Responses #
#############

#Will try setting respondent chunks to 100 instead of 10
data = {'survey_id': survey3, 'respondent_ids': respondent_ids}
responses = api.get_responses(data)
