ARG BASE_IMAGE=public.ecr.aws/lambda/python:3.8@sha256:26fed6a2af5b0adbf5883af82f0089cebbf04e5bbadf734c6e8c45a7ec755daf
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2024-05-22

LABEL Name="senzing/self-signed-certificate" \
  Maintainer="support@senzing.com" \
  Version="1.0.4"

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
