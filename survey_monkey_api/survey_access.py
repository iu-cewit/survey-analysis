# Working with json objects generated by Survey Monkey API

from survey_monkey_api import *


def main():
    # get questions from survey monkey api
    local_file = '/Users/nbrodnax/Indiana/CEWIT/survey_monkey_auth.txt'
    survey_id = '48173850'
    questions = get_questions(survey_id, local_file)
    print(questions)

    # modify question dictionary (for later use in dataframe)
    recode_question(questions, '608743994', 'can_attend')
    recode_answer(questions, '608743994', '7054599535', 1)
    recode_answer(questions, '608743994', '7054599536', 0)
    print('\n', questions)


def get_structure(json_object, nest=0):
    """Displays the names and types of nested objects.

    json object -> none"""
    if not isinstance(json_object, list):
        if not isinstance(json_object, dict):
            print('    '*nest + str(json_object) + ' has type ' +
                  str(type(json_object)))
        else:
            nest += 1
            for item in json_object.items():
                print('    '*nest + str(item[0]) + ' has type ' +
                      str(type(item[1])))
                get_structure(item[1], nest)
    else:
        nest += 1
        for child in json_object:
            get_structure(child, nest)
    # this is giving me an extra layer for values rather than just keys


def get_questions(survey_id, auth_filename):
    """Returns a dictionary of question ids and answer ids.

    str, str -> dict of str"""
    auth = credentials(auth_filename)
    api = ApiService(auth['key'], auth['token'])

    # get survey details
    data = {"survey_id": survey_id}
    details = api.get_survey_details(data)

    # get list of questions and answers
    pages = details["data"]["pages"]
    contents = [x.get("questions") for x in pages if isinstance(x, dict)]
    questions = {}
    for page in contents:
        for question in page:
            question_id = question.get("question_id")
            question_text = question.get("heading")
            answers = question.get("answers")
            if len(answers) == 0:
                answer_id = {'0': None}
            else:
                answer_id = {a.get("answer_id"): a.get("text")
                             for a in answers}
            questions[question_id] = {'text': question_text,
                                      'answer': answer_id}
    return questions


def get_respondent_ids(survey_id, auth_filename):
    """Returns a list of respondent ids

    str, str -> list"""
    auth = credentials(auth_filename)
    api = ApiService(auth['key'], auth['token'])
    data = {"survey_id": survey_id}
    respondents = api.get_respondent_list(data)
    return [r.get("respondent_id") for r in respondents["data"]]


# The question_dict returned by get_questions() has the format:
# {question_id: {'text': question_text, 'answer': {answer_id: answer_value}}}

def recode_question(question_dict, question_id, new_text):
    """Modifies the question text in a question dictionary

    dict, str, str -> none"""
    question_dict[question_id]["text"] = new_text


def recode_answer(question_dict, question_id, answer_id, new_value):
    """Modifies the answer value in a question dictionary

    dict, str, str, obj -> none"""
    question_dict[question_id]['answer'][answer_id] = new_value


if __name__ == '__main__':
    main()
