#!/usr/bin/env python3
import requests
import json
from py_voat.exceptions import *
from py_voat.authentication import get_auth
from py_voat.constants import base_url

class Voat(object):

    """
    A Class that handles the voat api, providing access to all its features.
    """ 

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
        Logins into a Voat instance.
        Arguments:
            username: Your voat username.
            password: Your voat password.
            api_key: Your api key.
        """
        self.username = username
        self.password = password
        self.auth_token = get_auth(self.username, self.password, self.api_key)
        self.logged_in = True
        # I used to just set the session.headers here...
        # ...but if I just set 'em once it wouldn't trigger the time-out.

    def get_subverse(self, subverse):
        url = base_url + "api/v1/v/{}".format(subverse)
        req = self.session.get(url)
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return req_json["data"]
            else:
                raise VoatException(req_json["error"])
        else:
            if req.status_code == 403:
                raise VoatNoAuthException("Need to login to use this feature!")
            elif req.status_code == 404:
                raise VoatThingNotFound("Couldn't find subverse '{}'!".format(subverse))

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
        url = base_url + "api/v1/v/{}".format(subverse)
        data = {"title": title}
        # Easier than implementing two methods.
        if is_url:
            data["url"] = content
        else:
            data["content"] = content
        # We need to dumps the data, as else it would get translated to FORM.

        req = self.session.post(url, data=json.dumps(data), headers=self.auth_token.headers)
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

    def get(self, id, subverse=None):
        if subverse is None:
            url = base_url + "api/v1/{}".format(id)
        else:
            url = base_url + "api/v1/v/{}/{}".format(subverse, id)
        req = self.session.get(url)
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return req_json["data"]
            else:
                raise req_json["error"]
        else:
            if req.status_code == 404:
                raise VoatThingNotFound("Post '{}' could not be found!".format(id))
            else:
                raise VoatException(req.status_code)

    def edit(self, title, content, id, subverse=None, is_url=False):
        if subverse is None:
            url = base_url + "api/v1/{}".format(id)
        else:
            url = base_url + "api/v1/v/{}/{}".format(subverse, id)

        data = {"title": title}
        if is_url:
            data["url"] = content
        else:
            data["content"] = content
        req = self.session.put(url, data=json.dumps(data), headers=self.auth_token.headers)
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return req_json["data"]
            else:
                raise VoatException(req_json["error"])
        else:
            if req.status_code == 404:
                raise VoatThingNotFound("Post '{}' could not be found!".format(id))
            elif req.status_code == 401:
                raise VoatInvalidAuth("Authentication is invalid for post '{}'".format(id))
            else:
                raise VoatException(req.status_code)









