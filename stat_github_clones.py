# pylint: disable=missing-function-docstring
import os
from pprint import pprint

from stat_git_downloads import get_current_github_stat, get_archive_stat, save_stats, \
    public_stats, merge_two_lists_of_dicts_by_key_condition

GH_COUNT_CLONES_BADGE = os.environ.get('GH_COUNT_CLONES_BADGE')
LOG_FILE = 'gh_clones.json'
BADGE_SVG = 'gh_clones.svg'


def sum_clones_stats(stats) -> int:
    print('sum_clones_stats')

    summary = sum(s['count'] for s in stats)
    pprint(summary)
    return summary


CURRENT = get_current_github_stat()['clones']
ARCHIVE = get_archive_stat(GH_COUNT_CLONES_BADGE)
MERGED = merge_two_lists_of_dicts_by_key_condition(CURRENT, ARCHIVE, 'timestamp', 'count')
SUMMARY: int = sum_clones_stats(MERGED)
save_stats(MERGED, LOG_FILE)
public_stats(SUMMARY, 'downloads/github/clones', BADGE_SVG, GH_COUNT_CLONES_BADGE, LOG_FILE)
