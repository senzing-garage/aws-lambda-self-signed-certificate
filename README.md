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
1. [Demonstrate using Command Line Interface](#demonstrate-using-command-line-interface)
    1. [Prerequisites for CLI](#prerequisites-for-cli)
    1. [Download](#download)
    1. [Run command](#run-command)
1. [Demonstrate using Docker](#demonstrate-using-docker)
    1. [Prerequisites for Docker](#prerequisites-for-docker)
    1. [Run Docker container](#run-docker-container)
1. [Develop](#develop)
    1. [Prerequisites for development](#prerequisites-for-development)
    1. [Clone repository](#clone-repository)
    1. [Build Docker image](#build-docker-image)
    1. [Test Docker image](#test-docker-image)
    1. [Make package for S3](#make-package-for-s3)
1. [Advanced](#advanced)
1. [Errors](#errors)
1. [References](#references)

## Preamble

At [Senzing](http://senzing.com),
we strive to create GitHub documentation in a
"[don't make me think](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/dont-make-me-think.md)" style.
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
        1. [Installation hints](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-python-dependencies.md)

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
          https://raw.githubusercontent.com/Senzing/aws-lambda-self-signed-certificate/main/self_signed_certificate.py
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
    1. [docker](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/docker.md)

### Run Docker container

1. Run Docker container.
   Example:

    ```console
    docker run \
      --interactive \
      --rm \
      --tty \
      senzing/self-signed-certificate
    ```

    Note:  Because this is built to run in an AWS Lambda environment,
    errors will be seen when running outside of that environment.

## Develop

The following instructions are used when modifying and building the Docker image.

### Prerequisites for development

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [git](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/git.md)
    1. [make](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/make.md)
    1. [docker](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/docker.md)

### Clone repository

For more information on environment variables,
see [Environment Variables](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md).

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=senzing
    export GIT_REPOSITORY=aws-lambda-self-signed-certificate
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Using the environment variables values just set, follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/clone-repository.md) to install the Git repository.

### Build Docker image

Since the Docker image is based on `public.ecr.aws/lambda/python:3.9`,
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
      https://github.com/senzing/template-docker.git#main
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

### Test Docker image

1. Download the
   [AWS Lambda Runtime Interface Emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator)
   and make executable.
   Example:

    ```console
    mkdir -p ~/aws-lambda-rie
    curl -Lo ~/aws-lambda-rie/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie
    chmod +x ~/aws-lambda-rie/aws-lambda-rie
    ```

1. Run docker container to start a service.
   Example:

    ```console
    docker run \
      --entrypoint /aws-lambda/aws-lambda-rie \
      --interactive \
      --publish 9001:8080 \
      --rm \
      --tty \
      --volume ~/aws-lambda-rie:/aws-lambda \
      senzing/self-signed-certificate \
        /var/lang/bin/python -m awslambdaric self_signed_certificate.handler
    ```

1. In a separate terminal window, call the lambda.
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

### Make package for S3

Make sure that the `python3 --version` used to run the `pip3 install` command is the same
as the python version seen in the AWS Lambda definition (i.e. the `Runtime:` parameter).
If not the python packages may not be the correct version.

1. :pencil2: Identify version of ZIP file.
   Example:

    ```console
    export SENZING_SELF_SIGNED_CERTIFICATE_VERSION=1.0.2
    ```


1. Prepare directories.
   Example:

    ```console
    sudo rm -rf ${GIT_REPOSITORY_DIR}/python
    mkdir -p ${GIT_REPOSITORY_DIR}/python/lib/python3.8/site-packages
    docker pull public.ecr.aws/sam/build-python3.8
    ```

1. Download dependencies.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo docker run \
        -v "$PWD":/var/task \
        "public.ecr.aws/sam/build-python3.8" \
            /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.8/site-packages/; exit"
    ```

1. Compress dependencies.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/python/lib/python3.8/site-packages
    zip -r ${GIT_REPOSITORY_DIR}/self-signed-certificate-${SENZING_SELF_SIGNED_CERTIFICATE_VERSION}.zip .
    ```

1. Add `self_signed_certificate.py` to compressed file.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    zip -g self-signed-certificate-${SENZING_SELF_SIGNED_CERTIFICATE_VERSION}.zip self_signed_certificate.py
    ```

1. Upload `self-signed-certificate-0.0.0.zip` to AWS S3.

## Advanced

## Errors

1. See [docs/errors.md](docs/errors.md).

## References

1. [PyPi - awslambdaric](https://pypi.org/project/awslambdaric/)
1. [Creating a function with runtime dependencies](https://docs.aws.amazon.com/lambda/latest/dg/python-package-create.html#python-package-create-with-dependency)
