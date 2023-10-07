import asyncio

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from keba_keyenergy_api.api import KebaKeEnergyAPI
from keba_keyenergy_api.error import APIError
from keba_keyenergy_api.error import InvalidJsonError


class TestKebaKeEnergyAPI:
    @pytest.mark.asyncio()
    async def test_api(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                body='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.808357"}]',
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.get_outdoor_temperature()

            assert isinstance(data, float)
            assert data == 10.808357  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_api_with_session(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                body='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.808357"}]',
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            session: ClientSession = ClientSession()
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host", session=session)
            data: float = await client.get_outdoor_temperature()

            assert not session.closed
            await session.close()

            assert isinstance(data, float)
            assert data == 10.808357  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue"}]',
                method="POST",
            )

    def test_invalid_json_error(self) -> None:
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

    def test_api_error(self) -> None:
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
