## UI testing in gitlab CI
Proud to introduce my ci-solution for selenium UI web testing

Instruments:
- gitlab-ci
- pytest

Images:
- python:3.7.6-alpine (with already installed project dependencies)
- selenium/standalone-chrome
- selenium/standalone-firefox

First: decide what do you want from job?

I want the job that executes e2e tests in chrome browser at remote driver.

Let's see. 
- What will be the name of the job?
- How to execute browser from the job?
- How to customize this job for remote driver?
- How to customize this job for chrome browser?

The name will be e2e:remote:chrome
```yaml
e2e:remote:chrome:
```
What next? Customizing? No. We need the parent job first.
```yaml
.job_template:
```
What should it do? Execute tests ofcourse!
```yaml
.job_template:
  script:
    - pytest
``` 
What tests? Okay, all the tests. Will not modify it yet.

What next? Each job should have a stage or it can't be executed. Need to define stages list.
```yaml
stages:
  - test1
  - test2
  - test3
```
Too much. Let's left only one for a while.
```yaml
stages:
  - test

.job_template:
  script:
    - pytest

e2e:remote:chrome:
```
Forgot something? Yes, each job should have a stage.
```yaml
stages:
  - test

.job_template:
  stage: test
  script:
    - pytest

e2e:remote:chrome:
  stage: test
```
Okay. But do you see what's wrong? Right! e2e job doesn't have a script, but it should.
```yaml
e2e:remote:chrome:
  stage: test
  script:
    - pytest
```
Wait, but now e2e job duplicates .job_template? Right. Let's fix it by inheritance. Finally .job_template just a template, so let's use it by it's purpose.
```yaml
.job_templage:
  stage: test
  script:
    - pytest

e2e:remote:chrome:
  extends: .job_template
```
Yes. That's all. No need to write stage or script in e2e job, they come here from .job_template
Template job has a dot before name. Template jobs never will be executed if they are not extended by jobs with normal names (without dot at first char).

What's next? We want to execute tests in docker, so we need an image to define in our yaml.
```yaml
image: python:3.7.6-alpine
```
Okay. Remember something? Project dependencies! Python and chrome/driver/selenium, etc.

Install python dependencies first. pip? pipenv? choose you destiny. I choose pip.
```yaml
.job_template:
  before_script:
    - pip3 install -r requirements.txt
```
Requirements should already have selenium and pytest at least.

What next? Chromebrowser. How to install it? Make custom docker image? Docker compose? Docker in docker? No. Gitlab services!
```yaml
e2e:remote:chrome:
  extends: .job_template
  services: 
    - selenium/standalone-chrome
```
What it gives? The second container, which is connected to the job and container with tests.
Let's compile all we have now
```yaml
image: python:3.7.6-alpine
stages:
  - test

.job_template:
  before_script:
    - pip3 install -r requirements.txt
  script:
    - pytest

e2e:remote:chrome:
  extends: .job_template
  services: 
    - selenium/standalone-chrome
```
Let's check our list of questions.

- What will be the name of the job? (done)
- How to execute browser from the job? (donot)
- How to customize this job for remote driver? (donot)
- How to customize this job for chrome browser? (donot)

How to execute REMOTE browser from the job? It's not clearly about gitlab-ci.yml, but important.
First of all you need to know the host. Just believe me:
`http://selenium__standalone-chrome:4444/wd/hub`

in conftest.py or other fixture file you should define driver. TLDR:
```python
#conftest.py
from selenium import webdriver

def browser():
    driver = webdriver.Remote(
        commandline_executor='http://selenium__standalone-chrome:4444/wd/hub')
    return driver
```
That should be enough at this moment. Let's draft simple test.
```python
#first_test.py
from conftest import browser

def test_webdriver_opens_page():
    browser.open_url('https://google.com')
    query_block = browser.find_element_by_name('q')
    assert query_block.is_displayed()
```
Return to ci. Now if you commit and push your files to gitlab, the e2e:remote:chrome job will start.








Full script will look like
```yaml
variables:
  REMOTE: 'True'

.job_template:
  stage: test
  script:
    - pytest --remote=${REMOTE} --browser=$BROWSER
  tags:
    - gitlab-org

.e2e:remote:
  image: registry.gitlab.com/aleksandr-kotlyar/python_and_gitlab:latest
  extends: .job_template
  only: 
    $REMOTE == 'True' || $REMOTE == 'true'

e2e:remote:chrome:
  extends: .e2e:remote
  services:
    - name: selenium/standalone-chrome
  only:
    variables:
      - $BROWSER == 'chrome'

e2e:remote:firefox:
  extends: .e2e:remote
  services:
    - name: selenium/standalone-firefox
  only:
    variables:
      - $BROWSER == 'firefox'
```