# Creating variables for use in dataframe


class Variable:
    """a class for a unique survey question-answer combination

    attributes: description (str), q (str), a (str), ref (dict)"""
    def __init__(self, description, question_id, answer_id=None, ref=None):
        """name (str), question_id from survey monkey (str), answer_id  from
        survey monkey (str), ref has format {answer_choice: value} (dict)"""
        self.desc = description
        self.q = question_id
        self.a = answer_id
        self.ref = ref

    def __str__(self):
        return self.desc

    def __repr__(self):
        return 'Variable(' + self.desc + ', ' + self.q + ', ' + \
               self.a + ', ' + str(self.ref) + ')'

    def get_value(self, responses):
        """Returns the value for a question-answer combination

        Variable, list of dicts (questions) -> list"""
        result = []
        for q in responses:
            if q.get("question_id") == self.q:
                if self.ref is None:
                    result = [a.get("text") for a in q.get("answers")]
                else:
                    grid = [a.get("col") for a in q.get("answers") if
                            a.get("row") == self.a]
                    result = [self.ref[col] for col in grid]
        return result
        # need to fix cases where respondent didn't answer
