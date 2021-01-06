# Python and GitLabCI for test automation (QA)

![GitHub statistics](https://raw.githubusercontent.com/aleksandr-kotlyar/python_and_gitlab/traffic-2021/traffic-python_and_gitlab/in_2021.svg)
![GitHub views](https://raw.githubusercontent.com/aleksandr-kotlyar/python_and_gitlab/traffic-2021/traffic-python_and_gitlab/views.svg)
![GitHub views per week](https://raw.githubusercontent.com/aleksandr-kotlyar/python_and_gitlab/traffic-2021/traffic-python_and_gitlab/views_per_week.svg)
![GitHub clones](https://raw.githubusercontent.com/aleksandr-kotlyar/python_and_gitlab/traffic-2021/traffic-python_and_gitlab/clones.svg)
![GitHub clones per week](https://raw.githubusercontent.com/aleksandr-kotlyar/python_and_gitlab/traffic-2021/traffic-python_and_gitlab/clones_per_week.svg)

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

