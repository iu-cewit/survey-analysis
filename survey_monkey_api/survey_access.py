#Get data from Survey Monkey for analysis

from survey_monkey_api import *
import csv

def authorize(filename):
    """Creates API service from key (line 1) and token (line 2) in file.

    str -> ApiService"""
    with open(filename, 'r') as file:
        auth = {'key': file.readline().strip(), 'token': file.readline().strip()}
        return ApiService(auth['key'], auth['token'])

def request_filename():
    """Requests user input for filename

    none -> str"""
    return input("Enter the filename to be created with format <name.csv>: ")

def save_survey_list(field_list): #works but redundant with save_survey_data
    """Creates csv file. Field list: title, date_created, date_modified,
    language_id, question_count, num_responses, analysis_url, preview_url

    list of str -> none"""
    filename = request_filename()
    with open(filename, 'w', encoding = 'utf-8') as csvfile:
        #csv file setup
        fieldnames = ['survey_id']
        for field in field_list:
            fieldnames.append(field)
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        #api request
        data = {'fields': field_list}
        survey_list = api.get_survey_list(data)
        for survey in survey_list['data']:
            writer.writerow(survey)
            print("Survey added to file: " + survey['survey_id'])

def save_survey_data(json_obj, sublist, req_field, opt_field_list=[]):
    #this should replace save_survey_list once tested
    """Creates csv file from json object. Object types: surveys, details,
    respondents, responses. 

    dict, str, str, list of str -> none"""
    filename = request_filename()
    with open(filename, 'w', encoding = 'utf-8') as csvfile:
        fieldnames = [req_field]
        for field in opt_field_list:
            fieldnames.append(field)
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        row_total = 0
        for row in json_obj[sublist]: #only works for one level of nested data
            writer.writerow(row)
            row_total += 1
    print("Total rows added to " + filename + ": " + str(row_total))

def get_structure(json_object, nest=0):
    """Displays the structure of a json_object.

    object -> none"""
    if not isinstance(json_object, list):
        if not isinstance(json_object, dict):
            print('    '*nest + str(json_object) + ' has type ' + \
                  str(type(json_object)))
        else:
            nest += 1
            for item in json_object.items():
                print('    '*nest + str(item[0]) + ' has type ' + \
                      str(type(item[1])))
                get_structure(item[1], nest)
    else:
        nest += 1
        for child in json_object:
            get_structure(child, nest)
    #this is giving me an extra layer for values rather than just keys

##def get_questions(survey_id, auth_file):
##    """Returns a dictionary of questions and answers.
##
##    str -> dict of str"""
    
