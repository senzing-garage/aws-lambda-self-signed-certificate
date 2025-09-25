ARG BASE_IMAGE=public.ecr.aws/lambda/python:3.13@sha256:8c681db5483cc3817257682dd3a4d2026132cac6c9f7f0cd70a1373e98be3ecf
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
