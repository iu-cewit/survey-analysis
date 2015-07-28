# Variables for student interest survey

from survey_access import *
from variables import *
from matching import *
import csv
import time


def main():
    # 1: Generate variables from survey monkey questions
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
    level = Variable('level of study', '592548553', ref=level_ref)
    mailing_ref = {"6926768925": "Yes", "6926768926": "No"}
    mailing = Variable('opt-in mailing list', '592549927', ref=mailing_ref)
    major1 = Variable('major1', '594645333', "6925814179")
    major2 = Variable('major2', '594645333', "6925814180")
    major3 = Variable('major3', '594645333', "6925814181")
    minor1 = Variable('minor1', '594645445', "6895985038")
    minor2 = Variable('minor2', '594645445', "6895985039")
    minor3 = Variable('minor3', '594645445', "6895985041")
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
    mentor_ref = {
        "6926590125": "peer",
        "6926590126": "staff",
        "6926590127": "faculty",
        "6926590128": "serve"
    }
    mentor = Variable('mentoring needs', '594654487', None, mentor_ref)
    agree_ref = {
        "6926745140": "Strongly Agree",
        "6926745141": "Agree",
        "6926745142": "Disagree",
        "6926745143": "Strongly Disagree",
        "6926745144": "Unsure/Don't Know"
    }
    it_career = Variable('interested in tech career', '597351774',
                         '6926745145', agree_ref)

    # 2: Create and populate new variables
    field = Variable('primary major or discipline', 'field_name')
    category = Variable('major or discipline category', 'field_category')
    school = Variable('degree granting unit', 'major_school')

    # Generate values for new variables

    # dictionary of all majors and categories
    source_file = '/Users/nbrodnax/Indiana/CEWIT/source_data/fields.csv'
    with open(source_file) as csvfile:
        contents = csv.DictReader(csvfile, fieldnames=['Major', 'Category'])
        fields = {}
        for row in contents:
            fields[row['Major'].lower()] = row['Category']

    # dictionary of all IU majors, schools, and credentials
    source_file = '/Users/nbrodnax/Indiana/CEWIT/source_data/iu_majors.csv'
    with open(source_file) as csvfile:
        contents = csv.DictReader(csvfile, fieldnames=['Major', 'School',
                                                       'STEM', 'Degrees'])
        schools = {}
        for row in contents:
            schools[row['Major'].lower()] = row['School']

    # dictionary of all IU majors, schools, and categories
    source_file = '/Users/nbrodnax/Indiana/CEWIT/source_data/iu_major_cat.csv'
    with open(source_file) as csvfile:
        contents = csv.DictReader(csvfile, fieldnames=['Major', 'School',
                                                       'Category'])
        categories = {}
        for row in contents:
            categories[row['Major'].lower()] = row['Category']

    # lists to use in the matching process
    field_list = [field.lower() for field in fields]
    iu_major_list = [m.lower() for m in schools]

    # match respondent input to major, category, and school

    # The variables I want to get data for
    varlist = [first_name, last_name, email, mailing, level, field, school,
               category, it_career, major1, minor1, data_analysis,
               blogging, programming, graphics, humanities, social_justice,
               social_good, social_media, game_dev, gaming, interaction,
               mobile_app, web_dev, phys_computing, project_mgmt, research,
               security, education, higher_ed, mentor]

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
    # print('Respondent IDs:', res_ids, '\n')

    field_matches = {'Exact': 0, 'Close': 0, 'None': 0}
    iu_major_matches = {'Exact': 0, 'Close': 0, 'None': 0}

    # Populate values for new variables (unreadable - needs refactoring)
    for r in res_ids:
        # find closest matching field and use to populate field and category
        # variables
        res_field = find_match(res_data[r], major1, field_list)
        field_matches[res_field[1]] += 1
        field.make_value(res_data[r], res_field[0])

        # find closest matching major and use to populate school variable
        res_iu_major = find_match(res_data[r], major1, iu_major_list)
        iu_major_matches[res_iu_major[1]] += 1
        school.make_value(res_data[r], schools.get(res_iu_major[0]))
        category.make_value(res_data[r], categories.get(res_iu_major[0]))

    # Create matrix of all variable values
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

    print('Field Matches:')
    for item in field_matches.items():
        print(item)
    print('IU Major Matches:')
    for item in iu_major_matches.items():
        print(item)
    print('Rows added: ', str(row))
    # return matrix

    # Save data to file
    with open("data.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(matrix)


def print_respondent(respondent, variable_list):
    """Displays all response data and corresponding variable values

    list of dicts (questions), list of Variables -> none"""
    print('respondent_id:', respondent)
    for var in variable_list:
        print(var.desc, ':', str(var.get_value(respondent)))


if __name__ == '__main__':
    main()
