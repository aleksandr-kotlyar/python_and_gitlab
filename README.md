# Python and GitLabCI for test automation (QA)
Hello! Here you can find examples of
* Code quality checking jobs
* GitLabCI: jobs with pytest execution
* GitLabCI: slack integration
* GitLabCI: Selenium in Docker test execution
* Pytest: slack integration
* Pytest: test parametrization
* Allure: logger messages as steps
* Allure: log each "requests" lib action
* Multi-thread method execution examples
* Sitemap checkers
* Azure pipeline pytest execution

## Installation 
Must have `python 3.7+`

`pip3 install -r requirements.txt`

## Allure reports
Type this in your project console:

`pytest --alluredir=reports src\test`

and after test execution type `allure serve reports` then your browser will open reports.

