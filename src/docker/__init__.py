# flake8: noqa
from docker.api import APIClient
from docker.client import DockerClient, from_env
from docker.context import Context
from docker.context import ContextAPI
from docker.tls import TLSConfig
from docker.version import version, version_info

__version__ = version
__title__ = 'docker'

import docker_device_requests as _docker_device_requests
from docker import constants as _constants
