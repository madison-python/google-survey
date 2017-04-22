import sys
import fire
from .responses import get_responses

class GoogleSurveyCLI:
    def get(self, sheet_name, creds_file, output=None):
        responses = get_responses(sheet_name, creds_file)
        if output is None:
            output = sys.stdout
        responses.to_csv(output, index=False)

if __name__ == '__main__':
    cli = GoogleSurveyCLI()
    fire.Fire(cli)
