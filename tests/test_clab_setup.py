"""
Copyright 2022 Inmanta

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

import pytest

LOGGER = logging.getLogger(__name__)

LOGGER.info(os.getcwd())


def test_simple_module(
    pytester: pytest.Pytester,
    pytestconfig: pytest.Config,
) -> None:
    # Patch the config to simulate an ini file
    pytestconfig._inicache["pytester_example_dir"] = os.path.join(
        os.path.dirname(__file__), "../docs/examples/"
    )

    # Run the tests of the module
    pytester.copy_example("nokia-srlinux-interface")
    result = pytester.runpytest_subprocess("tests", "-xvvv")
    result.assert_outcomes(passed=1)
