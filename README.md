# Device-requests for Docker Python SDK

[![Build status](
https://github.com/EpicWink/docker-py/workflows/test/badge.svg?branch=docker-device-requests)](
https://github.com/EpicWink/docker-py/actions?query=branch%3Adocker-device-requests+workflow%3Atest)

Device-requests patch for Docker Python SDK.

This package includes [#2471](https://github.com/docker/docker-py/pull/2471), which adds device requests. Once upstream `docker` supports device-requests, this package will become empty.

## Installation

    pip install docker-device-requests

## Usage

```python
import docker
from docker.types import DeviceRequest
client = docker.from_env(version="1.40")
o = client.containers.run(
    "nvidia/cuda:latest",
    "nvidia-smi",
    device_requests=[DeviceRequest(count=-1, capabilities=[["gpu"]])],
)
print(o.decode())
```
