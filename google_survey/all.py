import yaml

from .responses import get_responses
from .tidy import tidy_responses
from .questions import get_questions


def get(survey_info_yaml):
    survey_info = yaml.load(open(survey_info_yaml))

    # Get the responses
    sheet_name = survey_info['sheet_name']
    creds_file = survey_info['creds_file']
    wide_responses = get_responses(sheet_name, creds_file)
    long_responses = tidy_responses(wide_responses)

    # Get the questions
    survey_url = survey_info['survey_url']
    questions = get_questions(survey_url)

    return long_responses.merge(questions)
