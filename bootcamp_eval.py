# from survey_monkey_api import *
from survey_access import *
from variables import *
import csv

# 1: Generate a current list of all surveys associated with account
# The purpose of this step is to obtain the survey id for the survey you
# will analyze.  You only need to do this step once, look up the survey id,
# and use it for many of the other methods.
local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
auth = credentials(local_file)
api = ApiService(auth['key'], auth['token'])
# field_list = ['title', 'date_created', 'date_modified','language_id',
#               'question_count', 'num_responses']
# api.save_survey_list(field_list=field_list)
survey_id = '68555146'  # this is the survey id for the survey we want

# 2: Get survey details and questions
# The survey details dictionary provides you with all the question ids and
# answer ids for each question in the survey. You will need some of this
# information to create variables based on the questions you want to analyze
data = {'survey_id': survey_id}
details = api.get_survey_details(data)
questions = get_questions(survey_id, local_file)

# 3: Save details and questions to a text file for reference
# This will save the details and questions in a nice format so you can
# easily look up the question and answer ids needed to create variables
with open('bootcamp_details.txt', 'w') as file:
    file.write(json.dumps(details, sort_keys=True, indent=2))
# with open('bootcamp_questions.txt', 'w') as file:
#     file.write(json.dumps(questions, sort_keys=True, indent=2))

# 4: Create variables from survey monkey questions
# All variables require a description and a question id.  This maps your
# variable to the survey question.  Optional parameters include the specific
# answer id and a reference dictionary, depending on the type of question.
# Reference dictionaries must be defined before the variable object that
# will use it as a parameter.
affil_ref = {
    '9353729936': 'WESIT Board',
    '9353729937': 'WESIT Director',
    '9353729938': 'SIG Intern',
    '9353729939': 'CEWIT Staff'
}
affiliation = Variable('affiliation with CEWIT', '844929038', ref=affil_ref)
tenure_ref = {
    "9352528143": "Less than 1 month",
    "9352528144": "1 to 3 months",
    "9352528145": "4 to 6 months",
    "9352528146": "7 to 9 months",
    "9352528147": "10 to 12 months",
    "9352528148": "More than 12 months"
}
tenure = Variable('time in leadership position', '844932258', ref=tenure_ref)
rating_ref = {
    "9356420609": "Very Poor",
    "9356420610": "Poor",
    "9356420611": "Fair",
    "9356420612": "Good",
    "9356420613": "Excellent",
    "9356420614": "I Did Not Attend"
}
resume = Variable('group resume icebreaker', "845200943", "9356420599",
                  ref=rating_ref)
colors = Variable('colors assessment', "845200943", "9356420600",
                  ref=rating_ref)
dinner = Variable('dinner with first lady', "845200943", "9356420601",
                  ref=rating_ref)
spaghetti = Variable('spaghetti towers', "845200943", "9356420602",
                     ref=rating_ref)
overview = Variable('cewit overview', "845200943", "9356420603",
                    ref=rating_ref)
engagement = Variable('engagement drivers', "845200943", "9356420604",
                      ref=rating_ref)
plane = Variable('plane wreck survival', "845200943", "9356420605",
                 ref=rating_ref)
student_needs = Variable('student interests', "845200943", "9356420606",
                         ref=rating_ref)
teams = Variable('team breakout sessions', "845200943", "9356420607",
                 ref=rating_ref)
callout = Variable('callout planning', "845200943", "9356420608",
                   ref=rating_ref)
facility_ref = {
    "9354866606": "Very Poor",
    "9354866607": "Poor",
    "9354866608": "Fair",
    "9354866609": "Good",
    "9354866610": "Excellent",
    "9354866611": "Not Applicable"
}
location = Variable('convenience of location', "845206534", "9354866599",
                    ref=facility_ref)
parking = Variable('convenience of parking', "845206534", "9354866600",
                   ref=facility_ref)
comfort = Variable('meeting room comfort', "845206534", "9354866601",
                   ref=facility_ref)
size = Variable('meeting room size', "845206534", "9354866602",
                ref=facility_ref)
food_dinner = Variable('quality of food friday', "845206534", "9354866603",
                       ref=facility_ref)
food_lunch = Variable('quality of food saturday', "845206534", "9354866604",
                      ref=facility_ref)
food_snack = Variable('quality of snacks', "845206534", "9354866605",
                      ref=facility_ref)
agree_ref = {
    "9361708380": "Strongly Disagree",
    "9361708381": "Disagree",
    "9361708382": "Neutral",
    "9361708383": "Agree",
    "9361708384": "Strongly Agree",
    "9361708385": "I Don't Know"
}
purpose = Variable('understanding of purpose', "846041464", "9361708372",
                   ref=agree_ref)
my_role = Variable('understanding of my role', "846041464", "9361708373",
                   ref=agree_ref)
other_role = Variable('understanding of others roles', "846041464",
                      "9361708374", ref=agree_ref)
needs = Variable('understanding of student needs', "846041464", "9361708375",
                 ref=agree_ref)
team = Variable('connected to team', "846041464", "9361708376", ref=agree_ref)
leadership = Variable('connected to leadership', "846041464", "9361708377",
                      ref=agree_ref)
effective = Variable('working effectively', "846041464", "9361708378",
                     ref=agree_ref)
decision = Variable('making decisions', "846041464", "9361708379",
                    ref=agree_ref)

varlist = [affiliation, tenure, resume, colors, dinner, spaghetti, overview,
           engagement, plane, student_needs, teams, callout, location,
           parking, comfort, size, food_dinner, food_lunch, food_snack,
           purpose, my_role, other_role, needs, team, leadership, effective,
           decision]

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

with open("bootcamp_data.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows([header])
    writer.writerows(matrix)
