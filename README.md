# aws-lambda-self-signed-certificate

## Synopsis

An AWS Lambda Python program for generating self-signed certificates.

## Overview

The instructions show how to generate a package that is loaded onto AWS S3 and used by
[https://github.com/Senzing/aws-cloudformation-ecs-poc-simple](https://github.com/Senzing/aws-cloudformation-ecs-poc-simple)
AWS Cloudformation.

### Contents

1. [Preamble](#preamble)
    1. [Legend](#legend)
1. [Related artifacts](#related-artifacts)
1. [Expectations](#expectations)
1. [Demonstrate using Command Line Interface](#demonstrate-using-command-line-interface)
    1. [Prerequisites for CLI](#prerequisites-for-cli)
    1. [Download](#download)
    1. [Environment variables for CLI](#environment-variables-for-cli)
    1. [Run command](#run-command)
1. [Demonstrate using Docker](#demonstrate-using-docker)
    1. [Prerequisites for Docker](#prerequisites-for-docker)
    1. [Docker volumes](#docker-volumes)
    1. [Docker network](#docker-network)
    1. [Docker user](#docker-user)
    1. [Database support](#database-support)
    1. [External database](#external-database)
    1. [Run Docker container](#run-docker-container)
1. [Develop](#develop)
    1. [Prerequisites for development](#prerequisites-for-development)
    1. [Clone repository](#clone-repository)
    1. [Build Docker image](#build-docker-image)
1. [Examples](#examples)
    1. [Examples of CLI](#examples-of-cli)
    1. [Examples of Docker](#examples-of-docker)
1. [Advanced](#advanced)
    1. [Configuration](#configuration)
1. [Errors](#errors)
1. [References](#references)

## Preamble

At [Senzing](http://senzing.com),
we strive to create GitHub documentation in a
"[don't make me think](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/dont-make-me-think.md)" style.
For the most part, instructions are copy and paste.
Whenever thinking is needed, it's marked with a "thinking" icon :thinking:.
Whenever customization is needed, it's marked with a "pencil" icon :pencil2:.
If the instructions are not clear, please let us know by opening a new
[Documentation issue](https://github.com/Senzing/template-python/issues/new?template=documentation_request.md)
describing where we can improve.   Now on with the show...

### Legend

1. :thinking: - A "thinker" icon means that a little extra thinking may be required.
   Perhaps there are some choices to be made.
   Perhaps it's an optional step.
1. :pencil2: - A "pencil" icon means that the instructions may need modification before performing.
1. :warning: - A "warning" icon means that something tricky is happening, so pay attention.

## Related artifacts

1. [https://github.com/Senzing/aws-cloudformation-ecs-poc-simple](https://github.com/Senzing/aws-cloudformation-ecs-poc-simple) AWS Cloudformation

## Demonstrate using Command Line Interface

### Prerequisites for CLI

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. Install Python dependencies:
    1. See [requirements.txt](requirements.txt) for list
        1. [Installation hints](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-python-dependencies.md)

### Download

1. Get a local copy of
   [template-python.py](template-python.py).
   Example:

    1. :pencil2: Specify where to download file.
       Example:

        ```console
        export SENZING_DOWNLOAD_FILE=~/self_signed_certificate.py
        ```

    1. Download file.
       Example:

        ```console
        curl -X GET \
          --output ${SENZING_DOWNLOAD_FILE} \
          https://raw.githubusercontent.com/Senzing/aws-lambda-self-signed-certificate/master/self_signed_certificate.py
        ```

    1. Make file executable.
       Example:

        ```console
        chmod +x ${SENZING_DOWNLOAD_FILE}
        ```

1. :thinking: **Alternative:** The entire git repository can be downloaded by following instructions at
   [Clone repository](#clone-repository)

### Run command

1. Run the command.
   Example:

   ```console
   ${SENZING_DOWNLOAD_FILE}
   ```

## Demonstrate using Docker

### Prerequisites for Docker

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-docker.md)
1. [Install Senzing using Docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-senzing-using-docker.md)
    1. If using Docker with a previous "system install" of Senzing,
       see [how to use Docker with system install](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/use-docker-with-system-install.md).
1. [Configure Senzing database using Docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/configure-senzing-database-using-docker.md)
1. [Configure Senzing using Docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/configure-senzing-using-docker.md)

### Run Docker container

Although the `Docker run` command looks complex,
it accounts for all of the optional variations described above.
Unset `*_PARAMETER` environment variables have no effect on the
`docker run` command and may be removed or remain.

1. Run Docker container.
   Example:

    ```console
    sudo docker run \
      --interactive \
      --rm \
      --tty \
      senzing/template
    ```

1. For more examples of use, see [Examples of Docker](#examples-of-docker).

## Develop

The following instructions are used when modifying and building the Docker image.

### Prerequisites for development

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [git](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-git.md)
    1. [make](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-make.md)
    1. [docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-docker.md)

### Clone repository

For more information on environment variables,
see [Environment Variables](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md).

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=senzing
    export GIT_REPOSITORY=aws-lambda-self-signed-certificate
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Using the environment variables values just set, follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/clone-repository.md) to install the Git repository.

### Make package

Make sure that the `python3 --version` used to run the `pip3 install` command is the same
as the python version seen in the AWS Lambda definition (i.e. the `Runtime:` parameter).
If not the python packages may not be the correct version.

1. Install dependencies.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    pip3 install \
        --target ./package \
        cffi \
        cfnresponse \
        pyOpenSSL
    ```

1. Compress dependencies.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/package
    zip -r ../self-signed-certificate.zip .
    ```

1. Add `self_signed_certificate.py` to compressed file.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    zip -g self-signed-certificate.zip self_signed_certificate.py
    ```

#### Make package references

1. [Creating a function with runtime dependencies](https://docs.aws.amazon.com/lambda/latest/dg/python-package-create.html#python-package-create-with-dependency)

### Build Docker image

Since the Docker image is based on `public.ecr.aws/lambda/python:3.8`,
logging into AWS Elastic Container Registry (ECR) is required.

1. Set AWS environment variables.
   Example:

    ```console
    export AWS_ACCESS_KEY_ID=$(jq --raw-output ".Credentials.AccessKeyId" ~/aws-sts-get-session-token.json)
    export AWS_SECRET_ACCESS_KEY=$(jq --raw-output ".Credentials.SecretAccessKey" ~/aws-sts-get-session-token.json)
    export AWS_SESSION_TOKEN=$(jq --raw-output ".Credentials.SessionToken" ~/aws-sts-get-session-token.json)
    export AWS_DEFAULT_REGION=$(aws configure get default.region)
    ```

1. Login
   Example:

    ```console
    aws ecr-public get-login-password \
      --region us-east-1 \
    | docker login \
      --username AWS \
      --password-stdin public.ecr.aws/senzing
    ```

1. **Option #1:** Using `docker` command and GitHub.

    ```console
    sudo docker build \
      --tag senzing/template \
      https://github.com/senzing/template-docker.git
    ```

1. **Option #2:** Using `docker` command and local repository.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo docker build --tag senzing/template .
    ```

1. **Option #3:** Using `make` command.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo make docker-build
    ```

    Note: `sudo make docker-build-development-cache` can be used to create cached Docker layers.

### Test Docker image

1. Download
   [AWS Lambda Runtime Interface Emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator)
   and make executable.
   Example:

    ```console
    mkdir -p ~/aws-lambda-rie
    curl -Lo ~/aws-lambda-rie/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie
    chmod +x ~/aws-lambda-rie/aws-lambda-rie
    ```

1. Run docker container.
   Example:

    ```console
    docker run \
      --interactive \
      --volume ~/aws-lambda-rie:/aws-lambda \
      --publish 9001:8080 \
      --rm \
      --tty \
      --entrypoint /aws-lambda/aws-lambda-rie \
      senzing/self-signed-certificate \
        /var/lang/bin/python -m awslambdaric self_signed_certificate.handler
    ```

1. Call the lambda.
   Example:

    ```console
    curl -v -X POST \
      http://localhost:9001/2015-03-31/functions/function/invocations \
      --data-binary @- << EOF
        {
          "RequestType": "Create",
          "ResponseURL": "",
          "StackId": "",
          "RequestId": "",
          "LogicalResourceId": ""
        }
    EOF
    ```

## Advanced

## Errors

1. See [docs/errors.md](docs/errors.md).

## References

1. [PyPi - awslambdaric](https://pypi.org/project/awslambdaric/)
