#!/usr/bin/env python3
import requests
import json
import time


class VoatException(Exception):
    pass


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


class Voat(object):
    """
    A Class that handles the voat api, providing access to all its features.
    """
    base_url = "https://fakevout.azurewebsites.net/"

    def __init__(self, api_key):
        self.api_key = api_key
        self.logged_in = False
        self.session = requests.Session()
        # Some headers I know I'll always need.
        self.session.headers.update({
            "Voat-ApiKey": api_key,
            "Content-Type": "application/json"
        })

    def login(self, username, password):
        """
        Logins into a VoatBinder instance.
        Arguments:
            username: Your voat username.
            password: Your voat password.
            api_key: Your api key.
        """
        self.username = username
        self.password = password
        self.auth_token = get_auth(self.username, self.password, self.api_key)
        self.logged_in = True
        self.session.headers.update({
            "Authorization": "{} {}".format(self.auth_token.token_type.capitalize(),
                                            self.auth_token.token)
        })

    def get_subverse(self, subverse):
        url = VoatBinder.base_url + "api/v1/v/{}".format(subverse)
        req = self.session.get(url)
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return req_json["data"]
            else:
                raise VoatException(req_json["error"])

    def submit(self, title, content, subverse, is_url=False):
        """
        Submits a 'thing', the base behind submit_url and submit_text.
        Arguments:
            title: The title of the post.
            content: If is_url == True, then this will be the link to the url.
                     Else, this will be the content of the text post.
            subverse: What subverse to post in.
            is_url: Determines wheter the post is a text post or a 'link' post.
        """
        if not self.logged_in:
            raise VoatException("Need to be logged in to post!")
        url = VoatBinder.base_url + "api/v1/v/{}".format(subverse)
        data = {"title": title}
        # Easier than implementing two methods.
        if is_url:
            data["url"] = content
        else:
            data["content"] = content
        # We need to dumps the data, as else it would get translated to FORM.
        req = self.session.post(url, data=json.dumps(data))
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return req_json["data"]
            else:
                raise VoatException(req_json["error"])
        else:
            raise VoatException(req.status_code)

    # Most useless methods ever.

    def submit_url(self, title, url, subverse):
        """
        Please refer to .submit's docs.
        """
        return self.submit(title, url, subverse, True)

    def submit_text(self, title, content, subverse):
        """
        Please refer to .submit's docs.
        """
        return self.submit(title, content, subverse, False)


def get_auth(username, password, api_key):
    req = requests.post(VoatBinder.base_url + "/api/token", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Voat-ApiKey": api_key,
    }, data={
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
