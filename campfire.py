#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Campfire
========
A simple campfire api implementation.
"""

from six import b
from json import loads
from base64 import b64encode
from os.path import basename
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import urllib3


def _basic_auth(username, password):
    encoded_str = b64encode(b('{0}:{1}'.format(username, password))).decode('utf-8')
    return 'Basic {0}'.format(encoded_str)


class Campfire(object):
    def __init__(self, account, token, http=None):
        self.account = account
        self.auth = _basic_auth(token, '')
        self.http = http or urllib3.PoolManager()
        self.baseurl = 'https://{0}.campfirenow.com'.format(account)

    def _request(self, method, endpoint, **kwargs):
        url = urljoin(self.baseurl, endpoint)
        headers = {
            'User-Agent': 'Campfire.py (rodasmario2@gmail.com)',
            'Authorization': self.auth,
            'Content/Type': 'application/json',
        }
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        response = self.http.request(method, url=url, headers=headers, **kwargs)
        try:
            return loads(response.data.decode('utf-8'))
        except ValueError:
            return

    ### Account
    def get_account(self):
        return self._request('GET', '/account.json')

    ### Rooms
    def rooms(self):
        return self._request('GET', '/rooms.json')

    def presence(self):
        return self._request('GET', '/presence.json')

    def get_room(self, roomid):
        return self._request('GET', '/room/{0}.json'.format(roomid))

    def update_room(self, roomid, topic):
        endpoint = '/room/{0}.json'.format(roomid)
        return self._request('PUT', endpoint, fields={'topic': topic})

    def join_room(self, roomid):
        endpoint = '/room/{0}/join.json'.format(roomid)
        return self._request('POST', endpoint, encode_multipart=False)

    def leave_room(self, roomid):
        endpoint = '/room/{0}/leave.json'.format(roomid)
        return self._request('POST', endpoint, encode_multipart=False)

    def lock_room(self, roomid):
        endpoint = '/room/{0}/lock.json'.format(roomid)
        return self._request('POST', endpoint, encode_multipart=False)

    def unlock_room(self, roomid):
        endpoint = '/room/{0}/unlock.json'.format(roomid)
        return self._request('POST', endpoint, encode_multipart=False)

    ### Search
    def search(self, term):
        return self._request('GET', '/search', fields={'q': term, 'format': 'json'})

    ### Messages
    def speak(self, roomid, message, msgtype='TextMessage'):
        endpoint = '/room/{0}/speak.json'.format(roomid)
        return self._request('POST', endpoint, fields={'message': message, 'type': msgtype}, encode_multipart=False)

    def recent_messages(self, roomid, limit=None, since_msgid=None):
        endpoint = '/room/{0}/recent.json'.format(roomid)
        fields = {}
        if limit:
            fields['limit'] = limit
        if since_msgid:
            fields['since_message_id'] = since_msgid
        return self._request('GET', endpoint, fields=fields)

    def star_message(self, msgid):
        endpoint = '/messages/{0}/star.json'.format(msgid)
        return self._request('POST', endpoint, encode_multipart=False)

    def unstar_message(self, msgid):
        endpoint = '/messages/{0}/star.json'.format(msgid)
        return self._request('DELETE', endpoint)

    ### Transcripts
    def transcript(self, transid):
        endpoint = '/room/{0}/transcript.json'.format(transid)
        return self._request('GET', endpoint)

    def transcript_date(self, transid, year, month, day):
        endpoint = '/room/{0}/transcript/{1}/{2}/{3}.json'.format(transid, year, month, day)
        return self._request('GET', endpoint)

    ### Users
    def get_user(self, userid):
        endpoint = '/users/{0}.json'.format(userid)
        return self._request('PUT', endpoint)

    def me(self):
        return self._request('GET', '/users/me.json')

    ### Uploads
    def upload(self, roomid, filename):    # TODO
        endpoint = '/room/{0}/uploads.json'.format(roomid)
        with open(filename, 'rb') as f:
            fields = {
                'upload': (basename(f.name), f.read()),
            }
            return self._request('POST', endpoint, fields=fields, encode_multipart=True)

    def get_uploads(self, roomid):
        endpoint = '/room/{0}/uploads.json'.format(roomid)
        return self._request('PUT', endpoint)

    def get_upload(self, roomid, upload_msgid):
        endpoint = '/room/{0}/messages/{1}/upload.json'.format(roomid, upload_msgid)
        return self._request('PUT', endpoint)

    ### Streaming
    def stream(self, roomid):
        headers = {
            'User-Agent': 'Campfire.py (rodasmario2@gmail.com)',
            'Authorization': self.auth,
            'Content/Type': 'application/json',
        }
        self.join_room(roomid)
        endpoint = 'https://streaming.campfirenow.com/room/{0}/live.json'.format(roomid)
        response = self.http.request('GET', endpoint, headers=headers, preload_content=False)
        buf = b''
        for chunk in response.stream(amt=1):
            if chunk == ' ':     # Campfire heartbeat
                pass
            buf += chunk
            data, _, tail = buf.partition(b('\r'))
            if not tail:
                continue
            buf = tail
            yield loads(data.decode('utf-8'))
