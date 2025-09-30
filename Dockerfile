ARG BASE_IMAGE=public.ecr.aws/lambda/python:3.13@sha256:d9edaacb31059fc0ac2a98849ef5c271df0a81be36e8d78dfb72a414483f2e0a
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2024-06-24

LABEL Name="senzing/self-signed-certificate" \
  Maintainer="support@senzing.com" \
  Version="1.0.5"

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Run as "root" for system installation.

USER root

# Install packages via PIP.

COPY requirements.txt .
RUN pip3 install --upgrade pip \
  && pip3 install -r requirements.txt \
  && pip3 install awslambdaric \
  && rm requirements.txt

# Copy files from repository.

COPY ./rootfs /
COPY self_signed_certificate.py ./

# Make non-root container.

USER 1001

# Runtime execution.

ENV SENZING_DOCKER_LAUNCHED=true

ENTRYPOINT ["/var/task/self_signed_certificate.py"]
