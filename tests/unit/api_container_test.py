# -*- coding: utf-8 -*-

import json

from .api_test import (
    BaseAPIClientTest, url_prefix, fake_request, DEFAULT_TIMEOUT_SECONDS,
    fake_inspect_container
)

try:
    from unittest import mock
except ImportError:
    import mock


def fake_inspect_container_tty(self, container):
    return fake_inspect_container(self, container, tty=True)


class CreateContainerTest(BaseAPIClientTest):
    def test_create_container_with_device_requests(self):
        self.client.create_container(
            'busybox', 'true', host_config=self.client.create_host_config(
                device_requests=[
                    {
                        'device_ids': [
                            '0',
                            'GPU-3a23c669-1f69-c64e-cf85-44e9b07e7a2a'
                        ]
                    },
                    {
                        'driver': 'nvidia',
                        'Count': -1,
                        'capabilities': [
                            ['gpu', 'utility']
                        ],
                        'options': {
                            'key': 'value'
                        }
                    }
                ]
            )
        )

        args = fake_request.call_args
        assert args[0][1] == url_prefix + 'containers/create'
        expected_payload = self.base_create_payload()
        expected_payload['HostConfig'] = self.client.create_host_config()
        expected_payload['HostConfig']['DeviceRequests'] = [
            {
                'Driver': '',
                'Count': 0,
                'DeviceIDs': [
                    '0',
                    'GPU-3a23c669-1f69-c64e-cf85-44e9b07e7a2a'
                ],
                'Capabilities': [],
                'Options': {}
            },
            {
                'Driver': 'nvidia',
                'Count': -1,
                'DeviceIDs': [],
                'Capabilities': [
                    ['gpu', 'utility']
                ],
                'Options': {
                    'key': 'value'
                }
            }
        ]
        assert json.loads(args[1]['data']) == expected_payload
        assert args[1]['headers'] == {'Content-Type': 'application/json'}
        assert args[1]['timeout'] == DEFAULT_TIMEOUT_SECONDS
