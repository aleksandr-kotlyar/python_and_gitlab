import logging

STRING = """#EXTM3U
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=429362,RESOLUTION=704x528,FRAME-RATE=25.000,CODECS="avc1.64001e,mp4a.40.2"
    index-f1-v1-a1.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=830436,RESOLUTION=704x528,FRAME-RATE=25.000,CODECS="avc1.64001e,mp4a.40.2"
    index-f2-v1-a1.m3u8
    #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1330222,RESOLUTION=704x528,FRAME-RATE=25.000,CODECS="avc1.64001e,mp4a.40.2"
    index-f3-v1-a1.m3u8
    \
    """


def test_cut_m3u8():
    """ (generator) Find first string contains m3u8 and print """
    lines = STRING.split('\n')
    m3u8 = next((line for line in lines if 'm3u8' in line), None)
    logging.info(m3u8)


def test_cut_m3u8_another():
    """ (loop with break) Find first string contains m3u8 and print """
    lines = STRING.split('\n')
    m3u8 = ''
    for line in lines:
        if 'm3u8' in line:
            m3u8 = line
            break
    logging.info(m3u8)


def test_any_from_list_is_in_string():
    """ Test method any() and print if any finds any """
    arr = ['ab', 'cd', 'ej']
    string = 'cd'
    if any(test in string for test in arr):
        logging.info('true')
    else:
        logging.info('false')
