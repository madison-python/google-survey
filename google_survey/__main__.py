import sys
import fire
from .all import get


def download_survey(survey_info_yaml, output=None):
    responses = get(survey_info_yaml)
    if output is None:
        output = sys.stdout
    responses.to_csv(output, index=False)

if __name__ == '__main__':
    fire.Fire(download_survey)
