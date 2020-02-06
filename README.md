# Starting my python here.

To run tests you should have: 

* python 3.7+

After cloning, you should activate your virtual env and execute this command to install project's dependencies:

`pip3 install -r requirements.txt`


If you want to see Allure Report with attachments, try this in your project console:

`pytest --alluredir=reports --allure-no-capture src\test\test_allure_api.py`

and after tests execution try this and your browser with Allure Report will open:

`allure serve reports`

