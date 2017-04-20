import json
from os import path

import requests
import pandas
from bs4 import BeautifulSoup

from .survey_css import (CLS_QUESTION_LIST, CLS_QUESTION, CLS_QUESTION_TITLE,
                         CLS_QUESTION_TYPES)


def get_questions(survey_url):
    survey_html = get_survey_html(survey_url)
    soup = BeautifulSoup(survey_html, 'html5lib')
    question_list = soup.find('div', attrs={'class': CLS_QUESTION_LIST})
    questions = pandas.DataFrame({
        'div': question_list.find_all('div', attrs={'class': CLS_QUESTION})
    })
    questions['title'] = questions['div'].apply(
        lambda div: div.find('div', attrs={'class': CLS_QUESTION_TITLE}).text
    )

    questions['choices'] = questions['div'].apply(extract_choices)
    questions['choices_json'] = questions.choices.apply(lambda x: json.dumps(x))
    questions['id'] = ['q{}'.format(i) for i in range(len(questions))]
    return questions[['id', 'title', 'choices_json']]


def get_survey_html(survey_url, output=None):
    """Get the survey html from a url or a file.

    Args:
        survey_url: url or path to a text file containing the url.
        output: survey html will be saved to this location if provided.
    Returns:
        html contents of the survey
    """
    if path.exists(survey_url):
        survey_url = open(survey_url).read().strip()

    response = requests.get(survey_url)

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
