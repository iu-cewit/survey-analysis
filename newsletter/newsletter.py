# Import student interest survey results into salesforce marketing cloud

from survey_access import *
from variables import *
import csv
import time


def main():
    # 1: Generate variables from survey monkey questions
    first_name = Variable('first name', '592547791')
    last_name = Variable('last name', '592547959')
    email = Variable('email address', '594646446')
    interest_ref = {
        "6926587175": "Very Interested",
        "6926587176": "Interested",
        "6926587177": "Uninterested",
        "6926587178": "Completely Uninterested"
    }
    data_analysis = Variable('interested in data analysis',
                             '594651002', '6926587182', interest_ref)
    blogging = Variable('interested in blogging',
                        '594651002', '6926587184', interest_ref)
    programming = Variable('interested in computer programming',
                           '594651002', '6926587185', interest_ref)
    graphics = Variable('interested in digital art/graphic design',
                        '594651002', '6926587186', interest_ref)
    humanities = Variable('interested in digital humanities',
                          '594651002', '6926587187', interest_ref)
    social_justice = Variable('interested in tech equity/justice',
                              '594651002', '6926587188', interest_ref)
    game_dev = Variable('interested in game development',
                        '594651002', '6926587189', interest_ref)
    interaction = Variable('interested in human-computer interaction',
                           '594651002', '6926587190', interest_ref)
    mobile_app = Variable('interested in mobile app development',
                          '594651002', '6926587191', interest_ref)
    phys_computing = Variable('interested in physical computing',
                              '594651002', '6926587192', interest_ref)
    gaming = Variable('interested in playing games',
                      '594651002', '6926587193', interest_ref)
    project_mgmt = Variable('interested in project management',
                            '594651002', '6926587194', interest_ref)
    research = Variable('interested in research skills',
                        '594651002', '6926587195', interest_ref)
    social_media = Variable('interested in social media/networking',
                            '594651002', '6926587198', interest_ref)
    security = Variable('interested in technology security',
                        '594651002', '6926587200', interest_ref)
    education = Variable('interested in applications for K-12 education',
                         '594651002', '6926587203', interest_ref)
    higher_ed = Variable('interested in applications for higher ed',
                         '594651002', '6926587205', interest_ref)
    social_good = Variable('interested in applications for social good',
                           '594651002', '6926587207', interest_ref)
    web_dev = Variable('interested in web design',
                       '594651002', '6926587209', interest_ref)
    agree_ref = {
        "6926745140": "Strongly Agree",
        "6926745141": "Agree",
        "6926745142": "Disagree",
        "6926745143": "Strongly Disagree",
        "6926745144": "Unsure/Don't Know"
    }
    it_career = Variable('interested in tech career', '597351774',
                         '6926745145', agree_ref)
    workshop_ref = {
        "6926303108": "other",
        "6926303111": "presentation",
        "6926303112": "web design",
        "6926303113": "e-portfolio",
        "6926303114": "video editing",
        "6926303115": "mobile app dev",
        "6926303116": "social media",
        "6926303117": "adobe",
        "6926303118": "programming",
        "6926303119": "none"
    }
    workshops = Variable('interested in workshops', '597361598', None,
                         workshop_ref)

    # The variables I want to get data for
    varlist = [first_name, last_name, email, it_career, data_analysis,
               blogging, programming, graphics, humanities, social_justice,
               social_good, social_media, game_dev, gaming, interaction,
               mobile_app, web_dev, phys_computing, project_mgmt, research,
               security, education, higher_ed, workshops]

    # Create subset of questions corresponding to variables
    question_ids = []
    for var in varlist:
        if var.question not in question_ids:
            question_ids.append(var.question)
    # print(question_ids)

    # Parameters for accessing data via survey monkey api
    local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
    survey_id = '46772574'
    respondent_ids = get_respondent_ids(survey_id, local_file)

    # Get responses for the subset of questions in question_ids with
    # respondent ids split into batches of 500 to limit api calls/sec
    batch_num = (len(respondent_ids) // 500)
    i = 0
    row_begin = 0
    row_end = 500
    res_data = {}
    while i <= batch_num:
        if i < batch_num:
            respondents = respondent_ids[row_begin:row_end]
            print('processing rows ' + str(row_begin) + '-' + str(row_end-1))
        else:
            respondents = respondent_ids[row_begin:]
            print('processing rows ' + str(row_begin) + '-' +
                  str(len(respondent_ids)))
        responses = get_survey_data(survey_id, local_file, respondents)
        for respondent in responses["data"]:
            temp = [question for question in respondent["questions"] if
                    question.get("question_id") in question_ids]
            res_data[respondent.get("respondent_id")] = temp
        row_begin += 500
        row_end += 500
        i += 1
        time.sleep(5)

    res_ids = [respondent for respondent in res_data.keys()]

    # Dictionary of categories

    # Create matrix of all variable values - need to refactor
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

    # Save data to file
    with open("newsletter.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(matrix)

if __name__ == '__main__':
    main()
