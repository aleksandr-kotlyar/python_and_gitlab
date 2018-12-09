# Starting my python here.

To run tests you should have: 

* python 3.5+
* pipenv

After cloning, you should activate your virtual env and execute this command:

`pipenv install`

to install project's dependencies.

If you want to see Allure Report with attachments, try this in your project console:

`pytest --alluredir=reports --allure-no-capture src\test\allure_api_test.py`

and after tests execution try this:

`allure serve reports`

and your browser with Allure Report will open. 