import json
from os import path

import requests
import pandas
from bs4 import BeautifulSoup

from .survey_css import (CLS_QUESTION, CLS_QUESTION_TITLE, CLS_QUESTION_TYPES)


def get_questions(survey_url, requests_session=None):
    survey_html = get_survey_html(survey_url, requests_session=requests_session)
    soup = BeautifulSoup(survey_html, 'html5lib')

    # Extract the divs for each question
    questions = pandas.DataFrame({
        'div': soup.find_all('div', attrs={'class': CLS_QUESTION})
    })

    # Assign question numbers. ASSUMES question divs are in order.
    questions['question_id'] = ['q{}'.format(i) for i in range(len(questions))]

    # Extract question text from each question
    questions['question'] = questions['div'].apply(
        lambda div: div.find('div', attrs={'class': CLS_QUESTION_TITLE}).text
    )

    # Required questions are denoted with an asterisk in the html,
    # but not in the survey responses. Remove the asterisk so that
    # the response data can be merged with the question data.
    questions['question'] = questions.question.str.replace(' \*$', '')

    # Extract choices from each question div, and convert to json for safety.
    questions['choices'] = questions['div'].apply(extract_choices)
    questions['choices_json'] = questions.choices.apply(lambda x: json.dumps(x))

    return questions[['question_id', 'question', 'choices_json']]


def get_survey_html(survey_url, requests_session=None, output=None):
    """Get the survey html from a url or a file.

    Args:
        survey_url: url or path to a text file containing the url.
        requests_session: Optional. requests.Session() to use to get the survey.
        output: survey html will be saved to this location if provided.
    Returns:
        html contents of the survey
    """
    if path.exists(survey_url):
        survey_url = open(survey_url).read().strip()

    if requests_session is None:
        requests_session = requests.Session()

    response = requests_session.get(survey_url)

    if output:
        with open(output, 'wb') as handle:
            handle.write(response.content)

    return response.content


def extract_choices(div):
    choices = []
    for CLS in CLS_QUESTION_TYPES:
        choice_divs = div.find_all(attrs={'class': CLS})
        if len(choice_divs) > 0:
            choices.extend([div.text for div in choice_divs])
    return choices
