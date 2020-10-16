import os

import requests

CI_PROJECT_ID = os.getenv('CI_PROJECT_ID')
SOURCE_BRANCH = os.getenv('CI_COMMIT_REF_NAME')
PRIVATE_TOKEN = os.getenv('PRIVATE_TOKEN')


def get_opened_merge_requests_of_source_branch(project, branch):
    """Get last opened merge request for source branch"""
    response = requests.request(method='get', url=f'https://gitlab.com/api/v4/projects/{project}/merge_requests',
                                params={'source_branch': branch, 'state': 'opened'})
    assert response.status_code == 200
    return response.json()


def get_target_branch_of_merge_request(merge_request):
    print(merge_request[0]['target_branch'])
    return merge_request[0]['target_branch']


def get_latest_job_artifact_of_branch(branch):
    response = requests.request(
        method='get',
        url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/jobs/artifacts/{branch}/raw/pylint/score?job=Pylint',
        headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})

    print(response.text)
    return response.text


merge_requests = get_opened_merge_requests_of_source_branch(CI_PROJECT_ID, SOURCE_BRANCH)

if not merge_requests:
    exit(0)

mr = merge_requests[0]
target_branch = get_target_branch_of_merge_request(mr)
target_score = get_latest_job_artifact_of_branch(target_branch)
source_score = get_latest_job_artifact_of_branch(SOURCE_BRANCH)

if source_score < target_score:
    print('Quality become lower:', source_score, '<', target_score)
    exit(1)
