# Testing script for survey_monkey_api.py and survey_access.py
# NOTE: Do not copy api key or access token into any python script! Create a
# text file in a different directory with the api key on line 1 and the
# access token on line 2

from survey_access import *

# ########### #
# Definitions #
# ########### #
local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
my_dict = {"price": 542.23, "name": "ACME", "shares": 100, 'names':
           ['steve', 'sara', 'bob']}
survey1 = '47476967'
survey2 = '46658731'
survey3 = '48173850'
survey_id = '46772574'
respondent_fields = ['ip_address']
survey_fields = ['title', 'date_created', 'question_count', 'num_responses']

# ################# #
# Create api object #
# ################# #

auth = credentials(local_file)
api = ApiService(auth['key'], auth['token'])

# ########### #
# Survey list #
# ########### #

# data = {'fields': survey_fields}
# survey_list = api.get_survey_list(data)
# api.save_survey_list(field_list=survey_fields)

# ######### #
# Responses #
# ######### #

respondent_ids = get_respondent_ids(survey_id, local_file)
data = {'survey_id': survey_id, 'respondent_ids': respondent_ids[:11]}
responses = api.get_responses(data)
print(json.dumps(responses, sort_keys=True, indent=2))
