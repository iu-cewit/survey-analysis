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
surveys = ['71496549', '71783041']  # evaluation surveys for parts 1 and 2

# 3: Get survey details and questions and save to a text file for reference
# with open('details.txt', 'w') as d, open('questions.txt', 'w') as q:
#     for survey_id in surveys:
#         data = {'survey_id': survey_id}
#         details = api.get_survey_details(data)
#         d.write(json.dumps(details, sort_keys=True, indent=2))
#         questions = get_questions(survey_id, local_file)
#         q.write(json.dumps(questions, sort_keys=True, indent=2))

# 4: Create variables from survey monkey questions
affil_ref = {
    "9596618678": "Other (please specify)",
    "9596618681": "PhD Student",
    "9596618682": "Faculty - Tenure Track",
    "9596618683": "Faculty - Non-Tenure Track",
    "9618195876": "Other (please specify)",
    "9618195879": "PhD Student",
    "9618195880": "Faculty - Tenure Track",
    "9618195881": "Faculty - Non-Tenure Track"
}
market_ref = {
    "9596717221": "Other (please specify)",
    "9596717224": "Invitation from CEWiT",
    "9596717225": "Departmental or organizational listserv",
    "9596717226": "eNewsletter from WESiT",
    "9596717227": "eNewsletter from GPSG",
    "9596717228": "SSRC Events page",
    "9596717229": "Email from peer/colleague",
    "9596717230": "Facebook",
    "9596717231": "Twitter",
    "9596717232": "Word of mouth",
    "9618195886": "Other (please specify)",
    "9618195889": "Invitation from CEWiT",
    "9618195890": "Departmental or organizational listserv",
    "9618195891": "eNewsletter from WESiT",
    "9618195892": "eNewsletter from GPSG",
    "9618195893": "SSRC Events page",
    "9618195894": "Email from peer/colleague",
    "9618195895": "Facebook",
    "9618195896": "Twitter",
    "9618195897": "Word of mouth"
}
agree_ref = {
    "9596648172": "Strongly Disagree",
    "9596648173": "Disagree",
    "9596648174": "Neutral",
    "9596648176": "Agree",
    "9596648177": "Strongly Agree",
    "9596648178": "I Don't Know",
    "9618206446": "Strongly Disagree",
    "9618206447": "Disagree",
    "9618206448": "Neutral",
    "9618206449": "Agree",
    "9618206450": "Strongly Agree",
    "9618206451": "I Don't Know"
}
rating_ref = {
    "9596660704": "Very Poor",
    "9596660705": "Poor",
    "9596660706": "Neutral",
    "9596660707": "Good",
    "9596660708": "Excellent",
    "9596660709": "I Don't Know",
    "9618264861": "Very Poor",
    "9618264862": "Poor",
    "9618264863": "Neutral",
    "9618264864": "Good",
    "9618264865": "Excellent",
    "9618264866": "I Don't Know"
}
gender_ref = {
    "9596674853": "Other (please specify)",
    "9596674856": "Female",
    "9596674857": "Male",
    "9596674858": "Prefer not to identify",
    "9618195922": "Other (please specify)",
    "9618195925": "Female",
    "9618195926": "Male",
    "9618195927": "Prefer not to identify"
}
site_ref = {
    "9618213269": "Yes",
    "9618213270": "No",
    "9618213271": "No"
}
p1_affil = Variable('attendee affiliation', '876032204', ref=affil_ref)
p1_market = Variable('marketing penetration', '876034750', ref=market_ref)
p1_useful = Variable('found material useful', '876036733', '9596648167',
                     agree_ref)
p1_new = Variable('covered new material', '876036733', '9596648168', agree_ref)
p1_info = Variable('has enough info to build site', '876036733', '9596648169',
                   agree_ref)
p1_build = Variable('plan to build site', '876036733', '9596648171', agree_ref)
p1_location = Variable('location', '876038248', '9596660697', rating_ref)
p1_room = Variable('room', '876038248', '9596660698', rating_ref)
p1_computer = Variable('computers', '876038248', '9596660700', rating_ref)
p1_photo = Variable('photographer', '876038248', '9596660701', rating_ref)
p1_video = Variable('video', '876038248', '9596660702', rating_ref)
p1_audio = Variable('audio', '876038248', '9596660703', rating_ref)
p1_gender = Variable('gender', '876040299', ref=gender_ref)

p2_affil = Variable('attendee affiliation', '878943755', ref=affil_ref)
p2_market = Variable('marketing penetration', '878943756', ref=market_ref)
p2_useful = Variable('found material useful', '878943757', '9618206443',
                     agree_ref)
p2_new = Variable('covered new material', '878943757', '9618206444', agree_ref)
p2_info = Variable('has enough info to build site', '878943757', '9618206445',
                   agree_ref)
p2_location = Variable('location', '878943758', '9618264854', rating_ref)
p2_room = Variable('room', '878943758', '9618264855', rating_ref)
p2_computer = Variable('computers', '878943758', '9618264856', rating_ref)
p2_video = Variable('video', '878943758', '9618264857', rating_ref)
p2_audio = Variable('audio', '878943758', '9618264858', rating_ref)
p2_usable = Variable('Weebly usability', '878943758', '9618264859', rating_ref)
p2_flexible = Variable('Weebly flexibility', '878943758', '9618264860',
                       rating_ref)
p2_gender = Variable('gender', '878943759', ref=gender_ref)
p2_site = Variable('built site', '878946400', ref=site_ref)

varlist = [p1_affil, p1_market, p1_useful, p1_new, p1_info, p1_build, p1_room,
           p1_location, p1_computer, p1_photo, p1_video, p1_audio, p1_gender,
           p2_affil, p2_market, p2_useful, p2_new, p2_info, p2_room, p2_audio,
           p2_location, p2_computer, p2_video, p2_gender, p2_site, p2_usable,
           p2_flexible]

question_ids = []
for var in varlist:
    if var.question not in question_ids:
        question_ids.append(var.question)

# 5: Get responses for the subset of questions in question_ids for all
# respondents of the survey (no need to batch since all can be obtained with
# one api call
respondent_ids = []
s_data = []

for survey_id in surveys:
    s_ids = get_respondent_ids(survey_id, local_file)
    for s_id in s_ids:
        respondent_ids.append(s_id)
    s_responses = get_survey_data(survey_id, local_file, respondent_ids)
    for response in s_responses['data']:
        s_data.append(response)

responses = {'data': s_data}
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
