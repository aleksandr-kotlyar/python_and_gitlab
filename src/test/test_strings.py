import logging

from pytest import mark

STRING = """#EXTM3U
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=429362,RESOLUTION=704x528,FRAME-RATE=25.000,CODECS="avc1.64001e,mp4a.40.2"
    index-f1-v1-a1.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=830436,RESOLUTION=704x528,FRAME-RATE=25.000,CODECS="avc1.64001e,mp4a.40.2"
    index-f2-v1-a1.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1330222,RESOLUTION=704x528,FRAME-RATE=25.000,CODECS="avc1.64001e,mp4a.40.2"
    index-f3-v1-a1.m3u8
    \
    """


@mark.parametrize('source_string, desired_part', [(STRING, 'm3u8')])
def test_source_file_contains_desired_string(source_string, desired_part):
    """
    Pythonic way to find string in file.
    Use generator to find first string in file contains desired part and print this string.
    """
    lines = source_string.split('\n')
    desired_string = next((line for line in lines if desired_part in line), None)
    logging.info(desired_string)
    assert desired_string != '' or desired_string is not None


@mark.parametrize('source_list, desired_part', [(STRING.split('\n'), 'm3u8')])
def test_source_list_of_strings_contains_desired_string(source_list, desired_part):
    """
    Classic way to find string in list.
    Find first string in list contains desired part and print this string.
    """
    desired_string = ''
    for line in source_list:
        if desired_part in line:
            desired_string = line
            break
    logging.info(desired_string)
    assert desired_string != '' or desired_string is not None


@mark.parametrize('source_list, desired_strings', [
    (['ab', 'cd', 'ej'], ['ad', 'ab']),
    (['ab', 'cd', 'ej'], ['d', 'e']),
    (['ab', 'cd', 'ej'], ['dc', '']),
])
def test_source_list_contains_any_of_desired_strings(source_list, desired_strings):
    """ Test method any() and fail if any didn't find any equal string ;) """
    assert any(string in desired_strings for string in source_list), \
        f'No one from {desired_strings} is equal any of {source_list}'


@mark.parametrize('source_list, desired_parts', [
    (['ab', 'cd', 'ej'], ['ad', 'ab']),
    (['ab', 'cd', 'ej'], ['v', 'e']),
    (['ab', 'cd', 'ej'], ['f', 'k']),
    (['ab', 'cd', 'ej'], ['vg', '']),
])
def test_source_list_contains_any_of_desired_parts(source_list, desired_parts):
    """ Test method any() and fail if any didn't find any part string ;) """
    assert any(part in source_string for source_string in source_list for part in desired_parts), \
        f'No one from {desired_parts} is a part any of {source_list}'
