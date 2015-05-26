#!/usr/bin/env python3
import requests
import time
from py_voat.exceptions import *
from py_voat.constants import base_url


class AuthToken(object):

    """
    Small holder class for Voat's Auth Tokens.
    Built to be able to raise an exception when a token is expired.
    """

    def __init__(self, username, token, token_type, expiry_date):
        if isinstance(expiry_date, str):
            if expiry_date.isdigit():
                expiry_date = int(expiry_date)
        if not isinstance(expiry_date, int):
            raise VoatBadExpiry("Bad expiry date, must be int!")
        self.username = username
        self.expiry_date = expiry_date
        self.gotten_at = time.time()
        self.token_type = token_type
        self.token = token

    @property
    def token(self):
        if time.time() >= self.gotten_at + self.expiry_date:
            raise VoatExpiredToken("This token is expired!")
        else:
            return self._token

    @token.setter
    def token(self, val):
        self._token = val

    @property
    def headers(self):
        return {
                "Authentication": "{} {}".format(self.token_type.capitalize(),
                                                 self.token)
        }

    def __str__(self):
        return self.token


def get_auth(username, password, api_key):
    req = requests.post(base_url + "/api/token",
                        headers={
                            "Voat-ApiKey": api_key,
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        data={
                            "grant_type": "password",
                            "username": username,
                            "password": password
                        })
    if req.ok:
        req_json = req.json()
        return AuthToken(req_json["userName"],
                         req_json["access_token"],
                         req_json["token_type"],
                         req_json["expires_in"])
