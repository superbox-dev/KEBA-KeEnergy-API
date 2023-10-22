from typing import Any

import pytest
from aioresponses.core import aioresponses

from keba_keenergy_api.api import KebaKeEnergyAPI
from keba_keenergy_api.constants import HeatCircuitOperatingMode
from keba_keenergy_api.constants import HotWaterTankOperatingMode
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.error import APIError


class TestDeviceSection:
    @pytest.mark.asyncio()
    async def test_device_info(self) -> None:
        """Test get device info from hardware."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/deviceControl?action=getDeviceInfo",
                payload=[
                    {
                        "ret": "OK",
                        "revNo": 2,
                        "orderNo": 12345678,
                        "serNo": 12345678,
                        "name": "MOCKED-NAME",
                        "variantNo": 0,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: dict[str, Any] = await client.device.get_device_info()

            assert isinstance(response, dict)
            assert response == {
                "revNo": 2,
                "orderNo": 12345678,
                "serNo": 12345678,
                "name": "MOCKED-NAME",
                "variantNo": 0,
            }

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/deviceControl?action=getDeviceInfo",
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_name(self) -> None:
        """Test get device name from hardware."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/deviceControl?action=getDeviceInfo",
                payload=[
                    {
                        "ret": "OK",
                        "revNo": 2,
                        "orderNo": 12345678,
                        "serNo": 12345678,
                        "name": "MOCKED-NAME",
                        "variantNo": 0,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: str = await client.device.get_name()

            assert isinstance(response, str)
            assert response == "MOCKED-NAME"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/deviceControl?action=getDeviceInfo",
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_serial_number(self) -> None:
        """Test get serial number from hardware."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/deviceControl?action=getDeviceInfo",
                payload=[
                    {
                        "ret": "OK",
                        "revNo": 2,
                        "orderNo": 12345678,
                        "serNo": 12345678,
                        "name": "MOCKED-NAME",
                        "variantNo": 0,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: int = await client.device.get_serial_number()

            assert isinstance(response, int)
            assert response == 12345678  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/deviceControl?action=getDeviceInfo",
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_revision_number(self) -> None:
        """Test get revision number from hardware."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/deviceControl?action=getDeviceInfo",
                payload=[
                    {
                        "ret": "OK",
                        "revNo": 2,
                        "orderNo": 12345678,
                        "serNo": 12345678,
                        "name": "MOCKED-NAME",
                        "variantNo": 0,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.device.get_revision_number()

            assert isinstance(data, int)
            assert data == 2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/deviceControl?action=getDeviceInfo",
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_variant_number(self) -> None:
        """Test get variant number from hardware."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/deviceControl?action=getDeviceInfo",
                payload=[
                    {
                        "ret": "OK",
                        "revNo": 2,
                        "orderNo": 12345678,
                        "serNo": 12345678,
                        "name": "MOCKED-NAME",
                        "variantNo": 0,
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.device.get_variant_number()

            assert isinstance(data, int)
            assert data == 0

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/deviceControl?action=getDeviceInfo",
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_system_info(self) -> None:
        """Test get system information."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/swupdate?action=getSystemInstalled",
                payload=[
                    {
                        "ret": "OK",
                        "name": "KeEnergy.MTec",
                        "version": "2.2.2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: dict[str, Any] = await client.device.get_system_info()

            assert isinstance(data, dict)
            assert data == {
                "name": "KeEnergy.MTec",
                "version": "2.2.2",
            }

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/swupdate?action=getSystemInstalled",
                method="POST",
                ssl=False,
            )


class TestOptionSection:
    @pytest.mark.asyncio()
    async def test_get_positions(self) -> None:
        """Test get positions for heat pumps, heating circuits and hot water tanks."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            response: Position = await client.options.get_positions()

            assert isinstance(response, Position)
            assert response.heat_pump == 2  # noqa: PLR2004
            assert response.heat_circuit == 1
            assert response.hot_water_tank == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data=(
                    '[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits", "attr": "1"}, '
                    '{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}]'
                ),
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_number_of_hot_water_tanks(self) -> None:
        """Test get number of hot water tanks."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                        "value": "2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.options.get_number_of_hot_water_tanks()

            assert isinstance(data, int)
            assert data == 2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHotWaterTanks", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_number_of_heat_pumps(self) -> None:
        """Test get number of heat pumps."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                        "value": "1",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.options.get_number_of_heat_pumps()

            assert isinstance(data, int)
            assert data == 1

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatPumps", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_number_of_heating_circuits(self) -> None:
        """Test get number of heating circuits."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
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
                        "value": "3",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.options.get_number_of_heating_circuits()

            assert isinstance(data, int)
            assert data == 3  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.options.systemNumberOfHeatingCircuits", "attr": "1"}]',
                method="POST",
                ssl=False,
            )


class TestHotWaterTankSection:
    @pytest.mark.asyncio()
    async def test_get_temperature(self) -> None:
        """Test get temperature for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Temp. act.",
                            "lowerLimit": "20",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "58.900002",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_temperature()

            assert isinstance(data, float)
            assert data == 58.9  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 3, "heat_up"), (False, 3, 3)],
    )
    async def test_get_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test get operating mode for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtHotWaterTank",
                            "longText": "Op.mode",
                            "lowerLimit": "0",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.hot_water_tank.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("human_readable", "payload_value"),
        [(True, 10)],
    )
    async def test_get_invalid_human_readable_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
    ) -> None:
        """Test get invalid human readable operating mode for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtHotWaterTank",
                            "longText": "Op.mode",
                            "lowerLimit": "0",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.hot_water_tank.get_operating_mode(human_readable=human_readable)

            assert str(error.value) == (
                "Can't convert value to human readable value! "
                "{'name': 'APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode', "
                "'attributes': {'formatId': 'fmtHotWaterTank', 'longText': 'Op.mode', "
                "'lowerLimit': '0', 'unitId': 'Enum', 'upperLimit': '32767'}, 'value': '10'}"
            )

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [("off", 0), ("OFF", 0), (HotWaterTankOperatingMode.HEAT_UP.value, 3)],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int | str,
        expected_value: int,
    ) -> None:
        """Test set operating mode for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.hot_water_tank.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "value": "%s"}]'
                % expected_value,
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_operating_mode(
        self,
        operating_mode: int | str,
    ) -> None:
        """Test set operating mode for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.hot_water_tank.set_operating_mode(operating_mode)

            assert str(error.value) == "Invalid operating mode!"

            mock_keenergy_api.assert_not_called()

    @pytest.mark.asyncio()
    async def test_get_lower_limit_temperature(self) -> None:
        """Test get lower limit temperature for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "50",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.hot_water_tank.get_lower_limit_temperature()

            assert isinstance(data, int)
            assert data == 0

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_upper_limit_temperature(self) -> None:
        """Test get upper limit temperature for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "50",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.hot_water_tank.get_upper_limit_temperature()

            assert isinstance(data, int)
            assert data == 52  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_min_temperature(self) -> None:
        """Test get minimum temperature for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Sup.temp.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "0",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_min_temperature()

            assert isinstance(data, float)
            assert data == 0.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_set_min_temperature(self) -> None:
        """Test set minimum temperature for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.hot_water_tank.set_min_temperature(10)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "10"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_max_temperature(self) -> None:
        """Test get maximum temperature for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value",
                        "attributes": {
                            "dynUpperLimit": 1,
                            "formatId": "fmtTemp",
                            "longText": "Temp. nom.",
                            "lowerLimit": "0",
                            "unitId": "Temp",
                            "upperLimit": "52",
                        },
                        "value": "47",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_max_temperature()

            assert isinstance(data, float)
            assert data == 47.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_set_max_temperature(self) -> None:
        """Test set maximum temperature for hot water tank."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.hot_water_tank.set_max_temperature(47)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "value": "47"}]',
                method="POST",
                ssl=False,
            )


class TestHeatPumpSection:
    @pytest.mark.asyncio()
    async def test_get_name(self) -> None:
        """Test get name for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].param.name",
                        "attributes": {
                            "longText": "Name",
                        },
                        "value": "WPS26",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.heat_pump.get_name()

            assert isinstance(data, str)
            assert data == "WPS26"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].param.name", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 1, "flow"), (False, 1, 1)],
    )
    async def test_get_status(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: int | str,
    ) -> None:
        """Test get status for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState",
                        "attributes": {
                            "formatId": "fmtHPState",
                            "longText": "State",
                            "lowerLimit": "0",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_pump.get_status(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_circulation_pump(self) -> None:
        """Test get circulation pump for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmt3p0",
                            "longText": "Circulation pump",
                            "lowerLimit": "0.0",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                        },
                        "value": "0.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_circulation_pump()

            assert isinstance(data, float)
            assert data == 0.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_inflow_temperature(self) -> None:
        """Test get inflow temperature for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Inflow temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.200001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_inflow_temperature()

            assert isinstance(data, float)
            assert data == 24.2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_reflux_temperature(self) -> None:
        """Test get reflux temperature for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Reflux temp.",
                            "unitId": "Temp",
                        },
                        "value": "23.200001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_reflux_temperature()

            assert isinstance(data, float)
            assert data == 23.2  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_source_input_temperature(self) -> None:
        """Test get source input temperature for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Source in temp.",
                            "unitId": "Temp",
                        },
                        "value": "22.700001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_source_input_temperature()

            assert isinstance(data, float)
            assert data == 22.7  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_source_output_temperature(self) -> None:
        """Test get source output temperature for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Source out temp.",
                            "unitId": "Temp",
                        },
                        "value": "24.6",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_source_output_temperature()

            assert isinstance(data, float)
            assert data == 24.6  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_compressor_input_temperature(self) -> None:
        """Test get compressor input temperature for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Comp. in temp.",
                            "unitId": "Temp",
                        },
                        "value": "26.4",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor_input_temperature()

            assert isinstance(data, float)
            assert data == 26.4  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_compressor_output_temperature(self) -> None:
        """Test get compressor output temperature for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Comp. out temp.",
                            "unitId": "Temp",
                        },
                        "value": "26.5",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor_output_temperature()

            assert isinstance(data, float)
            assert data == 26.5  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_compressor(self) -> None:
        """Test get compressor for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Compressor",
                            "lowerLimit": "0.0",
                            "unitId": "Pct100",
                            "upperLimit": "1",
                        },
                        "value": "0.3",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor()

            assert isinstance(data, float)
            assert data == 0.3  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_high_pressure(self) -> None:
        """Test get high pressure for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "High pressure",
                            "unitId": "PressBar",
                        },
                        "value": "15.018749",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_high_pressure()

            assert isinstance(data, float)
            assert data == 15.02  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_low_pressure(self) -> None:
        """Test get low pressure for heat pump."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue",
                        "attributes": {
                            "formatId": "fmt3p2",
                            "longText": "Low pressure",
                            "unitId": "PressBar",
                        },
                        "value": "14.8125",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_low_pressure()

            assert isinstance(data, float)
            assert data == 14.81  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )


class TestHeatCircuitSection:
    @pytest.mark.asyncio()
    async def test_get_name(self) -> None:
        """Test get name for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.name",
                        "attributes": {
                            "longText": "Designation",
                        },
                        "value": "FBH",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: str = await client.heat_circuit.get_name()

            assert isinstance(data, str)
            assert data == "FBH"

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.name", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_temperature(self) -> None:
        """Test get temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Nom.",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "90",
                        },
                        "value": "22",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_temperature()

            assert isinstance(data, float)
            assert data == 22.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_day_temperature(self) -> None:
        """Test get day temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Day",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "30",
                        },
                        "value": "23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_day_temperature()

            assert isinstance(data, float)
            assert data == 23.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_set_day_temperature(self) -> None:
        """Test set day temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_day_temperature(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "value": "23"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_day_temperature_threshold(self) -> None:
        """Test get day temperature threshold for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Heating limit Day",
                            "lowerLimit": "-20",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "16",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_day_temperature_threshold()

            assert isinstance(data, float)
            assert data == 16.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_night_temperature(self) -> None:
        """Test get night temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. night",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "30",
                        },
                        "value": "23",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_night_temperature()

            assert isinstance(data, float)
            assert data == 23.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_set_night_temperature(self) -> None:
        """Test set night temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_night_temperature(23)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp", "value": "23"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_night_temperature_threshold(self) -> None:
        """Test get bight temperature threshold for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Heat limit Night",
                            "lowerLimit": "-20",
                            "unitId": "Temp",
                            "upperLimit": "100",
                        },
                        "value": "16",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_night_temperature_threshold()

            assert isinstance(data, float)
            assert data == 16.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_holiday_temperature(self) -> None:
        """Test get holiday temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Vacation",
                            "lowerLimit": "10",
                            "unitId": "Temp",
                            "upperLimit": "30",
                        },
                        "value": "14",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_holiday_temperature()

            assert isinstance(data, float)
            assert data == 14.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_get_offset_temperature(self) -> None:
        """Test get offset temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp",
                        "attributes": {
                            "formatId": "fmtTemp",
                            "longText": "Room temp. Offset",
                            "lowerLimit": "-2.5",
                            "unitId": "TempRel",
                            "upperLimit": "2.5",
                        },
                        "value": "2",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_offset_temperature()

            assert isinstance(data, float)
            assert data == 2.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    async def test_set_offset_temperature(self) -> None:
        """Test set offset temperature for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_offset_temperature(2)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp", "value": "2"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("human_readable", "payload_value", "expected_value"),
        [(True, 3, "night"), (False, 3, 3)],
    )
    async def test_get_operating_mode(
        self,
        human_readable: bool,  # noqa: FBT001
        payload_value: int,
        expected_value: str,
    ) -> None:
        """Test get operating mode for heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode",
                        "attributes": {
                            "formatId": "fmtHcMode",
                            "longText": "Operating mode",
                            "lowerLimit": "0",
                            "unitId": "Enum",
                            "upperLimit": "32767",
                        },
                        "value": f"{payload_value}",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | str = await client.heat_circuit.get_operating_mode(human_readable=human_readable)

            assert isinstance(data, (int | str))
            assert data == expected_value

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", "attr": "1"}]',
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [
            ("OFF", 0),
            ("AUTO", 1),
            (HeatCircuitOperatingMode.DAY.value, 2),
            (HeatCircuitOperatingMode.NIGHT.value, 3),
        ],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int | str,
        expected_value: int,
    ) -> None:
        """Test set operating mode heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            await client.heat_circuit.set_operating_mode(operating_mode)

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars?action=set",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", "value": "%s"}]'
                % expected_value,
                method="POST",
                ssl=False,
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        "operating_mode",
        ["INVALID"],
    )
    async def test_set_invalid_operating_mode(
        self,
        operating_mode: int,
    ) -> None:
        """Test set operating mode heat circuit."""
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars?action=set",
                payload={},
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")

            with pytest.raises(APIError) as error:
                await client.heat_circuit.set_operating_mode(operating_mode)

            assert str(error.value) == "Invalid operating mode!"

            mock_keenergy_api.assert_not_called()
