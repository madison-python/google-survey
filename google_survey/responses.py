import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials

# Requesting authentication to Google Sheets API
SCOPES = 'https://spreadsheets.google.com/feeds'


def get_responses(sheet_name, creds_file):
    """Download a Google Sheet containing the responses to a Google Survey.

    Args:
        sheet_name: The name of the Google Sheet containing the responses
            of the Google Survey. The name can contain weird characters
            such as spaces and parentheses, e.g. "MadPy (Responses)".
        creds_file: Path to a json keyfile containing Service
            Account Credentials obtained from the Google Developer Console.
            These credentials must be enabled access to the Google Sheets API.
            Also, the machine-generated email created with these credentials
            needs to be allowed access to the Google Sheet containing the
            Survey responses.
    Returns:
        pandas.DataFrame of Google Survey responses in wide format, with
        the responses to each question spread out over multiple rows.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, SCOPES)
    google_sheets = gspread.authorize(creds)
    worksheet = google_sheets.open(sheet_name).sheet1
    responses = pandas.DataFrame(worksheet.get_all_records())
    return responses
