import sys
import fire
from .all import get

class GoogleSurveyCLI:
    def get(self, survey_info_yaml, output=None):
        responses = get(survey_info_yaml)
        if output is None:
            output = sys.stdout
        responses.to_csv(output, index=False)

if __name__ == '__main__':
    cli = GoogleSurveyCLI()
    fire.Fire(cli)
