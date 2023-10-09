"""Retrieve hot water tank data."""
import importlib
import json
import re
from json import JSONDecodeError
from re import Pattern
from typing import Any
from typing import TYPE_CHECKING

from aiohttp import ClientSession
from aiohttp import ClientTimeout

from keba_keenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keenergy_api.constants import Control
from keba_keenergy_api.constants import Endpoint
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import Outdoor
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import InvalidJsonError

if TYPE_CHECKING:
    from types import ModuleType


class BaseSection:
    KEY_PATTERN: Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")

    def __init__(
        self,
        base_url: str,
        *,
        ssl: bool,
        session: ClientSession | None = None,
    ) -> None:
        self._base_url: str = base_url
        self._ssl: bool = ssl
        self._session: ClientSession | None = session

    async def _post(self, payload: str | None = None, endpoint: str | None = None) -> list[dict[str, str]]:
        """Run a POST request against the API."""
        session: ClientSession = (
            self._session
            if self._session and not self._session.closed
            else ClientSession(timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT))
        )

        try:
            async with session.post(
                f"{self._base_url}{endpoint if endpoint else ''}",
                ssl=self._ssl,
                data=payload,
            ) as resp:
                data: list[dict[str, Any]] = await resp.json(
                    content_type="application/json;charset=utf-8",
                )
        except JSONDecodeError as error:
            response_text = await resp.text()
            raise InvalidJsonError(response_text) from error
        finally:
            if not self._session:
                await session.close()

        if isinstance(data, dict) and "developerMessage" in data:
            raise APIError(data["developerMessage"])

        if isinstance(data, dict):
            data = [data]

        return data

    def _get_real_key(self, key: Control) -> str:
        class_name: str = key.__class__.__name__
        return f"{self.KEY_PATTERN.sub('_', class_name).upper()}_{key.name}"

    def _get_key_prefix(self, key: Control) -> str:
        module: ModuleType = importlib.import_module("keba_keenergy_api.constants")
        class_name: str = key.__class__.__name__
        prefix: str = getattr(module, f"{self.KEY_PATTERN.sub('_', class_name).upper()}_PREFIX", "")
        return prefix

    @staticmethod
    def _get_position(position: int | None) -> str:
        _position: str = "" if position is None else f"[{(position - 1)}]"
        return _position

    async def _read_values(
        self,
        request: Control | list[Control],
        position: int | None | list[int | None] = 1,
    ) -> dict[str, dict[str, float | int]]:
        payload: list[dict[str, str]] = []

        if isinstance(request, Outdoor | HotWaterTank | HeatPump | HeatCircuit):
            request = [request]

        if isinstance(position, int) or position is None:
            position = [position]

        payload += [
            {"name": f"{self._get_key_prefix(k)}{self._get_position(p)}.{k.value.value}"}
            for p in position
            for k in request
        ]
        _response: list[dict[str, Any]] = await self._post(
            payload=json.dumps(payload),
            endpoint=Endpoint.READ_VALUES,
        )

        response: dict[str, dict[str, float | int]] = {}
        response_item: dict[str, Any] = {}

        for p in position:
            for k in request:
                value: float | int = k.value.data_type(_response[0]["value"])
                response_item[self._get_real_key(k)] = round(value, 2) if isinstance(value, float) else value
                del _response[0]

            response[str(1 if p is None else p)] = response_item

        return response

    async def _write_values(
        self,
        request: dict[Control, Any],
        position: int | None | list[int | None] = 1,
    ) -> None:
        payload: list[dict[str, str]] = []

        if isinstance(position, int) or position is None:
            position = [position]

        payload += [
            {"name": f"{self._get_key_prefix(k)}{self._get_position(p)}.{k.value.value}", "value": str(v)}
            for p in position
            for k, v in request.items()
            if not k.value.read_only
        ]

        _response: list[dict[str, Any]] = await self._post(
            payload=json.dumps(payload),
            endpoint=Endpoint.WRITE_VALUES,
        )


class DeviceSection(BaseSection):
    """Class to retrieve the device data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_name(self) -> str:
        """Get name."""
        response: list[dict[str, Any]] = await self._post(endpoint=Endpoint.DEVICE_INFO)
        return str(response[0]["name"])

    async def get_serial_number(self) -> int:
        """Get serial_number."""
        response: list[dict[str, Any]] = await self._post(endpoint=Endpoint.DEVICE_INFO)
        return int(response[0]["serNo"])

    async def get_revision_number(self) -> int:
        """Get revision name."""
        response: list[dict[str, Any]] = await self._post(endpoint=Endpoint.DEVICE_INFO)
        return int(response[0]["revNo"])

    async def get_variant_number(self) -> int:
        """Get variant name."""
        response: list[dict[str, Any]] = await self._post(endpoint=Endpoint.DEVICE_INFO)
        return int(response[0]["variantNo"])


class HotWaterTankSection(BaseSection):
    """Class to send and retrieve the hot water tank data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_temperature(self, position: int | None = 1) -> float:
        """Get current temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HotWaterTank.TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HotWaterTank.TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_operating_mode(self, position: int | None = 1) -> int:
        """Get operating mode."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HotWaterTank.OPERATING_MODE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HotWaterTank.OPERATING_MODE)
        value: int = int(response[_position][_key])
        return value

    async def set_operating_mode(self, mode: int, position: int | None = 1) -> None:
        """Set operating mode."""
        await self._write_values(request={HotWaterTank.OPERATING_MODE: str(mode)}, position=position)

    async def get_min_temperature(self, position: int | None = 1) -> float:
        """Get minimum temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HotWaterTank.MIN_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HotWaterTank.MIN_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def set_min_temperature(self, temperature: int, position: int | None = 1) -> None:
        """Set minimum temperature."""
        await self._write_values(request={HotWaterTank.MIN_TEMPERATURE: str(temperature)}, position=position)

    async def get_max_temperature(self, position: int | None = 1) -> float:
        """Get maximum temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HotWaterTank.MAX_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HotWaterTank.MAX_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def set_max_temperature(self, temperature: int, position: int | None = 1) -> None:
        """Set maximum temperature."""
        await self._write_values(request={HotWaterTank.MAX_TEMPERATURE: str(temperature)}, position=position)


class HeatPumpSection(BaseSection):
    """Class to retrieve the heat pump data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_status(self, position: int | None = 1) -> int:
        """Get status."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.STATUS,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.STATUS)
        value: int = int(response[_position][_key])
        return value

    async def get_circulation_pump(self, position: int | None = 1) -> float:
        """Get circulation pump."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.CIRCULATION_PUMP,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.CIRCULATION_PUMP)
        value: float = response[_position][_key]
        return value

    async def get_inflow_temperature(self, position: int | None = 1) -> float:
        """Get inflow temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.INFLOW_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.INFLOW_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_reflux_temperature(self, position: int | None = 1) -> float:
        """Get reflux temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.REFLUX_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.REFLUX_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_source_input_temperature(self, position: int | None = 1) -> float:
        """Get source input temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.SOURCE_INPUT_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.SOURCE_INPUT_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_source_output_temperature(self, position: int | None = 1) -> float:
        """Get source output temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.SOURCE_OUTPUT_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.SOURCE_OUTPUT_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_compressor_input_temperature(self, position: int | None = 1) -> float:
        """Get compressor input temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.COMPRESSOR_INPUT_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.COMPRESSOR_INPUT_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_compressor_output_temperature(self, position: int | None = 1) -> float:
        """Get compressor output temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_compressor(self, position: int | None = 1) -> float:
        """Get compressor."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.COMPRESSOR,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.COMPRESSOR)
        value: float = response[_position][_key]
        return value

    async def get_high_pressure(self, position: int | None = 1) -> float:
        """Get high pressure in bar."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.HIGH_PRESSURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.HIGH_PRESSURE)
        value: float = response[_position][_key]
        return value

    async def get_low_pressure(self, position: int | None = 1) -> float:
        """Get low pressure in bar."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatPump.LOW_PRESSURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatPump.LOW_PRESSURE)
        value: float = response[_position][_key]
        return value


class HeatCircuitSection(BaseSection):
    """Class to send and retrieve the heat pump data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_temperature(self, position: int | None = 1) -> float:
        """Get temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_day_temperature(self, position: int | None = 1) -> float:
        """Get day temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.DAY_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.DAY_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def set_day_temperature(self, temperature: int, position: int | None = 1) -> None:
        """Set temperature."""
        await self._write_values(
            request={HeatCircuit.DAY_TEMPERATURE: str(temperature)},
            position=position,
        )

    async def get_day_temperature_threshold(self, position: int | None = 1) -> float:
        """Get day temperature threshold."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.DAY_TEMPERATURE_THRESHOLD,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.DAY_TEMPERATURE_THRESHOLD)
        value: float = response[_position][_key]
        return value

    async def get_night_temperature(self, position: int | None = 1) -> float | None:
        """Get night temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.NIGHT_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.NIGHT_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def set_night_temperature(self, temperature: int, position: int | None = 1) -> None:
        """Set night temperature."""
        await self._write_values(request={HeatCircuit.NIGHT_TEMPERATURE: str(temperature)}, position=position)

    async def get_night_temperature_threshold(self, position: int | None = 1) -> float:
        """Get night temperature threshold."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.NIGHT_TEMPERATURE_THRESHOLD,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.NIGHT_TEMPERATURE_THRESHOLD)
        value: float = response[_position][_key]
        return value

    async def get_holiday_temperature(self, position: int | None = 1) -> float:
        """Get holiday temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.HOLIDAY_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.HOLIDAY_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def get_offset_temperature(self, position: int | None = 1) -> float:
        """Get offset temperature."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.OFFSET_TEMPERATURE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.OFFSET_TEMPERATURE)
        value: float = response[_position][_key]
        return value

    async def set_offset_temperature(self, offset: int, position: int | None = 1) -> None:
        """Set offset temperature."""
        await self._write_values(request={HeatCircuit.OFFSET_TEMPERATURE: str(offset)}, position=position)

    async def get_operating_mode(self, position: int | None = 1) -> int:
        """Get operating mode."""
        response: dict[str, dict[str, float | int]] = await self._read_values(
            request=HeatCircuit.OPERATING_MODE,
            position=position,
        )
        _position: str = str(position if position else 1)
        _key: str = self._get_real_key(HeatCircuit.OPERATING_MODE)
        value: int = int(response[_position][_key])
        return value

    async def set_operating_mode(self, mode: int, position: int | None = 1) -> None:
        """Set operating mode."""
        await self._write_values(request={HeatCircuit.OPERATING_MODE: str(mode)}, position=position)
