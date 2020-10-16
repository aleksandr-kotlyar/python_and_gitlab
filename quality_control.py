import os
import sys

import requests

CI_PROJECT_ID = os.getenv('CI_PROJECT_ID')
SOURCE_BRANCH = os.getenv('CI_COMMIT_REF_NAME')
PRIVATE_TOKEN = os.getenv('PRIVATE_TOKEN')


def get_opened_merge_requests_of_source_branch(project, branch):
    """Get list of opened merge requests for source branch"""
    response = requests.request(method='get',
                                url=f'https://gitlab.com/api/v4/projects/{project}/merge_requests',
                                params={'source_branch': branch, 'state': 'opened'})
    assert response.status_code == 200
    return response.json()


def get_target_branch_of_merge_request(merge_request):
    """Get target_branch from merge_request."""
    return merge_request['target_branch']


def get_latest_job_artifact_of_branch(project, branch):
    """Get latest score.log artifact for branch."""
    result = requests.request(method='get',
                              url=f'https://gitlab.com/api/v4/projects/{project}/jobs/artifacts/'
                                  f'{branch}/raw/pylint/score?job=Pylint',
                              headers={'PRIVATE-TOKEN': PRIVATE_TOKEN}).text
    print(f'{branch} score = {result}')
    return result


MERGE_REQUESTS = get_opened_merge_requests_of_source_branch(CI_PROJECT_ID, SOURCE_BRANCH)

if not MERGE_REQUESTS:
    sys.exit(0)

LAST_MERGE_REQUEST = MERGE_REQUESTS[0]
TARGET_BRANCH = get_target_branch_of_merge_request(LAST_MERGE_REQUEST)
TARGET_SCORE = get_latest_job_artifact_of_branch(CI_PROJECT_ID, TARGET_BRANCH)
SOURCE_SCORE = get_latest_job_artifact_of_branch(CI_PROJECT_ID, SOURCE_BRANCH)

if SOURCE_SCORE < TARGET_SCORE:
    print(f'Quality become lower: {SOURCE_SCORE} vs {TARGET_SCORE}')
    sys.exit(1)
