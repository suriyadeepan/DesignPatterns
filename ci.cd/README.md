# Continuous Integration / Continuous Deployment

How to setup a github workflow that builds a docker image, pushes it to dockerhub, pulls the image in an ec2 instance using remote ssh commands and runs it as a container.

See this [repository](https://github.com/suriyadeepan/deploy-docker_image-to-ec2) for a working workflow script.

`cicd.workflow.yml` is a copy of the workflow file from that repo.

## Boilerplate

Name your workflow

```yml
name: ci/cd
```

Set up trigger

```yml
on:
  push:
    branches: [main]
```

Set up platform to run workflow on

```yml
runs-on: ubuntu-latest
```

## Action Steps

```yml
steps:
    ...
```

Checkout code

```yml
- name: Checkout code
    uses: actions/checkout@v2
```

Login to docker. We need to find an alternative way to login, soon.

```yml
- name: Docker login
    env:
        DOCKER_USER: ${{secrets.DOCKER_USER}}
        DOCKER_PASSWORD: ${{secrets.DOCKER_PASSWORD}}
    run:
        docker login -u $DOCKER_USER -p $DOCKER_PASSWORD
```

Build and push docker image to docker hub.

```yml
- name: Docker push
    env:
        REPO: deploy-example
    run: | # multiline script
        # build docker image from local Dockerfile instructions
        docker build -t $REPO
        # tag image with <username>/<repo_name>
        docker tag $REPO:latest ${{secrets.DOCKER_USER}}/$REPO:latest
        # push image to docker hub
        docker push ${{secrets.DOCKER_USER}}/$REPO
```

Set up everything necessary to use EC2 instance
```yml
- name: Docker pull & Run from hub
    env:
        # docker username/password (not necessary right now)
        # .. because we are not logging in
        DOCKER_USER: ${{secrets.DOCKER_USER}}
        DOCKER_PASSWORD: ${{secrets.DOCKER_PASSWORD}}
        # repo name
        REPO: deploy-example
    uses: appleboy/ssh-action@master
    with:
        # ec2 instance public dns name
        host: ${{secrets.EC2_HOST}}
        # ec2 user name
        username: ec2-user
        # *.pem file for accessing ec2 instance
        key: ${{secrets.EC2_PRIVATE_KEY}}
        # ssh port
        port: 22
        # set up environmental variables to be used in script below
        envs:
            DOCKER_USER, REPO
        script: |
            ...
```

Script to execute in ec2 instance

```yml
    script: |
        # right now we aren't logging in coz we are using public image
        # docker login -u="${{secrets.DOCKER_USER}}" -p="${{secrets.DOCKER_PASSWORD}}"
        # pull <username>/<repo_name> from dockerhub
        docker pull $DOCKER_USER/$REPO
        # stop all running containers
        docker stop $(docker ps -a -q)
        # remove containers
        docker rm $(docker ps -a -q)
        # run the pulled image in detached mode; expose port 5000 to port 80
        docker run -d -p 80:5000 $DOCKER_USER/$REPO
```


## Resources

- Minho Jang's [CI/CD Hands-On : Github Actions+Docker Hub+AWS EC2](https://medium.com/ryanjang-devnotes/ci-cd-hands-on-github-actions-docker-hub-aws-ec2-ba09f80297e1)
- Github Actions for executing remote ssh commands [appleboy/ssh-action](https://github.com/appleboy/ssh-action)