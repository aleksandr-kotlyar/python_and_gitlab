# Starting my python here. Here you can find examples of gitlab-ci pytest jobs, pylint-check jobs, storing artifacts in gitlab, parametrization-tests, multithread using inside test, sitemap checking for status codes.

To run tests you should have: 

* python 3.7+

After cloning, you should activate your virtual env and execute this command to install project's dependencies:

`pip3 install -r requirements.txt`


If you want to see Allure Report with attachments, try this in your project console:

`pytest --alluredir=reports --allure-no-capture src\test\test_allure_api.py`

and after tests execution try this and your browser with Allure Report will open:

`allure serve reports`

