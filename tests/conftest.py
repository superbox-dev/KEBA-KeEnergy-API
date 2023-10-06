import re
from collections.abc import Generator

import pytest
from aioresponses.core import aioresponses

from tests.mock_api import mock_kenergy_api_callback


@pytest.fixture()
def mock_aioresponse() -> Generator[aioresponses, None, None]:
    with aioresponses() as m:
        yield m


@pytest.fixture()
def mock_keenergy_api(mock_aioresponse: aioresponses) -> aioresponses:
    url_pattern: re.Pattern[str] = re.compile(r"^http://mocked-host/(.*)$")
    mock_aioresponse.post(url_pattern, callback=mock_kenergy_api_callback)
    return mock_aioresponse
