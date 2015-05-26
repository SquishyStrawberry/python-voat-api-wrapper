#!/usr/bin/env python3
"""
All of the exceptions used in the main voat api.
These are really specific in the names.
"""


class VoatException(Exception):
    pass


class VoatThingNotFound(VoatException):
    pass


class VoatNoAuthException(VoatException):
    pass


class VoatExpiredToken(VoatException):
    pass


class VoatBadExpiry(VoatException):
    pass


class VoatInvalidAuth(VoatException):
    pass


class VoatApiLimitException(VoatException):
    pass