# Functions to match strings
# Edit_distance() adapted from https://en.wikibooks.org/wiki/
# Algorithm_Implementation/Strings/Levenshtein_distance#Python


import re


def main():
    print(edit_distance('SEA', 'ATE'))
    print(edit_distance('plasma', 'altruism'))
    print(edit_distance('spartan', 'part'))


def edit_distance(s, t):
    """Returns the shortest distance to transform s (source) into t (target).

    str, str -> int"""
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            if s[i] == t[j]:
                cost = 0
            else:
                cost = 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    return v1[len(t)]


def find_match(respondent, variable, match_list):
    """Returns the closest word or phrase from a list of possible matches

    list of dicts (questions), Variable, list of str -> str"""
    res_value = variable.get_value(respondent)[0]
    print('Value entered:', str(res_value))
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
            res_fields = min(field_matches, key=field_matches.get)
            match_type = 'Close'
        except ValueError:
            res_fields = 'No Match Found'
    else:
        res_fields = res_fields[0]
    print(match_type + ' match: ', res_fields)
    return (res_fields, match_type)


if __name__ == '__main__':
    main()
