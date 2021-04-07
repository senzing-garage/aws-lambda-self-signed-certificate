# aws-lambda-docker-self-signed-certificates



## XXX

1. Download
   [AWS Lambda Runtime Interface Emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator)
   and make executable.
   Example:

    ```console
    mkdir -p ~/aws-lambda-rie
    curl -Lo ~/aws-lambda-rie/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie
    chmod +x ~/aws-lambda-rie/aws-lambda-rie
    ```




1. XXXX
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

1. XXXX
   Example:

    ```console
    ```



1. Download
   [AWS Lambda Runtime Interface Emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator)
   and make executable.
   Example:

    ```console
    docker run \
      --interactive \
      --volume ~/aws-lambda-rie:/aws-lambda \
      --publish 9001:8080 \
      --rm \
      --tty \
      --entrypoint /aws-lambda/aws-lambda-rie \
      senzing/self-signed-certificates \
        /var/lang/bin/python -m awslambdaric self-signed-certificates.handler
    ```

1. xXXX
   Example:

    ```console
    curl -v -X POST \
      -d '{}' \
      http://localhost:9001/2015-03-31/functions/function/invocations

    ```


1. https://pypi.org/project/awslambdaric/
