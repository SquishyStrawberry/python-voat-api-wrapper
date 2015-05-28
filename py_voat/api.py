#!/usr/bin/env python3
import json
from py_voat.classes import *
from py_voat.constants import base_url
from py_voat.helpers import handle_code


# noinspection PyAttributeOutsideInit
class Voat(object):
    """
    A Class that handles the voat api, providing access to all its features.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.logged_in = False
        self.last_call = None
        self.session = requests.Session()
        # Some headers I know I'll always need.
        self.session.headers.update({
            "Voat-ApiKey": api_key,
            "Content-Type": "application/json"
        })

    def login(self, username, password):
        """
        Log-ins into a Voat instance.
        Arguments:
            username: Your voat username.
            password: Your voat password.
            api_key: Your api key.
        """
        self.username = username
        self.password = password
        self.auth_token = AuthToken.get_auth(self.username,
                                             self.password,
                                             self.api_key)
        self.logged_in = True

    def get_subverse(self, subverse):
        req = self.make_request(self.session.get, "v", subverse)
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return [Submission.from_dict(i, self) for i in req_json["data"]]
            else:
                raise VoatException(req_json["error"])
        else:
            handle_code(req.status_code)

    def submit_post(self, title, content, subverse, is_url=False):
        """
        Submits a 'thing', the base behind submit_url and submit_text.
        Arguments:
            title: The title of the post.
            content: If is_url == True, then this will be the link to the url.
                     Else, this will be the content of the text post.
            subverse: What subverse to post in.
            is_url: Determines whether the post is a text post or a 'link' post.
        """
        if not self.logged_in:
            raise VoatException("Need to be logged in to post!")
        data = {"title": title}
        # Easier than implementing two methods.
        if is_url:
            data["url"] = content
        else:
            data["content"] = content
        # We need to dumps the data, as else it would get translated to FORM.

        req = self.make_request(self.session.post,
                                "v", subverse,
                                data=json.dumps(data),
                                headers=self.auth_token.headers)
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return req_json["data"]
            else:
                raise VoatException(req_json["error"])
        else:
            handle_code(req.status_code)

    # Most useless methods ever.

    def submit_url(self, title, url, subverse):
        """
        Please refer to the .submit method's docs.
        """
        return self.submit_post(title, url, subverse, True)

    def submit_text(self, title, content, subverse):
        """
        Please refer to the .submit method's docs.
        """
        return self.submit_post(title, content, subverse, False)

    def get_post(self, post_id, subverse=None):
        if subverse is None:
            req = self.make_request(self.session.get, "submissions", str(post_id))
        else:
            req = self.make_request(self.session.get, "v", str(post_id))
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return Submission.from_dict(req_json["data"], self)
            else:
                raise req_json["error"]
        else:
            handle_code(req.status_code)

    def edit_post(self, title, content, post_id, subverse=None, is_url=False):
        if not self.logged_in:
            raise VoatNoAuthException("Need to be authenticated to post something!")
        data = {"title": title}
        if is_url:
            data["url"] = content
        else:
            data["content"] = content
        if subverse is None:
            req = self.make_request(self.session.put,
                                    "submissions", str(post_id),
                                    data=json.dumps(data),
                                    headers=self.auth_token.headers)
        else:
            req = self.make_request(self.session.put,
                                    "v", subverse, str(post_id),
                                    data=json.dumps(data),
                                    headers=self.auth_token.headers)
        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                return req_json["data"]
            else:
                raise VoatException(req_json["error"])
        else:
            handle_code(req.status_code)

    def delete_post(self, post_id, subverse=None):
        if not self.logged_in:
            raise VoatNoAuthException("Need to be logged in to delete post!")
        if subverse is None:
            req = self.make_request(self.session.delete,
                                    "submissions", str(post_id),
                                    data=json.dumps(data),
                                    headers=self.auth_token.headers)
        else:
            req = self.make_request(self.session.delete,
                                    "v", subverse, str(post_id),
                                    data=json.dumps(data),
                                    headers=self.auth_token.headers)

        if req.ok:
            req_json = req.json()
            # There is no req_json["data"] to return.
            if not req_json["success"]:
                raise VoatException(req_json["error"])
        else:
            handle_code(req.status_code)

    def fetch_comments(self, post_id, subverse=None):
        if subverse is None:
            req = self.make_request(self.session.get, "submissions", str(post_id), "comments")
        else:
            req = self.make_request(self.session.get, "v", subverse, str(post_id), "comments")

        if req.ok:
            req_json = req.json()
            if req_json["success"]:
                # TODO make Comment class.
                return req_json["data"]
            else:
                raise VoatException(req_json["error"])
        else:
            handle_code(req.status_code)

    def make_request(self, method, *path, **kwargs):
        if self.last_call and time.time() - self.last_call < 1:
            time.sleep(1 - (time.time() - self.last_call))
        self.last_call = time.time()
        path = base_url + ("/" if not base_url.endswith("/") else "") + "/".join(path)
        return method(path, **kwargs)
