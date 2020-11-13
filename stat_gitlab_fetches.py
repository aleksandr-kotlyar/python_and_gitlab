# pylint: disable=missing-function-docstring
import os
from pprint import pprint

from stat_git_downloads import get_current_gitlab_stat, get_archive_stat, save_stats, \
    public_stats, merge_two_lists_of_dicts_by_key_condition

GL_COUNT_CLONES_BADGE = os.environ.get('GL_COUNT_CLONES_BADGE')
LOG_FILE = 'gl_fetches.json'
BADGE_SVG = 'gl_fetches.svg'


def sum_clones_stats(stats) -> int:
    print('sum_clones_stats')

    summary = sum(s['count'] for s in stats)
    pprint(summary)
    return summary


CURRENT = get_current_gitlab_stat()['fetches']['days']
ARCHIVE = get_archive_stat(GL_COUNT_CLONES_BADGE)
MERGED = merge_two_lists_of_dicts_by_key_condition(CURRENT, ARCHIVE, key1='date', key2='count')
SUMMARY: int = sum_clones_stats(MERGED)
save_stats(MERGED, LOG_FILE)
public_stats(SUMMARY, 'downloads/gitlab/fetches', BADGE_SVG, GL_COUNT_CLONES_BADGE, LOG_FILE)
