# See bootcamp_eval.py for detailed explanation of steps
# from survey_monkey_api import *
from variables import *
from survey_access import *
import csv

# 1: Generate a current list of all surveys associated with account
local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
auth = credentials(local_file)
api = ApiService(auth['key'], auth['token'])
# field_list = ['title', 'date_created', 'date_modified','language_id',
#               'question_count', 'num_responses']
# api.save_survey_list(field_list=field_list)

# 2: Get the relevant survey id from the survey list
survey_id = '71496549' # survey for part 1
survey_id = '71783041' # survey for part 2
# NEED A WAY TO COMBINE DATA FROM TWO SURVEYS INTO ONE SET OF DETAILS
# AND QUESTIONS IN PART 3

# 3: Get survey details and questions and save to a text file for reference
data = {'survey_id': survey_id}
details = api.get_survey_details(data)
with open('survey_details.txt', 'w') as file:
    file.write(json.dumps(details, sort_keys=True, indent=2))

questions = get_questions(survey_id, local_file)
with open('survey_questions.txt', 'w') as file:
    file.write(json.dumps(questions, sort_keys=True, indent=2))

# 4: Create variables from survey monkey questions
# All variables require a description and a question id.  This maps your
# variable to the survey question.  Optional parameters include the specific
# answer id and a reference dictionary, depending on the type of question.
# Reference dictionaries must be defined before the variable object that
# will use it as a parameter.

varlist = []

question_ids = []
for var in varlist:
    if var.question not in question_ids:
        question_ids.append(var.question)

# 5: Get responses for the subset of questions in question_ids for all
# respondents of the survey (no need to batch since all can be obtained with
# one api call
respondent_ids = get_respondent_ids(survey_id, local_file)
responses = get_survey_data(survey_id, local_file, respondent_ids)
res_data = {}
for respondent in responses["data"]:
    temp = [question for question in respondent["questions"] if
            question.get("question_id") in question_ids]
    res_data[respondent.get("respondent_id")] = temp

# 6: Create a matrix of all the variable values and save it to a file.  This
# creates a file that you can then import into R (or other statistical tools)
# for data analysis.
res_ids = [respondent for respondent in res_data.keys()]
row = 0
matrix = []
for respondent in res_ids:
    row_data = [respondent]
    for variable in varlist:
        value = variable.get_value(res_data[respondent])
        if len(value) == 1:
            row_data.append(value[0])
        else:
            row_data.append(value)
    matrix.append(row_data)
    row += 1

header = ['respondent']
for variable in varlist:
    header.append(variable)

with open("survey_data.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows([header])
    writer.writerows(matrix)
