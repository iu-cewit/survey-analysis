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
        """Returns a respondent's answer for a question-answer combination

        Variable, list of dicts (questions) -> list"""
        result = []
        for q in responses:
            if q.get("question_id") == self.q:
                if self.ref is None:
                    result = [a.get("text") for a in q.get("answers")]
                elif self.a is None:
                    row = [a.get("row") for a in q.get("answers")]
                    result = [self.ref[k] for k in row]
                else:
                    grid = [a.get("col") for a in q.get("answers") if
                            a.get("row") == self.a]
                    result = [self.ref[col] for col in grid]
        return result

    def make_value(self, responses, new_value=None):
        """Modifies a respondent's answer for a question-answer combination

        Variable, list of dicts (questions), value (str or num) -> none"""
        if new_value is None:
            new_value = []
        new_q = {"question_id": self.q}
        if self.a is None and self.ref is None:
            new_q["answers"] = [{"row": "0", "text": new_value}]
        elif self.a is not None and self.ref is None:
            new_q["answers"] = [{"row": self.a, "text": new_value}]
        elif self.a is None and self.ref is not None:
            new_q["answers"] = [{"row": new_value}]
        else:
            new_q["answers"] = [{"row": self.a, "col": new_value}]

        questions = [q.get("question_id") for q in responses]
        if self.q in questions:
            for q in responses:
                if q.get("question_id") == self.q:
                    responses.remove(q)
        responses.append(new_q)


