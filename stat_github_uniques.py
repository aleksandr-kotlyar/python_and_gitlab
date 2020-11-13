# pylint: disable=missing-function-docstring
import os
from pprint import pprint

import merge_dict
from stat_github import get_current_stat, get_archive_stat, save_stats, public_stats

GH_UNIQUE_CLONES_BADGE = os.environ.get('GH_UNIQUE_CLONES_BADGE')
LOG_FILE = 'gh_unique_clones.json'
BADGE_SVG = 'gh_unique_clones.svg'


def sum_uniques_stats(stats) -> int:
    print('sum_uniques_stats')

    summary = sum(s['uniques'] for s in stats)
    pprint(summary)
    return summary


CURRENT = get_current_stat()['clones']
ARCHIVE = get_archive_stat('stats:github:unique:clones', LOG_FILE)
MERGED = merge_dict.merge_two_lists_of_dicts_by_key_condition(CURRENT, ARCHIVE)
SUMMARY: int = sum_uniques_stats(MERGED)
save_stats(MERGED, LOG_FILE)
public_stats(SUMMARY, 'downloads/github/unique', BADGE_SVG, GH_UNIQUE_CLONES_BADGE, LOG_FILE)