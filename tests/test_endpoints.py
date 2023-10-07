import pytest
from aioresponses.core import aioresponses

from keba_keyenergy_api.api import KebaKeEnergyAPI
from keba_keyenergy_api.constants import HeatCircuitOperatingMode
from keba_keyenergy_api.constants import HotWaterTankOperatingMode


class TestHotWaterTank:
    @pytest.mark.asyncio()
    async def test_get_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue",
                        "value": "58.900002",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_temperature()

            assert isinstance(data, float)
            assert data == 58.900002  # noqa: PLR2004
            mock_keenergy_api.assert_called_once()

    @pytest.mark.asyncio()
    async def test_get_operating_mode(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "value": "3"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.hot_water_tank.get_operating_mode()

            assert isinstance(data, int)
            assert data == HotWaterTankOperatingMode.HEAT_UP

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [(HotWaterTankOperatingMode.OFF, 0), (HotWaterTankOperatingMode.HEAT_UP, 3)],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int,
        expected_value: int,
    ) -> None:
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
            )

    @pytest.mark.asyncio()
    async def test_get_min_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "0"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_min_temperature()

            assert isinstance(data, float)
            assert data == 0.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_set_min_temperature(self) -> None:
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
            )

    @pytest.mark.asyncio()
    async def test_get_max_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "value": "47"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.hot_water_tank.get_max_temperature()

            assert isinstance(data, float)
            assert data == 47.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_set_max_temperature(self) -> None:
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
            )


class TestHeatPump:
    @pytest.mark.asyncio()
    async def test_get_status(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState", "value": "0"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int = await client.heat_pump.get_status()

            assert isinstance(data, int)
            assert data == 0

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_circulation_pump(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled", "value": "0.5"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_circulation_pump()

            assert isinstance(data, float)
            assert data == 50.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_inflow_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue",
                        "value": "24.200001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_inflow_temperature()

            assert isinstance(data, float)
            assert data == 24.200001  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_reflux_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue",
                        "value": "23.200001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_reflux_temperature()

            assert isinstance(data, float)
            assert data == 23.200001  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_source_input_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue",
                        "value": "22.700001",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_source_input_temperature()

            assert isinstance(data, float)
            assert data == 22.700001  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_source_output_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue", "value": "24.6"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_source_output_temperature()

            assert isinstance(data, float)
            assert data == 24.6  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_compressor_input_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue",
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
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_compressor_output_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue",
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
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_compressor(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled", "value": "0.3"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_compressor()

            assert isinstance(data, float)
            assert data == 30.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_high_pressure(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[
                    {
                        "name": "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue",
                        "value": "15.018749",
                    },
                ],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_high_pressure()

            assert isinstance(data, float)
            assert data == 15.018749  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_low_pressure(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue", "value": "14.8125"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_pump.get_low_pressure()

            assert isinstance(data, float)
            assert data == 14.8125  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue"}]',
                method="POST",
            )


class TestHeatCircuit:
    @pytest.mark.asyncio()
    async def test_get_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "value": "22"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float = await client.heat_circuit.get_temperature()

            assert isinstance(data, float)
            assert data == 22.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_day_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "value": "23"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_day_temperature()

            assert isinstance(data, float)
            assert data == 23.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_set_day_temperature(self) -> None:
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
            )

    @pytest.mark.asyncio()
    async def test_get_day_temperature_threshold(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value", "value": "16"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_day_temperature_threshold()

            assert isinstance(data, float)
            assert data == 16.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_night_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp", "value": "23"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_night_temperature()

            assert isinstance(data, float)
            assert data == 23.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_set_night_temperature(self) -> None:
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
            )

    @pytest.mark.asyncio()
    async def test_get_night_temperature_threshold(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value", "value": "16"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_night_temperature_threshold()

            assert isinstance(data, float)
            assert data == 16.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_holiday_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp", "value": "14"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_holiday_temperature()

            assert isinstance(data, float)
            assert data == 14.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_get_offset_temperature(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp", "value": "2"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: float | None = await client.heat_circuit.get_offset_temperature()

            assert isinstance(data, float)
            assert data == 2.0  # noqa: PLR2004

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    async def test_set_offset_temperature(self) -> None:
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
            )

    @pytest.mark.asyncio()
    async def test_get_operating_mode(self) -> None:
        with aioresponses() as mock_keenergy_api:
            mock_keenergy_api.post(
                "http://mocked-host/var/readWriteVars",
                payload=[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", "value": "3"}],
                headers={"Content-Type": "application/json;charset=utf-8"},
            )

            client: KebaKeEnergyAPI = KebaKeEnergyAPI(host="mocked-host")
            data: int | None = await client.heat_circuit.get_operating_mode()

            assert isinstance(data, int)
            assert data == HeatCircuitOperatingMode.NIGHT

            mock_keenergy_api.assert_called_once_with(
                url="http://mocked-host/var/readWriteVars",
                data='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode"}]',
                method="POST",
            )

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("operating_mode", "expected_value"),
        [
            (HeatCircuitOperatingMode.OFF, 0),
            (HeatCircuitOperatingMode.AUTO, 1),
            (HeatCircuitOperatingMode.DAY, 2),
            (HeatCircuitOperatingMode.NIGHT, 3),
        ],
    )
    async def test_set_operating_mode(
        self,
        operating_mode: int,
        expected_value: int,
    ) -> None:
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
            )
