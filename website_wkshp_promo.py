# Data cleaning for the marketing efforts used in the website workshops

import csv

# load data
local_file = '/Users/nbrodnax/Indiana/CEWIT/evaluation/surveys/' + \
             'phd_website_workshop_15/data/website_workshop_data.csv'

# get data for two marketing variables
matrix = []
with open(local_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    for row in reader:
        respondent = row[0]
        p1_promotion = row[2]
        p2_promotion = row[15]

        if '[' in p1_promotion:
            promotion_type = eval(p1_promotion)
            for item in promotion_type:
                matrix.append([respondent, item, '[]'])
        else:
            matrix.append([respondent, p1_promotion, '[]'])

        if '[' in p2_promotion:
            promotion_type = eval(p2_promotion)
            for item in promotion_type:
                matrix.append([respondent, '[]', item])
        else:
            matrix.append([respondent, '[]', p2_promotion])


# write matrix to csv file
header = ['respondent', 'p1_promotion', 'p2_promotion']
with open("marketing_data.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows([header])
    writer.writerows(matrix)
