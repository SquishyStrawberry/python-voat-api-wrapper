#!/usr/bin/env python3
"""
All of the exceptions used in the main voat api.
"""


class VoatException(Exception):
    pass


class VoatThingNotFound(VoatException):
    pass


class VoatNoAuthException(VoatException):
    pass


class VoatExpiredToken(VoatException):
    pass
