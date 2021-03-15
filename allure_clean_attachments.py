"""
From all test-cases/*.json files collect json-files with "status": "passed".
From each collected "passed" test-case find all "attachments.source" in steps.
Go to attachments/ and clean collected "sources" one by one.
Rewrite all test-cases with empty "attachments": [ ].
"""
import json
import os
import sys

from more_itertools import flatten

allure_report_directory_path = sys.argv[1]
allure_test_cases_path = os.path.join(
    allure_report_directory_path, 'data', 'test-cases'
)
ALLURE_TEST_CASES = os.listdir(allure_test_cases_path)


def success_test_cases() -> list:
    """From all test-cases/*.json files collect json-files with "status": "passed"."""
    success_cases = []
    for test_case in ALLURE_TEST_CASES:
        with open(os.path.join(allure_test_cases_path, test_case), 'r') as tc:
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
        with open(os.path.join(allure_test_cases_path, test_case), 'r') as tc:
            attachment_sources.append(find('attachments', json.load(tc)))
    attachment_sources = list(flatten(flatten(attachment_sources)))
    attachment_sources = [attachment['source'] for attachment in attachment_sources]
    return attachment_sources


ALLURE_ATTACHMENT_SOURCES = allure_attachment_sources()


def clean_allure_attachments_of_passed_tests():
    """Go to attachments/ and clean collected "sources" one by one."""
    for attachment in ALLURE_ATTACHMENT_SOURCES:
        attachment_path = os.path.join(
            allure_report_directory_path, 'data', 'attachments', attachment
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
        with open(os.path.join(allure_test_cases_path, test_case), 'r') as tc:
            data = json.load(tc)

        data = rewrite('attachments', data)

        with open(os.path.join(allure_test_cases_path, test_case), "w") as tc:
            json.dump(data, tc)


rewrite_all_test_cases_with_empty_attachments()
