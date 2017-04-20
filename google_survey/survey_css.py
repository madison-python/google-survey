"""Classes in the survey html for extracting question data.

These were obtained by first downloading the survey html and
inspecting the results in a browser.

    import google_survey
    import webbrowser
    google_survey.get_survey_html('survey-url.txt', output='survey.html')
    webbrowser.open('survey.html')

Warning! Do not trust... Always verify.
"""
CLS_QUESTION_LIST = 'freebirdFormviewerViewItemList'
CLS_QUESTION = 'freebirdFormviewerViewItemsItemItem'
CLS_QUESTION_TITLE = 'freebirdFormviewerViewItemsItemItemTitle'

CLS_QUESTION_CHECKBOX = 'freebirdFormviewerViewItemsCheckboxLabel'
CLS_QUESTION_RADIO = 'freebirdFormviewerViewItemsRadioChoice'
CLS_QUESTION_TYPES = [CLS_QUESTION_CHECKBOX, CLS_QUESTION_RADIO]
