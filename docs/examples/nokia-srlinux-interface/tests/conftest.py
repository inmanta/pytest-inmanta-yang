"""
    Copyright 2023 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

import logging
import os
import shutil
from typing import Sequence

import pytest
from pygnmi.client import gNMIclient
from pytest_inmanta_yang.clab.config import HostConfig

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def clab_topology() -> str:
    return os.path.join(os.path.dirname(__file__), "topology/topology.yml")


@pytest.fixture()
def clab_workdir(clab_workdir: str) -> str:
    """
    Add the container initial config in the working directory.
    """
    config = os.path.join(os.path.dirname(__file__), "topology/config.cli")
    shutil.copy(config, os.path.join(clab_workdir, "config.cli"))

    return clab_workdir


@pytest.fixture()
def srlinux_host(clab_hosts: Sequence[HostConfig]) -> HostConfig:
    """
    Execute a few clab command in the clab working directory to start a lab, and once
    the tests are done, clean it up.
    The router will be preconfigured with the topology/config.cli
    """

    assert len(clab_hosts) == 1, "Our topology file only contains one host"
    host_config = clab_hosts[0]

    # Waiting for the router to be reachable
    client = gNMIclient(
        target=(str(host_config.ip_address.ip), 57400),
        password=host_config.password,
        username=host_config.username,
        insecure=False,
        skip_verify=True,
    )
    for _ in range(1, 5):
        try:
            with client as _:
                client.capabilities()
                break
        except Exception:
            pass
    else:
        raise RuntimeError("Failed to get capabilities from router")

    return host_config
