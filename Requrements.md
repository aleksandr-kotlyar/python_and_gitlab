#### In case of new requirements -> build and push new docker image
docker login registry.gitlab.com

docker build -t registry.gitlab.com/aleksandr-kotlyar/python_and_gitlab .

docker push registry.gitlab.com/aleksandr-kotlyar/python_and_gitlab

#### QA dependency baseline (Python 3.14)
- allure-pytest==2.13.5
- assertpy==1.1
- beautifulsoup4==4.12.3
- pytest==9.0.3
- requests==2.33.0
- selene==2.0.0rc9
- selenium==4.27.1
- jsonschema==4.23.0 (replaces `validictory`, which is incompatible with Python 3.14)
- voluptuous==0.15.2
- pytest-voluptuous==1.2.0
- curlify==2.2.1
- webdriver-manager==4.0.2
- mimesis==18.0.0

#### Lint and CI tooling
- anybadge==1.16.0
- black==26.3.1
- pycodestyle==2.14.0
- pylint==3.3.3
- pylint-exit==1.2.0
