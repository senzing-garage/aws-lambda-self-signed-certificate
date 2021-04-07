#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# self-signed-certificates.py Loader for creating self-signed certificates.
# -----------------------------------------------------------------------------

import base64
import json
import logging
import os
import random
import sys
import time
import traceback

from OpenSSL import crypto

__all__ = []
__version__ = "0.1.0"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2021-04-06'
__updated__ = '2021-04-06'

SENZING_PRODUCT_ID = "5019"  # See https://github.com/Senzing/knowledge-base/blob/master/lists/senzing-product-ids.md

NINE_YEARS_IN_SECONDS = 9 * 365 * 24 * 60 * 60
TEN_YEARS_IN_SECONDS = 10 * 365 * 24 * 60 * 60

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

# Configure logging. See https://docs.python.org/2/library/logging.html#levels

log_level_map = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "fatal": logging.FATAL,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

log_format = '%(asctime)s %(message)s'
log_level_parameter = os.getenv("SENZING_LOG_LEVEL", "info").lower()
log_level = log_level_map.get(log_level_parameter, logging.INFO)
logging.basicConfig(format=log_format, level=log_level)

# -----------------------------------------------------------------------------
# Message handling
# -----------------------------------------------------------------------------

# 1xx Informational (i.e. logging.info())
# 3xx Warning (i.e. logging.warning())
# 5xx User configuration issues (either logging.warning() or logging.err() for Client errors)
# 7xx Internal error (i.e. logging.error for Server errors)
# 9xx Debugging (i.e. logging.debug())

MESSAGE_INFO = 100
MESSAGE_WARN = 300
MESSAGE_ERROR = 700
MESSAGE_DEBUG = 900

message_dictionary = {
    "100": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}I",
    "101": "Event: {0}",
    "102": "Context: {0}",
    "300": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}W",
    "700": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "900": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}D",
    "998": "Debugging enabled.",
    "999": "{0}",
}


def message(index, *args):
    index_string = str(index)
    template = message_dictionary.get(index_string, "No message for index {0}.".format(index_string))
    return template.format(*args)


def message_generic(generic_index, index, *args):
    index_string = str(index)
    return "{0} {1}".format(message(generic_index, index), message(index, *args))


def message_info(index, *args):
    return message_generic(MESSAGE_INFO, index, *args)


def message_warning(index, *args):
    return message_generic(MESSAGE_WARN, index, *args)


def message_error(index, *args):
    return message_generic(MESSAGE_ERROR, index, *args)


def message_debug(index, *args):
    return message_generic(MESSAGE_DEBUG, index, *args)


def get_exception():
    ''' Get details about an exception. '''
    exception_type, exception_object, traceback = sys.exc_info()
    frame = traceback.tb_frame
    line_number = traceback.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_number, frame.f_globals)
    return {
        "filename": filename,
        "line_number": line_number,
        "line": line.strip(),
        "exception": exception_object,
        "type": exception_type,
        "traceback": traceback,
    }


def logging_info(message):
    print(message)


def logging_error(message):
    print(message)


def logging_warning(message):
    print(message)


def logging_debug(message):
    print(message)

# -----------------------------------------------------------------------------
# Lambda handler
# -----------------------------------------------------------------------------


def get_new_key():

    result = crypto.PKey()
    result.generate_key(crypto.TYPE_RSA, 2048)
    return result


def get_certificate_authority_certificate(public_key):

    # Create certificate.

    result = crypto.X509()
    result.set_version(2)
    result.set_serial_number(random.randrange(100000))

    # Set subject.

    subject = result.get_subject()
    subject.C = "US"
    subject.ST = "California"
    subject.L = "San Francisco"
    subject.O = "MyOrganization"
    subject.OU = "MyOrganizationalUnit"
    subject.CN = "My own Root CA"

    # Add extensions.

    result.add_extensions([
        crypto.X509Extension(
            b"subjectKeyIdentifier",
            False,
            b"hash",
            subject=result),
    ])
    result.add_extensions([
        crypto.X509Extension(
            b"authorityKeyIdentifier",
            False,
            b"keyid:always",
            issuer=result),
    ])
    result.add_extensions([
        crypto.X509Extension(
            b"basicConstraints",
            False,
            b"CA:TRUE"),
        crypto.X509Extension(
            b"keyUsage",
            False,
            b"keyCertSign, cRLSign"),
    ])

    # Set expiry.

    result.gmtime_adj_notBefore(0)
    result.gmtime_adj_notAfter(TEN_YEARS_IN_SECONDS)

    # Sign and seal.

    result.set_pubkey(public_key)
    result.set_issuer(subject)
    result.sign(public_key, 'sha256')

    return result


def get_certificate(public_key, ca_key, certificate_authority_certificate):

    # Crete certificate.

    result = crypto.X509()
    result.set_version(2)
    result.set_serial_number(random.randrange(100000))

    # Set subject.

    subject = result.get_subject()
    subject.C = "US"
    subject.ST = "California"
    subject.L = "San Francisco"
    subject.O = "MyOrganization"
    subject.OU = "MyOrganizationalUnit"
    subject.CN = "example.com"

    # Add extensions.

    result.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=result),
    ])
    result.add_extensions([
        crypto.X509Extension(
            b"authorityKeyIdentifier",
            False,
            b"keyid:always",
            issuer=certificate_authority_certificate),
        crypto.X509Extension(
            b"extendedKeyUsage",
            False,
            b"serverAuth"),
        crypto.X509Extension(
            b"keyUsage",
            False,
            b"digitalSignature"),
    ])
    result.add_extensions([
        crypto.X509Extension(b'subjectAltName', False,
            ','.join([
                'DNS:*.example.com'
    ]).encode())])

    # Set expiry.

    result.gmtime_adj_notBefore(0)
    result.gmtime_adj_notAfter(NINE_YEARS_IN_SECONDS)

    # Sign and seal.

    result.set_pubkey(public_key)
    result.set_issuer(certificate_authority_certificate.get_subject())
    result.sign(ca_key, 'sha256')

    return result

# -----------------------------------------------------------------------------
# Lambda handler
# -----------------------------------------------------------------------------


def handler(event, context):

    result = {}

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        logger.info("Event: {0}".format(json.dumps(event)))
        if event.get('RequestType') in ['Create', 'Update']:
            properties = event.get('ResourceProperties', {})
            describe_mount_targets_parameters = properties.get('DescribeMountTargetsParameters', {})

            certificate_authority_certificate_key = get_new_key()
            certificate_authority_certificate = get_certificate_authority_certificate(certificate_authority_certificate_key)
            certificate_key = get_new_key()
            certificate = get_certificate(certificate_key, certificate_authority_certificate_key, certificate_authority_certificate)

            result['certificate'] = base64.b64encode(crypto.dump_certificate(crypto.FILETYPE_PEM, certificate)).decode('utf-8')
            result['privateKey'] = base64.b64encode(crypto.dump_privatekey(crypto.FILETYPE_PEM, certificate_key)).decode('utf-8')

    except Exception as e:
        logger.error(e)
        traceback.print_exc()
    finally:
        pass

    return result

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == "__main__":

    logging.debug(message_debug(998))

    event = {
        "RequestType": "Create"
    }
    context = {}

    response = handler(event, context)
    print(json.dumps(response))
