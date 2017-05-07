# Google Survey

Get the results of a Google Survey with `google_survey`.

## Install

You can install the `google_survey` package with `pip`.

```bash
pip install -e git+git://github.com/madison-python/google-survey.git#egg=google_survey
```

## Use

To download the results of a Google Survey, you need the name of the
Google Sheet containing the results of the survey, and a path to a
credentials file that gives access to those results.

### Requirements

1. The name of the Google Sheet containing the results of the survey.
   Usually it will be named something like "Name of my survey (Responses)".
2. A Service Account Credentials file,
   e.g. "path/to/service-account-creds.json"

### Instructions

There are two steps involved in allowing API access to the Google Sheet
containing the survey results. The first step is to create new
Service Account credentials, which can be downloaded as a .json file.
This file is required in order to use `gspread` to connect to the Google
Sheets API. Within this .json file is a (machine-generated) email address.
The second step is to share the Google Sheet containing the results of
the survey with this email address.

1. Go to console.developer.google.com. Create a new project (or use an
   existing one). I called mine "madpy". Using this project, enable
   the Google Sheets API via the Dashboard, and then create new Service
   Account Credentials. You should get a .json file at the end. Ta da!
2. Go to drive.google.com, locate the Google Sheet with the results
   of the survey, and share the Google Sheet with the email address that
   was created along with the Service Account Credentials. Open up the
   .json file downloaded in the previous step to find the email address.
   Share this email address with the Google Sheet like you would any
   other collaborator. Now you can authenticate with the Service Account
   Credentials and download the results of your survey.

Now you are ready to download the results of the Google Survey with python!

### Using google_survey in scripts

Here's how you get just the responses to a survey. Basically this just downloads the Google Sheet containing the survey results in wide format.

```python
import google_survey
sheet_name = "Name of my survey (Responses)"
creds_file = "path/to/service-account-creds.json"
wide_responses = google_survey.get_responses(sheet_name, creds_file)
```

Usually survey responses are better off in long format. To melt the data from wide to long format, use the `tidy_responses` function.

```python
long_responses = google_survey.tidy_responses(wide_responses)
```

It's also helpful to know information about the questions in the survey. To extract question metadata from the survey html page itself, just provide the survey url to the `get_questions` function.

```python
survey_url = 'https://docs.google.com/forms/my-survey-url/viewform'
questions = google_survey.get_questions(survey_url)
```

The simplest way to use `google_survey` is to provide all of the necessary information in a simple yaml file, and pass this to the `google_survey.get` function.

```yaml
---
# contents of survey-info.yaml
sheet_name: Name of my survey (Responses)
creds_file: path/to/service-account-creds.json
survey_url: https://docs.google.com/forms/my-survey-url/viewform
```

```python
responses = google_survey.get('survey-info.yaml')
```

### Using google_survey from the command line

You can run Google Survey from the command line as a python module,
denoted by the "-m" flag, provided you pass the path to the survey info.

```bash
python -m google_survey survey-info.yaml > `date +results-%Y-%m-%d.csv`
```
