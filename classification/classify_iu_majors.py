# Classify IU majors into 8 College Board categories

import csv
import re


def main():
    # Load the field list and the iu majors file
    source_file = '/Users/nbrodnax/Indiana/CEWIT/source_data/fields.csv'
    with open(source_file) as csvfile:
        contents = csv.DictReader(csvfile, fieldnames=['Major', 'Category'])
        fields = {}
        for row in contents:
            fields[row['Major'].lower()] = row['Category']
    
    field_list = [field.lower() for field in fields]
    field_matches = {'Exact': 0, 'Close': 0, 'None': 0}
    
    source_file = '/Users/nbrodnax/Indiana/CEWIT/source_data/iu_majors.csv'
    with open(source_file) as csvfile:
        contents = csv.DictReader(csvfile, fieldnames=['Major', 'School',
                                                       'STEM', 'Degrees'])
        schools = {}
        for row in contents:
            schools[row['Major'].lower()] = row['School']
    
    # For each major in the list, find the category
    with open('iu_major_cat.csv', 'w', encoding='utf-8') as csvfile:
        fieldnames = ['Major', 'School', 'Category']
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for item in schools.items():
            temp_dict = {'Major': item[0], 'School': item[1]}
            category = find_match(item[0], field_list)
            field_matches[category[1]] += 1
            try:
                temp_dict['Category'] = fields[category[0]]
            except KeyError:
                temp_dict['Category'] = category[0]
            writer.writerow(temp_dict)

    print('Field Matches:')
    for item in field_matches.items():
        print(item)


def find_match(value, match_list):
    """Returns the closest word or phrase from a list of possible matches

    str, list of str -> tuple of str"""
    # print('Value entered:', str(value))
    match_type = 'None'
    if value.lower() in match_list:
        fields = [value.lower()]
        match_type = 'Exact'
    else:
        fields = [m.group(0) for f in match_list for m in
                  [re.search(r'.*(%s).*' % value.lower(), f)] if m]
    if len(fields) != 1:
        field_matches = {}
        for f in match_list:
            i = 0
            for w in [w.lower() for w in value.split() if w != 'and']:
                if w in f:
                    i += 1
                    field_matches[f] = i
        try:
            fields = max(field_matches, key=field_matches.get)
            match_type = 'Close'
        except ValueError:
            fields = 'No Match Found'
    else:
        fields = fields[0]
    # print(match_type + ' match: ', fields)
    return fields, match_type


if __name__ == '__main__':
    main()
