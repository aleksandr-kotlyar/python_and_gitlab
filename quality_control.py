import logging
import os

import requests

CI_PROJECT_ID = os.getenv('CI_PROJECT_ID')
SOURCE_BRANCH = os.getenv('CI_COMMIT_REF_NAME')
PRIVATE_TOKEN = os.getenv('PRIVATE_TOKEN')


def get_opened_merge_request_of_source_branch():
    """Get last opened merge request for source branch"""
    response = requests.request(method='get', url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/merge_requests',
                                params={'source_branch': SOURCE_BRANCH, 'state': 'opened'})
    assert response.status_code == 200
    return response.json()[0]


def get_target_branch_of_merge_request(merge_request):
    logging.info(merge_request['target_branch'])
    return merge_request['target_branch']


def get_latest_job_artifact_of_branch(branch):
    response = requests.request(
        method='get',
        url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs/artifacts/{branch}/raw/pylint/score?job=Pylint',
        headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})

    print(response.text)
    return response.text


mr = get_opened_merge_request_of_source_branch()
target_branch = get_target_branch_of_merge_request(mr)
target_score = get_latest_job_artifact_of_branch(target_branch)
source_score = get_latest_job_artifact_of_branch('linter')

assert source_score < target_score
