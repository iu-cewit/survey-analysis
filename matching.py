# Functions to match strings
# Edit_distance() adapted from https://en.wikibooks.org/wiki/
# Algorithm_Implementation/Strings/Levenshtein_distance#Python


import re


def main():
    pass


def find_match(respondent, variable, match_list):
    """Returns the closest word or phrase from a list of possible matches

    list of dicts (questions), Variable, list of str -> tuple of str"""
    res_value = variable.get_value(respondent)[0]
    # print('Value entered:', str(res_value))
    match_type = 'None'
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
    # print(match_type + ' match: ', res_fields)
    return res_fields, match_type


if __name__ == '__main__':
    main()
