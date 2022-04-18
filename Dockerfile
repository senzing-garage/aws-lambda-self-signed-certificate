ARG BASE_IMAGE=public.ecr.aws/lambda/python:3.9
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2022-04-19

LABEL Name="senzing/self-signed-certificate" \
      Maintainer="support@senzing.com" \
      Version="1.0.1"

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Run as "root" for system installation.

USER root

# Install packages via PIP.

RUN pip3 install \
      awslambdaric \
      cffi \
      cfnresponse \
      pyOpenSSL

# Copy files from repository.

COPY ./rootfs /
COPY self_signed_certificate.py ./

# Make non-root container.

USER 1001

# Runtime execution.

ENV SENZING_DOCKER_LAUNCHED=true

ENTRYPOINT ["/var/task/self_signed_certificate.py"]
