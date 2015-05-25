#!/usr/bin/env python3
import requests
from py_voat.exceptions import *


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
            raise VoatException("Bad expiry date, must be int!")
        self.username = username
        self.expiry_date = expiry_date
        self.gotten_at = time.time()
        self.token_type = token_type
        self.token = token

    @property
    def token(self):
        current_time = time.time()
        if current_time >= self.gotten_at + self.expiry_date:
            raise VoatException("Token is expired!")
        else:
            return self._token

    @token.setter
    def token(self, val):
        self._token = val

    # For ease of use.
    def __str__(self):
        return self.token


def get_auth(username, password, api_key):
    req = requests.post(Voat.base_url + "/api/token",
                        headers={
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Voat-ApiKey": api_key
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