from setuptools import setup

setup(
    name='google_survey',
    packages=['google_survey'],
    install_requires=['gspread', 'oauth2client', 'pandas', 'fire', 'bs4', 'pyyaml']
)
