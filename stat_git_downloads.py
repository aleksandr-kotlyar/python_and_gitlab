# pylint: disable=missing-function-docstring
import os
import sys
from operator import itemgetter
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


def get_current_github_stat():
    print('get_current_stat')
    stat = requests.get(
        url='https://api.github.com/repos/{0}/{1}/traffic/clones'.format(OWNER, REPO),
        headers={'Authorization': f'token {TOKEN}'},
        params={'per': 'day'})

    pprint(stat.json())
    return stat.json()


def get_current_gitlab_stat():
    print('get_current_stat')
    stat = requests.get(
        url='https://gitlab.com/api/v4/projects/{0}/statistics'.format(CI_PROJECT_ID),
        headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})

    pprint(stat.json())
    return stat.json()


def get_archive_stat(badgeid):
    print('get_archive_stat')
    stat = requests.get(
        url='https://gitlab.com/api/v4/projects/{0}/badges/{1}'.format(CI_PROJECT_ID, badgeid))
    code = stat.status_code
    print(code)
    if code != 200:
        print('stat.status_code is', code)
        sys.exit(1)

    stat = stat.json()['link_url']
    stat = requests.get(stat).json()
    pprint(stat)
    return stat


def merge_two_lists_of_dicts_by_key_condition(ld1, ld2, key1, key2):
    """Update dict with same timestamp by higher 'unique' key value."""
    if not ld2:
        return ld1

    listdict = ld1 + ld2
    listdict = sorted(listdict, key=itemgetter(key1))
    for i in range(len(listdict) - 1):
        for j in range(i + 1, len(listdict)):
            if listdict[i][key1] == listdict[j][key1]:
                if listdict[i][key2] < listdict[j][key2]:
                    listdict.remove(listdict[i])
                else:
                    listdict.remove(listdict[j])
                break

    print(f'list1: {len(ld1)}')
    print(f'list2: {len(ld2)}')
    pprint(f'merged_list\n{listdict}')
    print(f'merged_list: {len(listdict)}')
    return listdict


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
              'image_url': f'{CI_JOB_URL}/artifacts/raw/{badgesvg}'},
        headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})

    if badge_put.status_code in [200, 201]:
        pprint('badge published')
