"""MIT License

Copyright (c) 2021 Aleksandr Kotlyar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import os
import sys

from more_itertools import flatten

ALLURE_REPORT_DIRECTORY_PATH = sys.argv[1]
ALLURE_TEST_CASES_PATH = os.path.join(
    ALLURE_REPORT_DIRECTORY_PATH, 'data', 'test-cases'
)
ALLURE_TEST_CASES = os.listdir(ALLURE_TEST_CASES_PATH)


def success_test_cases() -> list:
    """From all test-cases/*.json files collect json-files with "status": "passed"."""
    success_cases = []
    for test_case in ALLURE_TEST_CASES:
        with open(os.path.join(ALLURE_TEST_CASES_PATH, test_case), 'r') as tc:
            if json.load(tc).get('status') == "broken":
                success_cases.append(test_case)
    return success_cases


ALLURE_SUCCESS_TEST_CASES = success_test_cases()


def find(key, value):
    if isinstance(value, dict):
        for k, v in value.items():
            if k == key and v:
                yield v
            elif isinstance(v, (dict, list)):
                for result in find(key, v):
                    yield result


def allure_attachment_sources():
    """From each collected "passed" test-case find all "attachments.source" in steps."""
    attachment_sources = []
    for test_case in ALLURE_SUCCESS_TEST_CASES:
        with open(os.path.join(ALLURE_TEST_CASES_PATH, test_case), 'r') as json_file:
            attachment_sources.append(find('attachments', json.load(json_file)))
    attachment_sources = list(flatten(flatten(attachment_sources)))
    attachment_sources = [attachment['source'] for attachment in attachment_sources]
    return attachment_sources


ALLURE_ATTACHMENT_SOURCES = allure_attachment_sources()


def clean_allure_attachments_of_passed_tests():
    """Go to attachments/ and clean collected "sources" one by one."""
    for attachment in ALLURE_ATTACHMENT_SOURCES:
        attachment_path = os.path.join(
            ALLURE_REPORT_DIRECTORY_PATH, 'data', 'attachments', attachment
        )
        if os.path.exists(attachment_path):
            os.remove(attachment_path)
        else:
            print(f"The file {attachment_path} does not exist")


clean_allure_attachments_of_passed_tests()


def rewrite(key, data):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                data[k] = []
            elif isinstance(v, (dict, list)):
                rewrite(key, v)
        return data


def rewrite_all_test_cases_with_empty_attachments():
    """Rewrite all test-cases with empty "attachments": [ ]."""
    for test_case in ALLURE_SUCCESS_TEST_CASES:
        with open(os.path.join(ALLURE_TEST_CASES_PATH, test_case), 'r') as json_file:
            data = json.load(json_file)

        data = rewrite('attachments', data)

        with open(os.path.join(ALLURE_TEST_CASES_PATH, test_case), "w") as json_file:
            json.dump(data, json_file)


rewrite_all_test_cases_with_empty_attachments()
