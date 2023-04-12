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
from pytest_inmanta.plugin import Project
from pytest_inmanta_yang.clab.config import HostConfig


def test_basics(project: Project, srlinux_host: HostConfig) -> None:
    project.compile(
        f"""
            import yang
            import nokia_srlinux
            import nokia_srlinux_interface

            device = nokia_srlinux::GnmiDevice(
                name="{srlinux_host.hostname}",
                mgmt_ip="{srlinux_host.ip_address.ip}",
                port=57400,
                yang_credentials=yang::Credentials(
                    username="{srlinux_host.username}",
                    password="{srlinux_host.password}",
                ),
            )

            intf = nokia_srlinux_interface::Interface(
                device=device,
                name="ethernet-1/1",
                mtu=9000,
                address="10.10.0.1/24",
            )
        """,
        no_dedent=False,
    )

    assert project.dryrun_resource("yang::GnmiResource")
    assert project.deploy_resource("yang::GnmiResource")
    assert not project.dryrun_resource("yang::GnmiResource")
