"""Retrieve hot water tank data."""
import json
from json import JSONDecodeError

from aiohttp import ClientSession
from aiohttp import ClientTimeout

from keba_keyenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keyenergy_api.error import InvalidJsonError


class BaseEndpoint:
    def __init__(self, payload_type: str, base_url: str, session: ClientSession | None = None) -> None:
        self._payload_type: str = payload_type
        self._base_url: str = base_url
        self._session: ClientSession | None = session

    async def _post(self, payload: str, endpoint: str | None = None) -> list[dict[str, str]]:
        """Run a POST request against the API."""
        session: ClientSession = (
            self._session
            if self._session and not self._session.closed
            else ClientSession(timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT))
        )

        try:
            async with session.post(f"{self._base_url}{endpoint}", data=payload) as resp:
                data: list[dict[str, str]] = await resp.json(content_type="application/json;charset=utf-8")
        except JSONDecodeError as error:
            response_text = await resp.text()
            raise InvalidJsonError(response_text) from error
        finally:
            if not self._session:
                await session.close()

        return data

    def _get_payload(self, position: int | None, key: str, value: str | None = None) -> str:
        payload: dict[str, str] = {
            "name": f"{self._payload_type}[{(position - 1) if position else 0}].{key}",
        }

        if value is not None:
            payload["value"] = value

        return json.dumps([payload])


class HotWaterTank(BaseEndpoint):
    """Class to send and retrieve the hot water tank data."""

    def __init__(self, base_url: str, session: ClientSession | None = None) -> None:
        super().__init__(payload_type="APPL.CtrlAppl.sParam.hotWaterTank", base_url=base_url, session=session)

    async def get_temperature(self, position: int | None = None) -> float:
        """Get current temperature."""
        data: list[dict[str, str]] = await self._post(payload=self._get_payload(position, "topTemp.values.actValue"))
        return float(data[0]["value"])

    async def get_operating_mode(self, position: int | None = None) -> int:
        """Get operating mode."""
        data: list[dict[str, str]] = await self._post(payload=self._get_payload(position, "param.operatingMode"))
        return int(data[0]["value"])

    async def set_operating_mode(self, mode: int, position: int | None = None) -> None:
        """Set operating mode."""
        await self._post(endpoint="?action=set", payload=self._get_payload(position, "param.operatingMode", str(mode)))

    async def get_min_temperature(self, position: int | None = None) -> float:
        """Get minimum temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.reducedSetTempMax.value"),
        )
        return float(data[0]["value"])

    async def get_max_temperature(self, position: int | None = None) -> float:
        """Get maximum temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.normalSetTempMax.value"),
        )
        return float(data[0]["value"])

    async def set_max_temperature(self, temperature: int, position: int | None = None) -> None:
        """Set maximum temperature."""
        await self._post(
            endpoint="?action=set",
            payload=self._get_payload(position, "param.normalSetTempMax.value", str(temperature)),
        )


class HeatPump(BaseEndpoint):
    """Class to send and retrieve the heat pump data."""

    def __init__(self, base_url: str, session: ClientSession | None = None) -> None:
        super().__init__(payload_type="APPL.CtrlAppl.sParam.heatpump", base_url=base_url, session=session)

    async def get_status(self, position: int | None = None) -> int:
        """Get status."""
        data: list[dict[str, str]] = await self._post(payload=self._get_payload(position, "values.heatpumpState"))
        return int(data[0]["value"])

    async def get_circulation_pump(self, position: int | None = None) -> float:
        """Get circulation pump."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "CircPump.values.setValueScaled"),
        )
        return float(data[0]["value"]) * 100

    async def get_inflow_temperature(self, position: int | None = None) -> float:
        """Get inflow temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "TempHeatFlow.values.actValue"),
        )
        return float(data[0]["value"])

    async def get_reflux_temperature(self, position: int | None = None) -> float:
        """Get reflux temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "TempHeatReflux.values.actValue"),
        )
        return float(data[0]["value"])

    async def get_source_input_temperature(self, position: int | None = None) -> float:
        """Get source input temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "TempSourceIn.values.actValue"),
        )
        return float(data[0]["value"])

    async def get_source_output_temperature(self, position: int | None = None) -> float:
        """Get source output temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "TempSourceOut.values.actValue"),
        )
        return float(data[0]["value"])

    async def get_compressor_input_temperature(self, position: int | None = None) -> float:
        """Get compressor input temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "TempCompressorIn.values.actValue"),
        )
        return float(data[0]["value"])

    async def get_compressor_output_temperature(self, position: int | None = None) -> float:
        """Get compressor output temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "TempCompressorOut.values.actValue"),
        )
        return float(data[0]["value"])

    async def get_compressor(self, position: int | None = None) -> float:
        """Get compressor."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "Compressor.values.setValueScaled"),
        )
        return float(data[0]["value"]) * 100

    async def get_high_pressure(self, position: int | None = None) -> float:
        """Get high pressure in bar."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "HighPressure.values.actValue"),
        )
        return float(data[0]["value"])

    async def get_low_pressure(self, position: int | None = None) -> float:
        """Get low pressure in bar."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "LowPressure.values.actValue"),
        )
        return float(data[0]["value"])


class HeatCircuit(BaseEndpoint):
    """Class to send and retrieve the heat pump data."""

    def __init__(self, base_url: str, session: ClientSession | None = None) -> None:
        super().__init__(payload_type="APPL.CtrlAppl.sParam.heatCircuit", base_url=base_url, session=session)

    async def get_temperature(self, position: int | None = None) -> float:
        """Get temperature."""
        data: list[dict[str, str]] = await self._post(payload=self._get_payload(position, "values.setValue"))
        return float(data[0]["value"])

    async def set_temperature(self, temperature: int, position: int | None = None) -> None:
        """Set temperature."""
        await self._post(
            endpoint="?action=set",
            payload=self._get_payload(position, "param.normalSetTemp", str(temperature)),
        )

    async def get_day_temperature(self, position: int | None = None) -> float:
        """Get day temperature."""
        data: list[dict[str, str]] = await self._post(payload=self._get_payload(position, "param.normalSetTemp"))
        return float(data[0]["value"])

    async def get_day_temperature_threshold(self, position: int | None = None) -> float:
        """Get day temperature threshold."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.thresholdDayTemp.value"),
        )
        return float(data[0]["value"])

    async def get_night_temperature(self, position: int | None = None) -> float:
        """Get night temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.reducedSetTemp"),
        )
        return float(data[0]["value"])

    async def set_night_temperature(self, temperature: int, position: int | None = None) -> None:
        """Set night temperature."""
        await self._post(
            endpoint="?action=set",
            payload=self._get_payload(position, "param.reducedSetTemp", str(temperature)),
        )

    async def get_night_temperature_threshold(self, position: int | None = None) -> float:
        """Get night temperature threshold."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.thresholdNightTemp.value"),
        )
        return float(data[0]["value"])

    async def get_holiday_temperature(self, position: int | None = None) -> float:
        """Get holiday temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.holidaySetTemp"),
        )
        return float(data[0]["value"])

    async def get_offset_temperature(self, position: int | None = None) -> float:
        """Get offset temperature."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.offsetRoomTemp"),
        )
        return float(data[0]["value"])

    async def set_offset_temperature(self, temperature: int, position: int | None = None) -> None:
        """Set offset temperature."""
        await self._post(
            endpoint="?action=set",
            payload=self._get_payload(position, "param.offsetRoomTemp", str(temperature)),
        )

    async def get_operating_mode(self, position: int | None = None) -> int:
        """Get operating mode."""
        data: list[dict[str, str]] = await self._post(
            payload=self._get_payload(position, "param.operatingMode"),
        )
        return int(data[0]["value"])

    async def set_operating_mode(self, mode: int, position: int | None = None) -> None:
        """Set operating mode."""
        await self._post(endpoint="?action=set", payload=self._get_payload(position, "param.operatingMode", str(mode)))
