#### In case of new requirements -> build and push new docker image
docker login registry.gitlab.com

docker build -t registry.gitlab.com/aleksandr-kotlyar/python_and_gitlab .

docker push registry.gitlab.com/aleksandr-kotlyar/python_and_gitlab

#### QA dependency baseline (Python 3.11/3.12)
- pytest==8.3.5
- allure-pytest==2.13.5
- requests==2.32.3
- selenium==4.27.1
- selene==2.0.0rc9
- webdriver-manager==4.0.2
- pytest-voluptuous==1.2.0
- voluptuous==0.15.2
- jsonschema==4.23.0 (replaces `validictory`, which is incompatible with Python 3.12)
