#!/usr/bin/env python3
from py_voat.exceptions import *


def handle_code(code):
    # TODO add more specific messages
    if code == 401:
        raise VoatNoAuthException("Invalid authentication!")
    elif code == 404:
        raise VoatThingNotFound("Could not find thing!")
    elif code == 429:
        raise VoatApiLimitException("Sending too many requests!")
    else:
        raise VoatException(code)


def handle_error(error):
    # TODO implement actual error messages
    raise VoatException(error)
