# pylint: disable=missing-function-docstring
import os
from pprint import pprint

from stat_github import get_current_github_stat, get_archive_stat, save_stats, public_stats, \
    merge_two_lists_of_dicts_by_key_condition

GH_COUNT_CLONES_BADGE = os.environ.get('GH_COUNT_CLONES_BADGE')
LOG_FILE = 'gh_clones.json'
BADGE_SVG = 'gh_clones.svg'


def sum_clones_stats(stats) -> int:
    print('sum_clones_stats')

    summary = sum(s['count'] for s in stats)
    pprint(summary)
    return summary


CURRENT = get_current_github_stat()['clones']
ARCHIVE = get_archive_stat('stats:github:clones', LOG_FILE)
MERGED = merge_two_lists_of_dicts_by_key_condition(CURRENT, ARCHIVE, 'timestamp', 'uniques')
SUMMARY: int = sum_clones_stats(MERGED)
save_stats(MERGED, LOG_FILE)
public_stats(SUMMARY, 'downloads/github/clones', BADGE_SVG, GH_COUNT_CLONES_BADGE, LOG_FILE)
