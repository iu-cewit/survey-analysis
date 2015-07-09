# Variables for student interest survey

from survey_access import *
from variables import *
import csv
import re


def main():
    # Generate variables from survey monkey questions
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
    mentor = Variable('mentoring needs', '594654487', None, mentor_ref)
    agree_ref = {
        "6926745140": 2,
        "6926745141": 1,
        "6926745142": -1,
        "6926745143": -2,
        "6926745144": 0
    }
    it_career = Variable('interested in tech career', '597351774',
                         '6926745145', agree_ref)

    # Create new variables
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

    # match respondent input to major, category, and school
    field_list = [f.lower() for f in fields]
    iu_major_list = [m.lower() for m in schools]

    # Working with all variables
    varlist = [first_name, last_name, level, mailing, field, major1, major2,
               major3, minor1, minor2, minor3, email, data_analysis, category,
               blogging, programming, graphics, humanities, social_justice,
               social_good, social_media, game_dev, gaming, interaction,
               mobile_app, web_dev, phys_computing, project_mgmt, research,
               security, education, higher_ed, mentor, it_career, school]

    # Create subset of questions corresponding to variables
    question_ids = []
    for var in varlist:
        if var.q not in question_ids:
            question_ids.append(var.q)
    # print(question_ids)

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
    # return res_data

    # For working offline only
    # with open('responses.txt', 'r') as file:
    #     contents = file.readlines()
    #     res_data = eval(contents[0])
    # return res_data

    res_ids = [r for r in res_data.keys()]
    print('Respondent IDs:', res_ids, '\n')
    for r in res_ids:
        print(first_name.get_value(res_data[r])[0],
              last_name.get_value(res_data[r])[0])
        res_field = find_match(res_data[r], major1, field_list)
        field.make_value(res_data[r], res_field)
        res_iu_major = find_match(res_data[r], major1, iu_major_list)
        category.make_value(res_data[r], fields.get(res_field))
        school.make_value(res_data[r], schools.get(res_iu_major))
        print(res_data[r])
    # res1 = data['3022130005']
    # print_respondent(res1, [last_name, level, minors, security])
    # need major variable, field list, respondent_ids


def print_respondent(respondent, variable_list):
    """Displays all response data and corresponding variable values

    list of dicts (questions), list of Variables -> none"""
    print('respondent_id:', respondent)
    for var in variable_list:
        print(var.desc, ':', str(var.get_value(respondent)))


def find_match(respondent, variable, match_list):
    """Returns the closest match from a list of possible matches

    list of dicts (questions), Variable, list of str -> str"""
    res_value = variable.get_value(respondent)[0]
    print('Value entered:', str(res_value))
    match_type = 'No'
    if res_value.lower() in match_list:
        res_fields = [res_value.lower()]
        match_type = 'Exact'
    else:
        res_fields = [m.group(0) for f in match_list for m in
                      [re.search(r'.*(%s).*' % res_value.lower(), f)] if m]
    if len(res_fields) != 1:
        field_matches = {}
        for f in match_list:
            i = 0
            for w in [w.lower() for w in res_value.split() if w != 'and']:
                if w in f:
                    i += 1
                    field_matches[f] = i
        try:
            res_fields = max(field_matches, key=field_matches.get)
            match_type = 'Close'
        except ValueError:
            res_fields = 'No Match Found'
    else:
        res_fields = res_fields[0]
    print(match_type + ' match: ', res_fields)
    return res_fields


if __name__ == '__main__':
    main()
