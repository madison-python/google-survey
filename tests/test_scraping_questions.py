import pytest
import google_survey

pytest.mark.usefixture('betamax_session')


class TestNewMeetupSurvey:
    NEW_MEETUP_SURVEY = 'https://docs.google.com/forms/d/e/1FAIpQLSdIg3yZqSPxCac-ESLjnlfEcE5PLBo02TeBP42lgZJlUlry5w/viewform'

    def test_questions_length(self, betamax_session):
        questions = google_survey.get_questions(
            survey_url=self.NEW_MEETUP_SURVEY,
            requests_session=betamax_session,
        )
        assert len(questions) == 16


class TestMadpyHabitsSurvey:
    MADPY_HABITS_SURVEY = 'https://docs.google.com/forms/d/e/1FAIpQLScnwwfdLN_iUNaZEyks62Y_2DO8qADWGZU0ykVoWSRcnDSkfA/viewform'

    def test_required_question_asterisk_removed(self, betamax_session):
        questions = google_survey.get_questions(
            survey_url=self.MADPY_HABITS_SURVEY,
            requests_session=betamax_session,
        )
        given = questions.ix[questions.question_id == 'q0', 'question'].squeeze()
        expected = "What's your screen name?"
        assert given == expected
