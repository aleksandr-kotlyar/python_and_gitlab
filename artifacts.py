import os
import subprocess
from pprint import pprint

import requests

CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
CI_COMMIT_REF_NAME = os.environ.get('CI_COMMIT_REF_NAME')
PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')

url = f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs'

payload = {
    'job': 'pages',
    'scope': 'success'
}
headers = {
    'PRIVATE-TOKEN': PRIVATE_TOKEN
}

response = requests.request("GET", url, headers=headers, params=payload)
latest_job_id = response.json()[0]['id']
print(latest_job_id)
url = f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs/' \
      f'{latest_job_id}/artifacts'

response = requests.request("GET", url, headers=headers)

file_name = 'artifacts.zip'
artifacts = open(file_name, 'wb')
artifacts.write(response.content)
artifacts.close()
subprocess.Popen('unzip -o ' + file_name, shell=True, cwd='.public').wait()
