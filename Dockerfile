ARG BASE_IMAGE=public.ecr.aws/lambda/python:3.8
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2021-03-09

LABEL Name="senzing/self-signed-certificate" \
      Maintainer="support@senzing.com" \
      Version="1.0.0"

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Install packages via PIP.

RUN pip3 install \
      awslambdaric \
      cffi \
      cfnresponse \
      pyOpenSSL

COPY self_signed_certificate.py   ./

# Runtime execution.

ENTRYPOINT ["/var/task/self_signed_certificate.py"]
