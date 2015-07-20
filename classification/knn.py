# kNN algorithm


import re
import csv
import random
import operator
from edit_distance import *


def main():
    data = split_data('category.csv')
    training_set = data[0]
    testing_set = data[1]
    correct_predictions = 0
    t1 = testing_set[0]
    t2 = testing_set[1]

    for t in testing_set:
        # print('\n', t)
        neighbors = get_neighbors_ed(t[0], training_set, 3)
        # print('Neighbors:', neighbors)
        category = get_prediction(neighbors)
        # print('Prediction:', category)
        # print('Actual:', t[1])
        if category == t[1]:
            correct_predictions += 1
        # print(str(correct_predictions))

    print('Accuracy:', str(correct_predictions / len(testing_set) * 100),'%')


def split_data(filename, split_ratio=0.66):
    """Returns training and test datasets from a csv file

        str, float -> list"""
    try:
        with open(filename, 'r') as csvfile:
            contents = csv.reader(csvfile)
            dataset = list(contents)
            train = []
            test = []
            for row in range(len(dataset)):
                if random.random() < split_ratio:
                    train.append(dataset[row])
                else:
                    test.append(dataset[row])
        return [train, test]
    except IOError:
        print("There was a problem opening the file.")


def get_neighbors_ed(test_instance, training_set, k):
    """Returns the k neighbors with the smallest edit distance

        list, list, int -> list"""
    distances = []
    for row in range(len(training_set)):
        ed = edit_distance_phrase(test_instance, training_set[row][0])
        distances.append((training_set[row], ed))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for instance in range(k):
        neighbors.append(distances[instance][0])
    return neighbors


def get_neighbors(test_instance, training_set):
    """Returns the k neighbors with the largest number of word matches

        list, list, int -> list"""
    matches = [match.group(0)
               for train_instance in training_set
               for match in [re.search(r'.*(%s).*' % test_instance[0],
                                       train_instance[0], re.IGNORECASE)]
               if match]
    return matches # will later incorporate k by ranking them


def get_prediction(neighbors):
    """Returns a predicted attribute based on nearest neighbors

        list -> str or num"""
    class_votes = {}
    for class_type in range(len(neighbors)):
        vote = neighbors[class_type][-1]
        if vote in class_votes:
            class_votes[vote] += 1
        else:
            class_votes[vote] = 1
    return max(class_votes, key=class_votes.get)


if __name__ == '__main__':
    main()
