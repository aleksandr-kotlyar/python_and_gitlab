# pylint: disable=missing-function-docstring
import os
from pprint import pprint

import anybadge
import requests

import merge_dict

PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN')
TOKEN = os.environ.get('TOKEN')
OWNER = os.environ.get('CI_PROJECT_NAMESPACE')
REPO = os.environ.get('CI_PROJECT_NAME')
CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
GH_UNIQUE_CLONES_BADGE = os.environ.get('GH_UNIQUE_CLONES_BADGE')
CI_JOB_URL = os.environ.get('CI_JOB_URL')
LOG_FILE = 'gh_unique_clones.json'


def get_current_uniques_stat():
    print('get_current_uniques_stat')
    stat = requests.get(
        url='https://api.github.com/repos/{0}/{1}/traffic/clones'.format(OWNER, REPO),
        headers={'Authorization': f'token {TOKEN}'},
        params={'per': 'day'})

    if stat.status_code != 200:
        return 0

    pprint(stat.json())
    return stat.json()


def get_archive_uniques_stat():
    print('get_archive_uniques_stat')
    stat = requests.get(
        url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}'
            f'/jobs/artifacts/master/raw/{LOG_FILE}?job=stats:github:unique:clones')

    if stat.status_code != 200:
        return 0

    pprint(stat)
    return int(stat.text)


def sum_uniques_stats(current, archive):
    print('sum_uniques_stats')
    if archive == 0:
        return current

    stats = merge_dict.merge_two_lists_of_dicts_by_key_condition(current, archive)
    pprint(stats)
    return stats


def save_uniques_stats(stats):
    print('save_uniques_stats')
    with open(LOG_FILE, 'w') as file:
        file.write(str(stats))


def public_uniques_stats(stats):
    print('public_uniques_stats')
    badge = anybadge.Badge(label='downloads/unique',
                           value=stats['uniques'],
                           default_color='green',
                           num_padding_chars=1)
    badge.write_badge('gh_unique_clones.svg', overwrite=True)

    badge_put = requests.put(
        url=f'https://gitlab.com/api/v4/projects/{CI_PROJECT_ID}/badges/{GH_UNIQUE_CLONES_BADGE}',
        json={'link_url': f'{CI_JOB_URL}/artifacts/raw/{LOG_FILE}',
              'image_url': f'{CI_JOB_URL}/artifacts/raw/gh_unique_clones.svg'},
        headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})

    if badge_put.status_code in [200, 201]:
        pprint('badge published')


CURRENT = get_current_uniques_stat()
ARCHIVE = get_archive_uniques_stat()
SUMMARY = sum_uniques_stats(CURRENT, ARCHIVE)
save_uniques_stats(SUMMARY)
public_uniques_stats(SUMMARY)
