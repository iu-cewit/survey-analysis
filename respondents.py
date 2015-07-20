# A class for survey respondents from surveys administered by Survey Monkey

class Respondent:
    """a class for a unique survey respondent

        attributes: id (str), responses (dict)"""
    def __init__(self, id, responses):
        """id (str) is respondent_id from survey monkey, responses (dict) are
        from survey monkey api method get_responses"""
        self.id = id
        self.responses = responses

    def __str__(self):
        return self.id

    def __repr__(self):
        return 'Respondent(' + self.id + ',' + self.responses + ')'

