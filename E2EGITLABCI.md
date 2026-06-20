# GitLab CI/CD and Docker for Python Tests

This guide is a practical GitLab CI/CD cookbook for Python and pytest projects.
It starts with a deliberately simple CI job, shows why that approach becomes
painful, then moves toward Docker images, GitLab Container Registry, schedules,
manual variables, multi-project triggers, and parallel test pipelines.

The target reader is a QA engineer, SDET, or developer who wants to understand
not only what to put into `.gitlab-ci.yml`, but why the pipeline should be built
that way.

## Official documentation map

Keep these GitLab and Docker pages close while working through the examples:

1. [GitLab CI/CD pipelines](https://docs.gitlab.com/ci/pipelines/) explains
   pipelines, jobs, stages, manual runs, and pipeline-level variables.
2. [GitLab Runner](https://docs.gitlab.com/runner/) explains how GitLab Runner
   receives jobs from GitLab and sends results back.
3. [GitLab Runner executors](https://docs.gitlab.com/runner/executors/) and
   [Docker executor](https://docs.gitlab.com/runner/executors/docker/) explain
   where jobs are executed.
4. [Run CI/CD jobs in Docker containers](https://docs.gitlab.com/ci/docker/using_docker_images/)
   explains `image`, `services`, and private registry access.
5. [Build and push container images to GitLab Container Registry](https://docs.gitlab.com/user/packages/container_registry/build_and_push_images/)
   explains how to publish Docker images from CI.
6. [Scheduled pipelines](https://docs.gitlab.com/ci/pipelines/schedules/)
   explains nightly or periodic pipelines.
7. [Rules](https://docs.gitlab.com/ci/jobs/job_rules/) explains how to decide
   when jobs should be created.
8. [Downstream pipelines](https://docs.gitlab.com/ci/pipelines/downstream_pipelines/)
   explains parent-child and multi-project pipelines.
9. [Parallel jobs](https://docs.gitlab.com/ci/jobs/job_control/#parallelize-large-jobs)
   explains `parallel` and `parallel:matrix`.
10. [Docker base images](https://docs.docker.com/build/building/base-images/)
    explains what a base image is and why it matters.

## How GitLab CI/CD works

GitLab CI/CD starts from a file named `.gitlab-ci.yml` in the repository root.
When a pipeline is created, GitLab reads this YAML file and decides which jobs
should exist in the pipeline.

A pipeline can be created by many events:

- push to a branch
- push of a tag
- merge request event
- schedule
- manual run from the GitLab UI
- trigger from another pipeline or project

The pipeline is made of jobs and stages.

Jobs are concrete tasks:

```yaml
test:
  script:
    - pytest
```

Stages group jobs and control execution order:

```yaml
stages:
  - build
  - test
  - report
```

Jobs in the same stage may run in parallel if runners are available. Stages run
in order: all jobs in `build` finish first, then `test`, then `report`.

## What runners and executors are

GitLab itself does not run your test command directly. GitLab creates a job, and
GitLab Runner executes it.

The simplified flow is:

1. You push code or start a pipeline manually.
2. GitLab reads `.gitlab-ci.yml`.
3. GitLab creates pipeline jobs.
4. GitLab Runner asks GitLab for available jobs.
5. Runner receives a job and passes it to an executor.
6. The executor runs the job script.
7. Runner streams logs and sends the final status back to GitLab.

An executor is the environment strategy used by GitLab Runner. Common executors
include:

- Docker
- Shell
- Kubernetes
- Docker Autoscaler
- Instance

## Why Docker executor is a good default

For most common QA automation and application test pipelines, Docker executor is
the best starting point.

It gives you:

- a clean container for each job
- repeatable dependency versions
- the same image locally and in CI
- easy use of service containers such as Postgres, Redis, Selenium, or MySQL
- less host pollution than shell executor
- simpler dependency management through Docker images

Shell executor can be useful for very specific host-level tasks, but it is easy
to accidentally depend on tools installed on one runner machine. Kubernetes and
autoscaling executors are powerful, but they are a bigger operational step. For
everyday test automation, Docker is usually the best balance between isolation,
clarity, and maintenance cost.

## First example: install dependencies in the job

Here is a first simple pytest job:

```yaml
stages:
  - test

test:pytest:
  stage: test
  image: python:3.14
  script:
    - pip install -r requirements.txt
    - pytest
```

This works. It is also a good first learning step because everything is visible:
GitLab pulls `python:3.14`, installs dependencies, and runs `pytest`.

Sometimes your tests need system dependencies too:

```yaml
stages:
  - test

test:pytest:
  stage: test
  image: python:3.14
  script:
    - apt-get update
    - apt-get install -y gcc libpq-dev
    - pip install -r requirements.txt
    - pytest
```

This still works, but now the pipeline is starting to smell.

## Why installing dependencies in CI jobs is bad practice

Installing dependencies inside every test job is usually bad long-term practice.

It makes pipelines:

- slower, because every job repeats the same installation
- less stable, because package indexes can change between runs
- harder to debug, because setup noise hides test output
- more expensive, because runner minutes are spent on environment preparation
- harder to scale, because every new test job repeats the same setup

Use this approach only at the beginning, while learning or prototyping. Once the
dependency set becomes stable, move it into a Docker image.

CI should run the work. Docker should prepare the environment.

## Better practice: create a Docker image

Instead of installing dependencies in every job, build an image once and reuse
it in test jobs.

Example `Dockerfile`:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest"]
```

Now the slow environment preparation happens when the image is built. Test jobs
can start from an already prepared image.

## Docker base images

Every Dockerfile starts with `FROM`. That line defines the base image.

Common choices:

| Base image | Good for | Tradeoff |
|---|---|---|
| `python:3.14` | simple learning, broad compatibility | larger image |
| `python:3.14-slim` | practical Python CI image | may need extra apt packages |
| `python:3.14-alpine` | small images | musl libc can break native Python deps |
| `ubuntu` / `debian` | familiar Linux package ecosystem | larger base |
| `scratch` | static binaries | not practical for normal Python tests |
| distroless/hardened | production runtime hardening | less convenient for debugging |

For Python test automation, `python:<version>-slim` is often the best default.
It is smaller than the full image but still Debian-based, so native dependencies
are less surprising than on Alpine.

## Build and push image to GitLab Container Registry

GitLab provides built-in CI/CD variables for the project registry:

- `CI_REGISTRY`
- `CI_REGISTRY_IMAGE`
- `CI_REGISTRY_USER`
- `CI_REGISTRY_PASSWORD`
- `CI_COMMIT_SHORT_SHA`

Example image build job:

```yaml
stages:
  - build
  - test

build:test-image:
  stage: build
  image: docker:27-cli
  services:
    - docker:27-dind
  variables:
    IMAGE_TAG: "$CI_REGISTRY_IMAGE/test-runner:$CI_COMMIT_SHORT_SHA"
  script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
    - docker build --pull -t "$IMAGE_TAG" .
    - docker push "$IMAGE_TAG"
```

Using commit SHA tags prevents different pipeline runs from overwriting each
other. Avoid building everything directly to `latest`; concurrent pipelines can
race and make results confusing.

For a reusable default branch image, add a separate latest-style tag only on the
default branch:

```yaml
build:test-image:latest:
  stage: build
  image: docker:27-cli
  services:
    - docker:27-dind
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
    - docker build --pull -t "$CI_REGISTRY_IMAGE/test-runner:latest" .
    - docker push "$CI_REGISTRY_IMAGE/test-runner:latest"
```

## Use your own image in CI jobs

After the image is pushed, test jobs can use it:

```yaml
stages:
  - test

test:pytest:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  script:
    - pytest
```

When the image is hosted in the same GitLab instance, GitLab Runner can use
GitLab-provided credentials for registry authentication in many common setups.
For cross-project private image access, check project permissions and job token
access settings.

## Simple Selenium service job

Docker executor can attach service containers to a job. This is useful for
browser tests, databases, caches, and any external dependency your tests need.

```yaml
test:e2e:chrome:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  services:
    - name: selenium/standalone-chrome
      alias: selenium
  variables:
    SELENIUM_REMOTE_URL: "http://selenium:4444/wd/hub"
  script:
    - pytest tests/e2e --browser chrome --remote-url "$SELENIUM_REMOTE_URL"
```

The test code should read the remote URL from an environment variable instead of
hardcoding the service hostname.

## Nightly scheduled tests

Running all tests on every push is attractive at the beginning. It gives fast
feedback while the project is small.

Later, it becomes expensive:

- many pushes are work in progress
- full E2E suites are slow
- browser tests can be flaky because of external systems
- runner time becomes a shared bottleneck
- developers start ignoring pipelines if every push produces too much noise

A better model is:

- small smoke checks on merge requests
- relevant checks on changed areas
- full suites on schedules
- manual full runs when needed

Scheduled job:

```yaml
test:nightly:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
  script:
    - pytest tests
```

Create the schedule in GitLab:

1. Open the project.
2. Go to **Build > Pipeline schedules**.
3. Create a schedule, for example every night.
4. Set the target branch.
5. Add schedule variables if needed.

## Run tests selectively instead of every push

Use `rules` to run tests only when they are valuable.

Example: run smoke tests on merge requests, full tests on schedules or manual
web pipelines:

```yaml
test:smoke:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_PIPELINE_SOURCE == "web"
  script:
    - pytest tests/smoke

test:full:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
    - if: $CI_PIPELINE_SOURCE == "web"
      when: manual
      allow_failure: true
  script:
    - pytest tests
```

Example: run API tests only when API code or API tests changed:

```yaml
test:api:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - changes:
        - src/api/**/*
        - tests/api/**/*
  script:
    - pytest tests/api
```

## Manual runs and CI/CD variables

Manual pipeline variables are useful when a person chooses what to test.

Pipeline-level variables can be prefilled in the GitLab UI:

```yaml
variables:
  TEST_SUITE:
    value: "smoke"
    options:
      - "smoke"
      - "regression"
      - "api"
      - "e2e"
    description: "Select test suite to execute."
  TARGET_ENV:
    value: "staging"
    options:
      - "dev"
      - "staging"
      - "production-like"
    description: "Select target test environment."

test:manual:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "web"
  script:
    - pytest "tests/$TEST_SUITE" --env "$TARGET_ENV"
```

Do not use manual variables for secrets. Use protected or masked CI/CD variables
or an external secrets manager.

## Scheduled tests for different environments

Create separate schedules with different variables:

| Schedule name | Cron | Variables |
|---|---|---|
| Nightly dev smoke | every night | `TARGET_ENV=dev`, `TEST_SUITE=smoke` |
| Nightly staging regression | every night | `TARGET_ENV=staging`, `TEST_SUITE=regression` |
| Weekly production-like E2E | weekly | `TARGET_ENV=production-like`, `TEST_SUITE=e2e` |

Use job names that make pipelines easy to scan:

```yaml
test:dev:smoke:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" && $TARGET_ENV == "dev" && $TEST_SUITE == "smoke"
  script:
    - pytest tests/smoke --env dev

test:staging:regression:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" && $TARGET_ENV == "staging" && $TEST_SUITE == "regression"
  script:
    - pytest tests/regression --env staging

test:production-like:e2e:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" && $TARGET_ENV == "production-like" && $TEST_SUITE == "e2e"
  script:
    - pytest tests/e2e --env production-like
```

Clear names such as `test:staging:regression` make the Jobs list readable.

## Trigger tests from another project pipeline

Sometimes application code and test automation live in different projects. The
application pipeline can trigger the test project pipeline after deployment.

Example trigger job:

```yaml
trigger:e2e-tests:
  stage: test
  trigger:
    project: my-group/e2e-tests
    branch: main
    strategy: mirror
  variables:
    TARGET_ENV: staging
    TEST_SUITE: regression
    APPLICATION_REF: "$CI_COMMIT_SHA"
```

The downstream project receives the variables and runs tests with them.

In the test project:

```yaml
test:from-upstream:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - if: $CI_PIPELINE_SOURCE == "pipeline"
  script:
    - pytest "tests/$TEST_SUITE" --env "$TARGET_ENV"
```

Use downstream pipelines when tests are shared across projects or when the test
suite has its own lifecycle.

## Monorepository example

In a monorepo, different services should not always run all tests.

```yaml
test:api:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - changes:
        - services/api/**/*
        - tests/api/**/*
  script:
    - pytest tests/api

test:web:
  stage: test
  image: node:22
  rules:
    - changes:
        - services/web/**/*
        - tests/web/**/*
  script:
    - npm ci --prefix services/web
    - npm test --prefix services/web

test:billing:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  rules:
    - changes:
        - services/billing/**/*
        - tests/billing/**/*
  script:
    - pytest tests/billing
```

For a large monorepo, consider child pipelines per component:

```yaml
trigger:api-tests:
  stage: test
  rules:
    - changes:
        - services/api/**/*
        - tests/api/**/*
  trigger:
    include: ci/api-tests.yml
    strategy: depend
```

## Parallel job execution

GitLab can split one job into several jobs with `parallel`.

```yaml
test:pytest:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  parallel: 4
  script:
    - pytest tests --splits "$CI_NODE_TOTAL" --group "$CI_NODE_INDEX"
```

Your test framework must know how to split tests. GitLab creates parallel jobs
and provides:

- `CI_NODE_TOTAL`
- `CI_NODE_INDEX`

For different combinations of environment, browser, or suite, use
`parallel:matrix`.

```yaml
test:e2e:
  stage: test
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"
  parallel:
    matrix:
      - TARGET_ENV: [dev, staging]
        BROWSER: [chrome, firefox]
  script:
    - pytest tests/e2e --env "$TARGET_ENV" --browser "$BROWSER"
```

This creates jobs such as:

- `test:e2e: [dev, chrome]`
- `test:e2e: [dev, firefox]`
- `test:e2e: [staging, chrome]`
- `test:e2e: [staging, firefox]`

Parallel jobs still need runner capacity. If you create 20 jobs but have only
two runner slots, only two jobs run at the same time.

## Big daddy pipelines

A big test pipeline should not be one giant job. It should be a set of grouped
suites that can run in parallel where possible and remain easy to read.

Good grouping dimensions:

- environment
- suite
- browser
- service
- shard

Example:

```yaml
stages:
  - smoke
  - regression
  - e2e
  - report

default:
  image: "$CI_REGISTRY_IMAGE/test-runner:latest"

test:smoke:
  stage: smoke
  parallel:
    matrix:
      - TARGET_ENV: [dev, staging]
        SUITE: [api-smoke, ui-smoke]
  script:
    - pytest "tests/$SUITE" --env "$TARGET_ENV"

test:regression:
  stage: regression
  parallel:
    matrix:
      - TARGET_ENV: [staging]
        SUITE: [auth, billing, search, profile]
  script:
    - pytest "tests/regression/$SUITE" --env "$TARGET_ENV"

test:e2e:
  stage: e2e
  parallel:
    matrix:
      - TARGET_ENV: [staging]
        BROWSER: [chrome, firefox]
        SUITE: [checkout, onboarding, account]
  script:
    - pytest "tests/e2e/$SUITE" --env "$TARGET_ENV" --browser "$BROWSER"

report:allure:
  stage: report
  script:
    - echo "Generate report here"
```

This structure gives you:

- readable job names
- parallel execution
- separate visibility for environments and suites
- room to add more suites without rewriting the whole pipeline
- a clean path from small smoke tests to full nightly validation

## Final shape

The mature version of this CI/CD setup looks like this:

1. Dependencies are packaged into a Docker image.
2. The image is pushed to GitLab Container Registry.
3. Test jobs use the custom image.
4. Small checks run on merge requests or selected changes.
5. Full suites run on schedules or manual pipelines.
6. Environment and suite selection is controlled by variables or inputs.
7. Large suites are split with `parallel` or `parallel:matrix`.
8. Multi-project pipelines trigger shared test automation when needed.

That is the main idea: keep jobs focused on testing, keep environments in Docker
images, and keep pipeline structure readable for humans who debug failures.
