import asyncio

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import Control
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HotWaterTank
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
                payload=[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.808357"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: float = await client.get_outdoor_temperature()

            assert isinstance(response, float)
            assert response == 10.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_api_with_session(self) -> None:
        """Test api with seassion."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.808357"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            session: ClientSession = ClientSession()
            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host", session=session)
            data: float = await client.get_outdoor_temperature()

            assert not session.closed
            await session.close()

            assert isinstance(data, float)
            assert data == 10.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        (
            "control",
            "position",
            "option_payload",
            "payload",
            "expected_data",
            "expected_response",
        ),
        [
            (
                HeatCircuit.TEMPERATURE,
                1,
                None,
                [
                    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "value": "10.808357"},
                ],
                '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue"}]',
                {
                    "HEAT_CIRCUIT_TEMPERATURE": (10.81,),
                },
            ),
            (
                [HeatCircuit.TEMPERATURE, HeatPump.INFLOW_TEMPERATURE],
                [1, 3],
                None,
                [
                    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "value": "10.808357"},
                    {"name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue", "value": "11.808357"},
                    {"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "value": "24.200001"},
                    {"name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue", "value": "23.200001"},
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatCircuit[2].values.setValue"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[2].TempHeatFlow.values.actValue"}]'
                ),
                {
                    "HEAT_CIRCUIT_TEMPERATURE": (10.81, 11.81),
                    "HEAT_PUMP_INFLOW_TEMPERATURE": (24.2, 23.2),
                },
            ),
            (
                [HeatCircuit.TEMPERATURE, HeatPump.INFLOW_TEMPERATURE],
                None,
                [
                    {"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps", "value": "2"},
                    {"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits", "value": "1"},
                    {"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "value": "1"},
                ],
                [
                    {"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "value": "10.808357"},
                    {"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "value": "24.200001"},
                    {"name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue", "value": "23.200001"},
                ],
                (
                    '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue"}, '
                    '{"name": "APPL.CtrlAppl.sParam.heatpump[1].TempHeatFlow.values.actValue"}]'
                ),
                {
                    "HEAT_CIRCUIT_TEMPERATURE": (10.81,),
                    "HEAT_PUMP_INFLOW_TEMPERATURE": (
                        24.2,
                        23.2,
                    ),
                },
            ),
        ],
    )
    async def test_read_values(
        self,
        control: Control,
        position: int | None | list[int | None],
        option_payload: list[dict[str, str]] | None,
        payload: list[dict[str, str]],
        expected_data: str,
        expected_response: ValueResponse,
    ) -> None:
        """Test read multiple values."""
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
            response: ValueResponse = await client.read_values(request=control, position=position)

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
        ("control", "expected_data"),
        [
            (
                {
                    HotWaterTank.MIN_TEMPERATURE: (10,),
                },
                '[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "10"}]',
            ),
            (
                {
                    HotWaterTank.MIN_TEMPERATURE: (10,),
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
    async def test_write_values(
        self,
        control: dict[Control, tuple[float | int | None, ...]],
        expected_data: str,
    ) -> None:
        """Test write multiple values."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload=[{}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.write_values(request=control)

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
                loop.run_until_complete(client.get_outdoor_temperature())

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
                loop.run_until_complete(client.get_outdoor_temperature())

            assert str(error.value) == "mocked-error"
