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
