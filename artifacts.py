import logging
import os
from subprocess import call  # nosec

import requests

CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
CI_COMMIT_REF_NAME = os.environ.get('CI_COMMIT_REF_NAME')
PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')

PAYLOAD = {
    'job': 'pages',
    'scope': 'success'
}
HEADERS = {
    'PRIVATE-TOKEN': PRIVATE_TOKEN
}
URL = f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs'

RESPONSE = requests.request("GET", URL, headers=HEADERS, params=PAYLOAD)

LATEST_JOB_ID = RESPONSE.json()[0]['id']
logging.info(LATEST_JOB_ID)

URL = f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs/' \
      f'{LATEST_JOB_ID}/artifacts'

RESPONSE = requests.request("GET", URL, headers=HEADERS)

FILE_NAME = 'artifacts.zip'
ARTIFACTS = open(FILE_NAME, 'wb')
ARTIFACTS.write(RESPONSE.content)
ARTIFACTS.close()

PATH_TO_ZIP = FILE_NAME
PATH_TO_OUT = '.public'
UNZIP = ['unzip', '-o', PATH_TO_ZIP, '-d', PATH_TO_OUT]

call(UNZIP, shell=True)  # nosec
