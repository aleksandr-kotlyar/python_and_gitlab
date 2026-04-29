# Python and GitLab CI/CD Testing Cookbook

Practical examples for building CI/CD-based QA automation workflows with Python, pytest, GitLab CI, Docker, Allure, Slack notifications, and Azure Pipelines.

This repository is a cookbook of reusable examples and patterns for QA engineers, SDETs, and QA leads who want to integrate automated tests, quality checks, reports, and notifications into delivery pipelines.

## What this project covers

- Python test execution with pytest
- GitLab CI jobs for automated test runs
- Dockerized Selenium execution
- Slack notifications from CI and pytest
- Allure reporting and logging examples
- Code quality checks with pylint and Black
- Test parametrization patterns
- Multi-thread execution examples
- Sitemap status checking
- Azure Pipelines pytest execution

## Scope

This is not a single production-ready test framework.

It is a collection of independent CI/CD testing examples that can be reused, adapted, or combined in real QA automation projects.

## How to use this repository

Choose a scenario:

| Scenario | What it demonstrates |
|---|---|
| GitLab CI pytest execution | Running automated tests inside GitLab pipelines |
| GitLab artifacts | Passing and publishing test outputs between jobs |
| Slack notifications | Sending pipeline/test feedback to team channels |
| Selenium in Docker | Running browser tests in isolated containers |
| Allure reporting | Producing readable test reports and logged steps |
| Code quality checks | Running pylint and formatting checks in CI |
| Azure Pipelines | Running pytest outside GitLab CI |
| Sitemap checking | Validating public links and HTTP statuses |

## Quick start

Requirements:

- Python 3.12+
- pip
- Docker, optional, for browser/Selenium examples
- Allure CLI, optional, for local report generation

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest src/tests
```

## Generate Allure report

```bash
pytest --alluredir=reports src/tests
allure serve reports
```

## Design goals

- keep test feedback close to the delivery pipeline
- make test results visible and actionable
- provide reusable CI/CD examples for QA automation teams
- demonstrate local and CI execution patterns
- combine tests, quality checks, reports, and notifications
