from operator import itemgetter
from pprint import pprint


def merge_two_lists_of_dicts_by_key_condition(ld1, ld2):
    """Update dict with same timestamp by higher 'unique' key value."""
    if not ld2:
        return ld1

    listdict = ld1['clones'] + ld2['clones']
    listdict = sorted(listdict, key=itemgetter('timestamp'))
    for i in range(len(listdict) - 1):
        for j in range(i + 1, len(listdict)):
            if listdict[i]['timestamp'] == listdict[j]['timestamp']:
                if listdict[i]['uniques'] < listdict[j]['uniques']:
                    listdict.remove(listdict[i])
                else:
                    listdict.remove(listdict[j])
                break

    print(f'list1: {len(ld1)}')
    print(f'list2: {len(ld2)}')
    pprint(f'merged_list\n{listdict}')
    print(f'merged_list: {len(listdict)}')
    return listdict
