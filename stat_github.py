# pylint: disable=missing-function-docstring
import os
from pprint import pprint

import anybadge
import requests

PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')
TOKEN = os.environ.get('TOKEN')
OWNER = os.environ.get('CI_PROJECT_NAMESPACE')
REPO = os.environ.get('CI_PROJECT_NAME')
CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
GH_UNIQUE_CLONES_BADGE = os.environ.get('GH_UNIQUE_CLONES_BADGE')
CI_JOB_URL = os.environ.get('CI_JOB_URL')


def get_current_uniques_stat():
    stat = requests.get(
        url='https://api.github.com/repos/{0}/{1}/traffic/clones'.format(OWNER, REPO),
        headers={'Authorization': f'token {TOKEN}'},
        params={'per': 'week'})

    if stat.status_code != 200:
        return 0

    pprint(stat.json())
    return stat.json()['uniques']


def get_archive_uniques_stat():
    stat = requests.get(
        url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}'
            f'/jobs/artifacts/master/raw/gh_unique_clones.log?job=stats:github:unique:clones')

    if stat.status_code != 200:
        return 0

    pprint(stat)
    return int(stat.text)


def sum_uniques_stats(current, archive):
    if archive == 0:
        return current

    stats = current + archive
    pprint(stats)
    return stats


def save_uniques_stats(stats):
    with open('gh_unique_clones.log', 'w') as file:
        file.write(str(stats))


def public_uniques_stats(stats):
    badge = anybadge.Badge(label='downloads/unique',
                           value=stats,
                           default_color='green',
                           num_padding_chars=1)
    badge.write_badge('gh_unique_clones.svg', overwrite=True)

    requests.put(
        url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/badges/{GH_UNIQUE_CLONES_BADGE}',
        json={'image_url': f'{CI_JOB_URL}/artifacts/raw/gh_unique_clones.svg'},
        headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})
    pprint('badge published')


CURRENT = get_current_uniques_stat()
ARCHIVE = get_archive_uniques_stat()
SUMMARY = sum_uniques_stats(CURRENT, ARCHIVE)
save_uniques_stats(SUMMARY)
public_uniques_stats(SUMMARY)
