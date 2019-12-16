#### In case of new requirements -> build and push new docker image
docker login registry.gitlab.com

docker build -t registry.gitlab.com/aleksandr-kotlyar/python_and_gitlab .

docker push registry.gitlab.com/aleksandr-kotlyar/python_and_gitlab
