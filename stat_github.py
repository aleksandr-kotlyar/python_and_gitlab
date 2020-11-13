# pylint: disable=missing-function-docstring
import json
import os
from pprint import pprint

import anybadge
import requests

CI_COMMIT_BRANCH = os.environ.get('CI_COMMIT_BRANCH')
CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
CI_JOB_URL = os.environ.get('CI_JOB_URL')

OWNER = os.environ.get('CI_PROJECT_NAMESPACE')
REPO = os.environ.get('CI_PROJECT_NAME')

PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')
TOKEN = os.environ.get('TOKEN')


def get_current_stat():
    print('get_current_stat')
    stat = requests.get(
        url='https://api.github.com/repos/{0}/{1}/traffic/clones'.format(OWNER, REPO),
        headers={'Authorization': f'token {TOKEN}'},
        params={'per': 'day'})

    pprint(stat.json())
    return stat.json()


def get_archive_stat(job, logfile):
    print('get_archive_stat')
    stat = requests.get(
        url='https://gitlab.com/api/v4/projects/{0}/jobs/artifacts/{1}/raw/{2}?job={3}'
            .format(CI_PROJECT_ID, CI_COMMIT_BRANCH, logfile, job))

    if stat.status_code != 200:
        return []

    stat = stat.text.replace("'", '"')
    stat = json.loads(stat)
    pprint(stat)
    return stat


def save_stats(stats, logfile):
    print('save_stats')
    with open(logfile, 'w') as file:
        file.write(str(stats))


def public_stats(summary: int, label, badgesvg, badgeid, logfile):
    print('public_stats')
    badge = anybadge.Badge(label=label,
                           value=summary,
                           default_color='green',
                           num_padding_chars=1)
    badge.write_badge(badgesvg, overwrite=True)

    badge_put = requests.put(
        url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/badges/{badgeid}',
        json={'link_url': f'{CI_JOB_URL}/artifacts/raw/{logfile}',
              'image_url': f'{CI_JOB_URL}/artifacts/raw/gh_unique_clones.svg'},
        headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})

    if badge_put.status_code in [200, 201]:
        pprint('badge published')
