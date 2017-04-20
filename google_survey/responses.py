from os import path
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials


def get_responses(sheet_name, service_account_creds):
    """Download a Google Sheet containing the responses to a Google Survey.

    Args:
        sheet_name: The name of the Google Sheet containing the responses
            of the Google Survey. The name can contain weird characters
            such as spaces and parentheses, e.g. "MadPy (Responses)".
        service_account_creds: Path to a json keyfile containing Service
            Account Credentials obtained from the Google Developer Console.
            These credentials must be allowed access to the Google Sheets API.
            Also, the machine-generated email created with these credentials
            needs to be allowed access to the Google Sheet containing the
            Survey responses.
    Returns:
        pandas.DataFrame of Google Survey responses in wide format, with
        the responses to each question spread out over multiple rows.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        service_account_creds, scopes = 'https://spreadsheets.google.com/feeds',
    )
    google_sheets = gspread.authorize(credentials)
    worksheet = google_sheets.open(sheet_name).sheet1
    return pandas.DataFrame(worksheet.get_all_records())


def tidy_responses(google_survey_responses):
    """Tranform Google Survey responses from wide to long format."""
    wide_responses = google_survey_responses.copy()

    # Assign a unique identifier for each survey taker
    person_ids = ['p{}'.format(i) for i in list(wide_responses.index)]
    wide_responses.insert(0, 'person', person_ids)

    # Melt the data from wide to long
    response_strs = pandas.melt(wide_responses, 'person', var_name='question',
                                value_name='response_str')

    # Split response strings into one response per row
    responses = melt_responses(response_strs)

    return responses


def melt_response_strs(response_strs):
    """Melt response strings containing multiple responses.

    An example response str is 'Libraries, Offices'. The resulting DataFrame
    will have two rows, one for each response item, e.g, ['Libraries', 'Offices'].
    """
    melted_rows = []
    for row in response_strs.itertuples():
        response_str = row.response_str
        try:
            responses = [response.strip() for response in response_str.split(',')]
        except AttributeError:
            # If the response can't be split, they probably didn't answer
            # this question, so just put the empty value in a list.
            responses = [response_str]

        # Create a new row for each response
        for response_n, response in enumerate(responses):
            melted_rows.append(dict(person=row.person, question=row.question,
                                    response_n=response_n, response=response))

    ordered_columns = 'person question response_n response'.split()
    return pandas.DataFrame.from_records(melted_rows, columns=ordered_columns)
