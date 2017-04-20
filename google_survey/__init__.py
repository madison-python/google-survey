from .responses import get_responses, tidy_responses
from .questions import get_questions, get_survey_html


def get_survey(responses_sheet_name, creds, survey_url, deidentify=False):
    # Start with the Google responses downloaded with gspread
    wide_responses = get_responses(responses_sheet_name, creds)

    # Deidentify responses if desired
    if deidentify:
        wide_responses = deidentify_survey_responses(wide_responses)

    # 
    questions = get_questions(survey_url)
    new_column_names = questions.set_index('title')['id'].to_dict()
    tidied_responses = google_survey.tidy_responses(responses, new_column_names)
    responses = responses.groupby('question').apply(label_response_type,
                                                    questions=questions)
    return responses


def label_response_type(responses, questions, other_response_type='Other'):
    # Identify the question being labeled
    assert len(responses.question.unique()) == 1
    question_id = responses.question.iloc[0]

    # Get the choices for this question
    choices = questions.ix[questions.id == question_id, 'choices'].tolist()[0]

    # Fill response types either with responses if they in the choices
    # or with the other response type if its not in the choices.
    # SMELLS!
    response_types = []
    for response in question_responses.response:
        if response not in choices:
            response = other_response_type
        response_types.append(response)
    responses['response_type'] = response_types

    return responses
