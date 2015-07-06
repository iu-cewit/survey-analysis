# Creating variables for use in dataframe


def main():
    with open('background.txt', 'r') as file:
        contents = file.readlines()
    data = eval(contents[0])
    return data
    # res1 = data["3038076826"]
    # res2 = data["3059085614"]
    # lname = Variable('last name', '592547959', None)
    # major = Variable('majors', '594645333', None)
    # minor = Variable('minors', '594645445', None)
    # map1 = {"6926587175":1,"6926587176":1,"6926587177":0,"6926587178":0}
    # big_data = Variable('big data', '594651002', '6926587182', map1)


class Variable:
    """a class for a unique survey question-answer combination

    attributes: q_id (str), q_text (str), a_id (str), a_text (str)"""
    def __init__(self, description, question_id, answer_id=None, ref=None):
        """name (str), question_id (str), answer_id (str), ref (dict)"""
        self.des = description
        self.id = question_id
        self.ans = answer_id
        self.ref = ref

    def __str__(self):
        return self.des

    def __repr__(self):
        return 'Variable(' + self.des + ', ' + self.id + ', ' + \
               str(self.ref) + ')'

    def get_value(self, responses):
        """Returns the value for a question-answer combination

        Variable, list of dicts (questions) -> list"""
        for q in responses:
            if q.get("question_id") == self.id:
                if self.ref is None:
                    return [a.get("text") for a in q.get("answers")]
                else:
                    grid = [a.get("col") for a in q.get("answers") if
                            a.get("row") == self.ans]
                    return [self.ref[col] for col in grid]
        # need to fix cases where respondent didn't answer


if __name__ == '__main__':
    main()
