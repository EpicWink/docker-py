import datetime
import json
import unittest

import docker
from docker.api import APIClient
import requests
import six

from . import fake_api

try:
    from unittest import mock
except ImportError:
    import mock


DEFAULT_TIMEOUT_SECONDS = docker.constants.DEFAULT_TIMEOUT_SECONDS


def response(status_code=200, content='', headers=None, reason=None, elapsed=0,
             request=None, raw=None):
    res = requests.Response()
    res.status_code = status_code
    if not isinstance(content, six.binary_type):
        content = json.dumps(content).encode('ascii')
    res._content = content
    res.headers = requests.structures.CaseInsensitiveDict(headers or {})
    res.reason = reason
    res.elapsed = datetime.timedelta(elapsed)
    res.request = request
    res.raw = raw
    return res


def fake_resolve_authconfig(authconfig, registry=None, *args, **kwargs):
    return None


def fake_inspect_container(self, container, tty=False):
    return fake_api.get_fake_inspect_container(tty=tty)[1]


def fake_resp(method, url, *args, **kwargs):
    key = None
    if url in fake_api.fake_responses:
        key = url
    elif (url, method) in fake_api.fake_responses:
        key = (url, method)
    if not key:
        raise Exception('{0} {1}'.format(method, url))
    status_code, content = fake_api.fake_responses[key]()
    return response(status_code=status_code, content=content)


fake_request = mock.Mock(side_effect=fake_resp)


def fake_get(self, url, *args, **kwargs):
    return fake_request('GET', url, *args, **kwargs)


def fake_post(self, url, *args, **kwargs):
    return fake_request('POST', url, *args, **kwargs)


def fake_put(self, url, *args, **kwargs):
    return fake_request('PUT', url, *args, **kwargs)


def fake_delete(self, url, *args, **kwargs):
    return fake_request('DELETE', url, *args, **kwargs)


def fake_read_from_socket(self, response, stream, tty=False, demux=False):
    return six.binary_type()


url_base = '{0}/'.format(fake_api.prefix)
url_prefix = '{0}v1.40/'.format(
    url_base,
    docker.constants.DEFAULT_DOCKER_API_VERSION)


class BaseAPIClientTest(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch.multiple(
            'docker.api.client.APIClient',
            get=fake_get,
            post=fake_post,
            put=fake_put,
            delete=fake_delete,
            _read_from_socket=fake_read_from_socket
        )
        self.patcher.start()
        self.client = APIClient()

    def tearDown(self):
        self.client.close()
        self.patcher.stop()

    def base_create_payload(self, img='busybox', cmd=None):
        if not cmd:
            cmd = ['true']
        return {"Tty": False, "Image": img, "Cmd": cmd,
                "AttachStdin": False,
                "AttachStderr": True, "AttachStdout": True,
                "StdinOnce": False,
                "OpenStdin": False, "NetworkDisabled": False,
                }
