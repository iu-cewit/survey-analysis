# Creating variables for use in dataframe


class Variable:
    """a class for a unique survey question-answer combination

    attributes: description (str), q (str), a (str), ref (dict)"""
    def __init__(self, description, question_id, answer_id=None, ref=None):
        """name (str), question_id from survey monkey (str), answer_id  from
        survey monkey (str), ref has format {answer_choice: value} (dict)"""
        self.description = description
        self.question = question_id
        self.answer = answer_id
        self.ref = ref

    def __str__(self):
        return self.description

    def __repr__(self):
        return 'Variable(' + self.description + ', ' + self.question + ', ' + \
               self.answer + ', ' + str(self.ref) + ')'

    def get_value(self, responses):
        """Returns a respondent's answer for a question-answer combination

        Variable, list of dicts (questions) -> list"""
        result = []
        for question in responses:
            if question.get("question_id") == self.question:
                if self.ref is None:
                    result = [answer.get("text") for answer in 
                              question.get("answers")]
                elif self.answer is None:
                    row = [answer.get("row") for answer in 
                           question.get("answers")]
                    result = [self.ref[k] for k in row]
                else:
                    grid = [answer.get("col") for answer in 
                            question.get("answers") if
                            answer.get("row") == self.answer]
                    result = [self.ref[col] for col in grid]
        return result

    def make_value(self, responses, new_value=None):
        """Modifies a respondent's answer for a question-answer combination

        Variable, list of dicts (questions), value (str or num) -> none"""
        if new_value is None:
            new_value = []
        new_question = {"question_id": self.question}
        if self.answer is None and self.ref is None:
            new_question["answers"] = [{"row": "0", "text": new_value}]
        elif self.answer is not None and self.ref is None:
            new_question["answers"] = [{"row": self.answer, "text": new_value}]
        elif self.answer is None and self.ref is not None:
            new_question["answers"] = [{"row": new_value}]
        else:
            new_question["answers"] = [{"row": self.answer, "col": new_value}]

        questions = [question.get("question_id") for question in responses]
        if self.question in questions:
            for question in responses:
                if question.get("question_id") == self.question:
                    responses.remove(question)
        responses.append(new_question)


