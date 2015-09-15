# Translate student interest survey results into newsletter preferences

from survey_access import *
from variables import *
import csv
import time


def main():
    # 1: Defines the variables based survey monkey questions
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

    # 2: Creates a list of the variables you want to get data for and gets all
    # the info you need to request the data via the survey monkey api
    varlist = [first_name, last_name, email, it_career, data_analysis,
               blogging, programming, graphics, humanities, social_justice,
               social_good, social_media, game_dev, gaming, interaction,
               mobile_app, web_dev, phys_computing, project_mgmt, research,
               security, education, higher_ed, workshops]

    # A list of only those survey questions corresponding to variables
    question_ids = []
    for var in varlist:
        if var.question not in question_ids:
            question_ids.append(var.question)

    # Parameters for accessing data via survey monkey api
    # local_file contains your api key (line 1) and access token (line 2)
    local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
    survey_id = '46772574'
    respondent_ids = get_respondent_ids(survey_id, local_file)
    # respondent_ids = respondent_ids[:10]  # subset for testing only

    # 3: Gets response data for the subset of questions in question_ids with
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

    # A list of unique respondent ids - you will use this to create a
    # dictionary of newsletter preferences for each survey respondent
    res_ids = [respondent for respondent in res_data.keys()]

    # 4: Defines the mapping of topics and workshops to categories

    # Dictionary identifying the category for each topic. The keys are either
    # variable names (no quotes) or workshop topics (with quotes)
    categories = {
        data_analysis: 'No category',
        blogging: 'No category',
        programming: 'Programming/coding',
        graphics: 'Digital Humanities',
        humanities: 'Digital Humanities',
        social_justice: 'Volunteer or Service Opportunities',
        social_good: 'Volunteer or Service Opportunities',
        social_media: 'Social Media',
        game_dev: 'Game Development',
        gaming: 'Game Development',
        interaction: 'Web Design/Development',
        mobile_app: 'App Design/Development',
        web_dev: 'Web Design/Development',
        phys_computing: 'No category',
        project_mgmt: 'Leadership',
        research: 'Research Technologies',
        security: 'No category',
        education: 'Teaching Technologies',
        higher_ed: 'Teaching Technologies',
        it_career: 'Tech Career Info/Opportunities',
        'other': 'No category',
        'presentation': 'No category',
        'web design': 'Web Design/Development',
        'e-portfolio': 'Web Design/Development',
        'video editing': 'No category',
        'mobile app dev': 'App Design/Development',
        'social media': 'Social Media',
        'adobe': 'Web Design/Development',
        'programming': 'Programming/coding',
        'none': 'No category'
    }

    # Dictionary identifying the level of interest (1=yes, 0=no) for each
    # category.  You will create one of these for each respondent and modify
    # the level of interest depending on how she answered the survey
    cat_count = {
        'App Design/Development': 0,
        'Digital Humanities': 0,
        'Game Development': 0,
        'Leadership': 0,
        'Programming/coding': 0,
        'Research Technologies': 0,
        'Social Media': 0,
        'Teaching Technologies': 0,
        'Tech Career Info/Opportunities': 0,
        'Volunteer or Service Opportunities': 0,
        'Web Design/Development': 0,
        'No category': 0
    }

    # 5: Generate newsletter preferences based on three kinds of variables:
    # info (3), interests (20), and workshops (1)
    info = [first_name, last_name, email]

    interests = [data_analysis, blogging, programming, graphics, humanities,
                 social_justice, social_good, social_media, game_dev, gaming,
                 interaction, mobile_app, web_dev, phys_computing,
                 project_mgmt, research, security, education, higher_ed,
                 it_career]

    newsletter_preferences = {}
    for respondent in res_ids:
        row_data = {'id': respondent}
        # for info variables, get the values
        for variable in info:
            value = variable.get_value(res_data[respondent])
            if len(value) == 1:
                row_data[variable.description] = value[0]
            else:
                row_data[variable.description] = value
        # for interest variables from question 8, get values and categorize
        res_categories = cat_count.copy()
        for variable in interests:
            value = variable.get_value(res_data[respondent])
            if len(value) > 0:
                if value[0] in ['Agree', 'Strongly Agree', 'Interested',
                                'Very Interested']:
                    res_categories[categories[variable]] = 1
        # for workshop variable from question 9, get list of values and
        # categorize
        res_workshops = workshops.get_value(res_data[respondent])
        if len(res_workshops) == 1:
            res_categories[categories[res_workshops[0]]] = 1
        elif len(res_workshops) > 1:
            for item in res_workshops:
                res_categories[categories[item]] = 1
        for category in res_categories:
            row_data[category] = res_categories[category]
        email_addr = row_data['email address']
        if isinstance(email_addr, str):
            newsletter_preferences[email_addr] = row_data

    # 6: Makes a copy of the newsletter recipients file with interests added
    # open the newsletter recipients file
    fieldnames_in = ['last', 'first', 'email']
    fieldnames_out = fieldnames_in.copy()
    for category in cat_count:
        fieldnames_out.append(category)
    with open('newsletter_recipients.csv', 'r', encoding='utf-8',
              errors='ignore') as infile, \
            open('newsletter_preferences.csv', 'w') as outfile:
        reader = csv.DictReader(infile, fieldnames_in)
        next(reader, None)  # skip the header row
        writer = csv.DictWriter(outfile, fieldnames_out)
        writer.writeheader()
        for recipient in reader:
            temp = recipient.copy()
            if recipient['email'] in newsletter_preferences:
                prefs = newsletter_preferences[recipient['email']]
                for pref in cat_count:
                    temp[pref] = prefs[pref]
            else:
                for pref in cat_count:
                    temp[pref] = cat_count[pref]
            writer.writerow(temp)


if __name__ == '__main__':
    main()
