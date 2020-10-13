import os
from zipfile import ZipFile

import requests

CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
CI_COMMIT_REF_NAME = os.environ.get('CI_COMMIT_REF_NAME')
PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')

url = f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs'

payload = {
    'ref': CI_COMMIT_REF_NAME,
    'job': 'pages',
    'status': 'success'
}
headers = {
    'PRIVATE-TOKEN': PRIVATE_TOKEN
}

response = requests.request("GET", url, headers=headers, params=payload)

latest_job_id = response.json()[0]['id']

url = f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs/' \
      f'{latest_job_id}/artifacts'

headers.update({'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache'})

response = requests.request("GET", url, headers=headers)

artifacts = open('artifacts.zip', 'wb')
artifacts.write(response.content)
artifacts.close()

with ZipFile('artifacts.zip', 'r') as zip_obj:
    zip_obj.extractall()
