import asyncio

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from keba_keyenergy_api.api import KebaKeEnergyAPI
from keba_keyenergy_api.error import APIError
from keba_keyenergy_api.error import InvalidJsonError


@pytest.mark.asyncio()
async def test_api(mock_keenergy_api: aioresponses) -> None:
    client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
    data: float = await client.get_outdoor_temperature()

    assert isinstance(data, float)
    assert data == 10.808357  # noqa: PLR2004
    mock_keenergy_api.assert_called_once()


@pytest.mark.asyncio()
async def test_api_with_session(mock_keenergy_api: aioresponses) -> None:
    session: ClientSession = ClientSession()
    client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host", session=session)
    data: float = await client.get_outdoor_temperature()

    assert not session.closed
    await session.close()

    assert isinstance(data, float)
    assert data == 10.808357  # noqa: PLR2004
    mock_keenergy_api.assert_called_once()


def test_invalid_json_error() -> None:
    loop = asyncio.get_event_loop()

    with aioresponses() as mocked:
        mocked.post(
            "http://mocked-host/var/readWriteVars",
            body="bad-json",
            headers={"Content-Type": "application/json;charset=utf-8"},
        )
        client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

        with pytest.raises(InvalidJsonError) as error:
            loop.run_until_complete(client.get_outdoor_temperature())

        assert str(error.value) == "bad-json"


def test_api_error() -> None:
    loop = asyncio.get_event_loop()

    with aioresponses() as mocked:
        mocked.post(
            "http://mocked-host/var/readWriteVars",
            body='{"developerMessage": "mocked-error"}',
            headers={"Content-Type": "application/json;charset=utf-8"},
        )
        client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

        with pytest.raises(APIError) as error:
            loop.run_until_complete(client.get_outdoor_temperature())

        assert str(error.value) == "mocked-error"
