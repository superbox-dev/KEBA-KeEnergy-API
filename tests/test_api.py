import asyncio
from typing import Any

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import System
from keba_keenergy_api.endpoints import ValueResponse
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import InvalidJsonError


class TestKebaKeEnergyAPI:
    @pytest.mark.asyncio()
    async def test_api(self) -> None:
        """Test api without session."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Exterior temp.",
                            "lowerLimit": "-100",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "10.808357",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: float = await client.system.get_outdoor_temperature()

            assert isinstance(response, float)
            assert response == 10.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_api_with_session(self) -> None:
        """Test api with seassion."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Exterior temp.",
                            "lowerLimit": "-100",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "10.808357",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            session: ClientSession = ClientSession()
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host", session=session)
            data: float = await client.system.get_outdoor_temperature()

            assert not session.closed
            await session.close()

            assert isinstance(data, float)
            assert data == 10.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        (
            "section",
            "position",
            "option_payload",
            "payload",
            "expected_data",
            "expected_response",
        ),
        [
            (
                [
                    System.HOT_WATER_TANK_NUMBERS,
                    HotWaterTank.TEMPERATURE,
                ],
                1,
                None,
                [
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty heat pumps",
                            "lowerLimit": "0",
                            "upperLimit": "4",
                        },
                        "value": "2",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.",
                            "lowerLimit": "20",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "40.808357",
                    },
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue", "attr": "1"}]'
                ),
                {
                    "system": {
                        "hot_water_tank_numbers": {
                            "attributes": {
                                "lower_limit": "0",
                                "upper_limit": "4",
                            },
                            "value": 2,
                        },
                    },
                    "hot_water_tank": {
                        "temperature": [
                            {
                                "value": 40.81,
                                "attributes": {
                                    "lower_limit": "20",
                                    "upper_limit": "90",
                                },
                            },
                        ],
                    },
                    "heat_pump": {},
                    "heat_circuit": {},
                },
            ),
            (
                [HeatCircuit.TEMPERATURE, HeatPump.INFLOW_TEMPERATURE],
                [1, 3],
                None,
                [
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "10.808357",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "11.808357",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.200001",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "23.200001",
                    },
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue", "attr": "1"}]'
                ),
                {
                    "system": {},
                    "hot_water_tank": {},
                    "heat_circuit": {
                        "temperature": [
                            {
                                "value": 10.81,
                                "attributes": {
                                    "lower_limit": "10",
                                    "upper_limit": "90",
                                },
                            },
                            {
                                "value": 11.81,
                                "attributes": {
                                    "lower_limit": "10",
                                    "upper_limit": "90",
                                },
                            },
                        ],
                    },
                    "heat_pump": {
                        "inflow_temperature": [
                            {
                                "value": 24.2,
                                "attributes": {},
                            },
                            {
                                "value": 23.2,
                                "attributes": {},
                            },
                        ],
                    },
                },
            ),
            (
                [System.OUTDOOR_TEMPERATURE, HeatCircuit.TEMPERATURE, HeatPump.INFLOW_TEMPERATURE],
                None,
                [
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty heat pumps",
                            "lowerLimit": "0",
                            "upperLimit": "4",
                        },
                        "value": "2",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty HC",
                            "lowerLimit": "0",
                            "upperLimit": "8",
                        },
                        "value": "1",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks",
                        "attributes": {
                            "dynLowerLimit": 1,
                            "dynUpperLimit": 1,
                            "formatId": "fmt2p0",
                            "longText": "Qty HW tank",
                            "lowerLimit": "0",
                            "upperLimit": "4",
                        },
                        "value": "1",
                    },
                ],
                [
                    {
                        "name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Exterior temp.",
                            "lowerLimit": "-100",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "17.54",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "10.808357",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.200001",
                    },
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "23.200001",
                    },
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue", "attr": "1"}]'
                ),
                {
                    "system": {
                        "outdoor_temperature": {
                            "value": 17.54,
                            "attributes": {
                                "lower_limit": "-100",
                                "upper_limit": "100",
                            },
                        },
                    },
                    "hot_water_tank": {},
                    "heat_pump": {
                        "inflow_temperature": [
                            {
                                "value": 24.2,
                                "attributes": {},
                            },
                            {
                                "value": 23.2,
                                "attributes": {},
                            },
                        ],
                    },
                    "heat_circuit": {
                        "temperature": [
                            {
                                "value": 10.81,
                                "attributes": {
                                    "lower_limit": "10",
                                    "upper_limit": "90",
                                },
                            },
                        ],
                    },
                },
            ),
        ],
    )
    async def test_read_data(
        self,
        section: Section,
        position: int | None | list[int | None],
        option_payload: list[dict[str, str]] | None,
        payload: list[dict[str, str]],
        expected_data: str,
        expected_response: dict[str, ValueResponse],
    ) -> None:
        """Test read multiple data."""
        with aioresponses() as mock_keenergy_api:
            if option_payload is not None:
                mock_keenergy_api.post(
                    "http://mocked-host/var/readWriteVars",
                    payload=option_payload,
                    headers={"Content-Type": "application/json;charset=utf-8"},
                )

            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=payload,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: dict[str, ValueResponse] = await client.read_data(
                request=section,
                position=position,
            )

            assert isinstance(response, dict)
            assert response == expected_response

            mock_keenergy_api.assert_called_with(
                url="http://mocked-host/var/readWriteVars",
                data=expected_data,
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("section", "expected_data"),
        [
            (
                {
                    HotWaterTank.MIN_TEMPERATURE: (10,),
                },
                '[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "10"}]',
            ),
            (
                {
                    HotWaterTank.MIN_TEMPERATURE: [
                        10,
                    ],
                    HotWaterTank.MAX_TEMPERATURE: (
                        45,
                        44,
                    ),
                },
                (
                    "["
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", '
                    '"value": "10"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", '
                    '"value": "45"}, '
                    '{"name": "APPL.CtrlAppl.sParam.hotWaterTank[1].param.normalSetTempMax.value", '
                    '"value": "44"}'
                    "]"
                ),
            ),
        ],
    )
    async def test_write_data(self, section: dict[Section, list[Any]], expected_data: str) -> None:
        """Test write multiple data."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload=[{}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.write_data(request=section)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data=expected_data,
                method="POST",
                ssl=False,
            )

    def test_invalid_json_error(self) -> None:
        """Test invalid json error."""
        loop = asyncio.get_event_loop()

        with aioresponses() as mocked:
            mocked.post(
                "http://mocked-host/var/readWriteVars",
                body="bad-json",
                headers={"Content-Type": "application/json;charset=utf-8"},
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(InvalidJsonError) as error:
                loop.run_until_complete(client.system.get_outdoor_temperature())

            assert str(error.value) == "bad-json"

    def test_api_error(self) -> None:
        """Test api error."""
        loop = asyncio.get_event_loop()

        with aioresponses() as mocked:
            mocked.post(
                "http://mocked-host/var/readWriteVars",
                payload={"developerMessage": "mocked-error"},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                loop.run_until_complete(client.system.get_outdoor_temperature())

            assert str(error.value) == "mocked-error"
