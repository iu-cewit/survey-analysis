# Variables for student interest survey

from survey_access import *
from variables import *


def main():
    # Create the variables
    first_name = Variable('first name', '592547791')
    last_name = Variable('last name', '592547959')
    level_ref = {
      "6915931739": "Other",
      "6915931746": "Freshman",
      "6915931749": "Sophomore",
      "6915931752": "Junior",
      "6915931755": "Senior",
      "6915931757": "Senior",
      "6915931760": "Master",
      "6915931763": "JD",
      "6915931766": "PhD",
      "6915931769": "EdD",
      "6915931770": "OD"
    }
    level = Variable('level of study', '592548553', None, level_ref)
    mailing_ref = {"6926768925": "Yes", "6926768926": "No"}
    mailing = Variable('opt-in mailing list','592549927', ref=mailing_ref)
    majors = Variable('majors', '594645333')
    minors = Variable('minors', '594645445')
    email = Variable('email address', '594646446', answer_id='0')
    interest_ref = {
        "6926587175": 2,
        "6926587176": 1,
        "6926587177": 0,
        "6926587178": -1
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
    mentor_ref = {
      "6926590125": "peer",
      "6926590126": "staff",
      "6926590127": "faculty",
      "6926590128": "serve"
    }
    mentor = Variable('mentoring needs','594654487', None, mentor_ref)
    agree_ref = {
      "6926745140": 2,
      "6926745141": 1,
      "6926745142": -1,
      "6926745143": -2,
      "6926745144": 0
    }
    it_career = Variable('interested in tech career', '597351774',
                         '6926745145', agree_ref)

    varlist = [first_name, last_name, level, mailing, majors, minors,
               email, data_analysis, blogging, programming, graphics,
               humanities, social_justice, social_good, social_media,
               game_dev, gaming, interaction, mobile_app, web_dev,
               phys_computing, project_mgmt, research, security,
               education, higher_ed, mentor, it_career]

    # Create subset of questions corresponding to variables
    question_ids = []
    for var in varlist:
        if var.q not in question_ids:
            question_ids.append(var.q)
    #print(question_ids)

    # Access student interest survey via api
    local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
    survey_id = '46772574'
    respondent_ids = get_respondent_ids(survey_id, local_file)

    # Get responses for a subset of respondents (to limit calls/second)
    test_respondents = respondent_ids[:10]
    responses = get_survey_data(survey_id, local_file, test_respondents)
    res_data = {}
    for respondent in responses["data"]:
        temp = [q for q in respondent["questions"] if q.get("question_id")
                in question_ids]
        res_data[respondent.get("respondent_id")] = temp
    #return res_data

    #res1 = res_data["3038076826"]
    #res2 = res_data["3059085614"]

    for res in res_data:
        print('respondent_id:',res)
        for var in varlist:
            print(var.desc,':',str(var.get_value(res_data[res])))


if __name__ == '__main__':
    main()
