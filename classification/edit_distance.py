# Levenshtein distance


def edit_distance(source, target):
    """Returns the shortest distance to transform source into target.

    str, str -> int"""
    if source == target:
        return 0
    elif len(source) == 0:
        return len(target)
    elif len(target) == 0:
        return len(source)
    v0 = [None] * (len(target) + 1)
    v1 = [None] * (len(target) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(source)):
        v1[0] = i + 1
        for j in range(len(target)):
            if source[i] == target[j]:
                cost = 0
            else:
                cost = 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    return v1[len(target)]


def edit_distance_phrase(source, target):
    """Returns the shortest distance to transform source phrase into target.

    str, str -> int"""
    source = source.split()
    target = target.split()

    # remove common words
    for s_word in source.copy():
        if s_word in target.copy():
            source.remove(s_word)
            target.remove(s_word)

    # calc minimum distance for remaining words
    distance = []
    if source == []:
        return sum([len(word) for word in target])
    elif target == []:
        return sum([len(word) for word in source])
    else:
        for s_word in source:
            edit_dist = []
            for t_word in target:
                edit_dist.append(edit_distance(s_word, t_word))
            distance.append(sum(edit_dist))
        return min(distance)