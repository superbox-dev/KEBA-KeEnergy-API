"""Retrieve hot water tank data."""
import importlib
import json
import re
from enum import Enum
from json import JSONDecodeError
from re import Pattern
from typing import Any
from typing import NamedTuple
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import TypedDict

from aiohttp import ClientSession
from aiohttp import ClientTimeout

from keba_keenergy_api.constants import API_DEFAULT_TIMEOUT
from keba_keenergy_api.constants import Control
from keba_keenergy_api.constants import Endpoint
from keba_keenergy_api.constants import HeatCircuit
from keba_keenergy_api.constants import HeatPump
from keba_keenergy_api.constants import HotWaterTank
from keba_keenergy_api.constants import Options
from keba_keenergy_api.constants import Outdoor
from keba_keenergy_api.error import APIError
from keba_keenergy_api.error import InvalidJsonError

if TYPE_CHECKING:
    from types import ModuleType


class ReadPayload(TypedDict):
    name: str


class WritePayload(TypedDict):
    name: str
    value: str


ValueResponse: TypeAlias = dict[str, tuple[float | int, ...]]
Payload: TypeAlias = list[ReadPayload | WritePayload]
Response: TypeAlias = list[dict[str, str]]


class Position(NamedTuple):
    heat_pump: int
    heat_circuit: int
    hot_water_tank: int


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

    async def _post(self, payload: str | None = None, endpoint: str | None = None) -> Response:
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
                response: list[dict[str, Any]] = await resp.json(
                    content_type="application/json;charset=utf-8",
                )
        except JSONDecodeError as error:
            response_text = await resp.text()
            raise InvalidJsonError(response_text) from error
        finally:
            if not self._session:
                await session.close()

        if isinstance(response, dict) and "developerMessage" in response:
            raise APIError(response["developerMessage"])

        if isinstance(response, dict):
            response = [response]

        return response

    def _get_real_key(self, key: Control, *, key_prefix: bool = True) -> str:
        class_name: str = key.__class__.__name__
        _real_key: str = key.name

        if key_prefix is True:
            _real_key = f"{self.KEY_PATTERN.sub('_', class_name).upper()}_{_real_key}"

        return _real_key

    def _get_key_prefix(self, key: Control) -> str:
        module: ModuleType = importlib.import_module("keba_keenergy_api.constants")
        class_name: str = key.__class__.__name__
        prefix: str = getattr(module, f"{self.KEY_PATTERN.sub('_', class_name).upper()}_PREFIX", "")
        return prefix

    @staticmethod
    def _get_position(idx: int | None) -> str:
        _position: str = "" if idx is None else f"[{idx}]"
        return _position

    def _get_position_index(self, control: Control, position: Position | list[int | None]) -> list[int | None]:
        idx: list[int | None] = []

        if isinstance(position, Position):
            position_key: str = f"{self.KEY_PATTERN.sub('_', control.__class__.__name__).lower()}"
            idx = list(range(getattr(position, position_key)))
        elif isinstance(position, list):
            idx = [p if p is None else (p - 1) for p in position]

        return idx

    def _generate_read_payload(
        self,
        request: list[Control],
        position: Position | list[int | None],
        allowed_type: list[type[Enum]] | None,
    ) -> Payload:
        payload: Payload = []

        for control in request:
            if (allowed_type and type(control) in allowed_type) or allowed_type is None:
                for idx in self._get_position_index(control=control, position=position):
                    payload += [
                        ReadPayload(
                            name=f"{self._get_key_prefix(control)}{self._get_position(idx)}.{control.value.value}",
                        ),
                    ]

        return payload

    async def _read_values(
        self,
        request: Control | list[Control],
        position: Position | int | list[int | None] | None = 1,
        allowed_type: type[Enum] | list[type[Enum]] | None = None,
        *,
        key_prefix: bool = True,
    ) -> ValueResponse:
        if isinstance(request, Options | Outdoor | HotWaterTank | HeatPump | HeatCircuit):
            request = [request]

        if isinstance(position, int) or position is None:
            position = [position]

        if isinstance(allowed_type, type):
            allowed_type = [allowed_type]

        payload: Payload = self._generate_read_payload(
            request=request,
            position=position,
            allowed_type=allowed_type,
        )

        _response: list[dict[str, Any]] = await self._post(
            payload=json.dumps(payload),
            endpoint=Endpoint.READ_VALUES,
        )

        response: dict[str, list[float | int]] = {}

        for control in request:
            if (allowed_type and type(control) in allowed_type) or not allowed_type:
                for _ in self._get_position_index(control=control, position=position):
                    value: float | int = control.value.data_type(_response[0]["value"])
                    response_key: str = self._get_real_key(control, key_prefix=key_prefix)

                    if not response.get(response_key):
                        response[response_key] = []

                    response[response_key].append(round(value, 2) if isinstance(value, float) else value)
                    del _response[0]

        return {k: tuple(v) for k, v in response.items()}

    def _generate_write_payload(self, request: dict[Control, tuple[float | int | None, ...]]) -> Payload:
        payload: Payload = []

        for key, values in request.items():
            if not key.value.read_only:
                for idx, value in enumerate(values):
                    if value is not None:
                        payload += [
                            WritePayload(
                                name=f"{self._get_key_prefix(key)}{self._get_position(idx)}.{key.value.value}",
                                value=str(value),
                            ),
                        ]

        return payload

    async def _write_values(self, request: dict[Control, tuple[float | int | None, ...]]) -> None:
        payload: Payload = self._generate_write_payload(request)

        await self._post(
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


class OptionsSection(BaseSection):
    """Class to retrieve the option data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_positions(self) -> Position:
        """Get number of heat pump, heating circuit and hot water tank."""
        data: ValueResponse = await self.read_values(
            request=[
                Options.HEAT_PUMP_NUMBERS,
                Options.HEAT_CIRCUIT_NUMBERS,
                Options.HOT_WATER_TANK_NUMBERS,
            ],
        )

        return Position(**{k.replace("_NUMBERS", "").lower(): int(v[0]) for k, v in data.items()})

    async def read_values(
        self,
        request: Control | list[Control],
    ) -> ValueResponse:
        """Read multiple option values from API with one request."""
        _values: ValueResponse = await self._read_values(
            request=request,
            position=None,
            key_prefix=False,
            allowed_type=Options,
        )

        return _values

    async def get_number_of_hot_water_tanks(self) -> int:
        """Get number of hot water tanks."""
        response: ValueResponse = await self._read_values(
            request=Options.HOT_WATER_TANK_NUMBERS,
            position=None,
        )
        _key: str = self._get_real_key(Options.HOT_WATER_TANK_NUMBERS)
        return int(response[_key][0])

    async def get_number_of_heat_pumps(self) -> int:
        """Get number of heat pumps."""
        response: ValueResponse = await self._read_values(
            request=Options.HEAT_PUMP_NUMBERS,
            position=None,
        )
        _key: str = self._get_real_key(Options.HEAT_PUMP_NUMBERS)
        return int(response[_key][0])

    async def get_number_of_heating_circuits(self) -> int:
        """Get number of heating circuits."""
        response: ValueResponse = await self._read_values(
            request=Options.HEAT_CIRCUIT_NUMBERS,
            position=None,
        )
        _key: str = self._get_real_key(Options.HEAT_CIRCUIT_NUMBERS)
        return int(response[_key][0])


class HotWaterTankSection(BaseSection):
    """Class to send and retrieve the hot water tank data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_temperature(self, position: int | None = 1) -> float:
        """Get current temperature."""
        response: ValueResponse = await self._read_values(
            request=HotWaterTank.TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.TEMPERATURE)
        return float(response[_key][_idx])

    async def get_operating_mode(self, position: int | None = 1) -> int:
        """Get operating mode."""
        response: ValueResponse = await self._read_values(
            request=HotWaterTank.OPERATING_MODE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.OPERATING_MODE)
        return int(response[_key][_idx])

    async def set_operating_mode(self, mode: int, position: int = 1) -> None:
        """Set operating mode."""
        modes: list[int | None] = [mode if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.OPERATING_MODE: tuple(modes)})

    async def get_min_temperature(self, position: int | None = 1) -> float:
        """Get minimum temperature."""
        response: ValueResponse = await self._read_values(
            request=HotWaterTank.MIN_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.MIN_TEMPERATURE)
        return float(response[_key][_idx])

    async def set_min_temperature(self, temperature: int, position: int = 1) -> None:
        """Set minimum temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.MIN_TEMPERATURE: tuple(temperatures)})

    async def get_max_temperature(self, position: int | None = 1) -> float:
        """Get maximum temperature."""
        response: ValueResponse = await self._read_values(
            request=HotWaterTank.MAX_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HotWaterTank.MAX_TEMPERATURE)
        return float(response[_key][_idx])

    async def set_max_temperature(self, temperature: int, position: int = 1) -> None:
        """Set maximum temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HotWaterTank.MAX_TEMPERATURE: tuple(temperatures)})


class HeatPumpSection(BaseSection):
    """Class to retrieve the heat pump data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_status(self, position: int | None = 1) -> int:
        """Get status."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.STATUS,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.STATUS)
        return int(response[_key][_idx])

    async def get_circulation_pump(self, position: int | None = 1) -> float:
        """Get circulation pump."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.CIRCULATION_PUMP,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.CIRCULATION_PUMP)
        return float(response[_key][_idx])

    async def get_inflow_temperature(self, position: int | None = 1) -> float:
        """Get inflow temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.INFLOW_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.INFLOW_TEMPERATURE)
        return float(response[_key][_idx])

    async def get_reflux_temperature(self, position: int | None = 1) -> float:
        """Get reflux temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.REFLUX_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.REFLUX_TEMPERATURE)
        return float(response[_key][_idx])

    async def get_source_input_temperature(self, position: int | None = 1) -> float:
        """Get source input temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.SOURCE_INPUT_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.SOURCE_INPUT_TEMPERATURE)
        return float(response[_key][_idx])

    async def get_source_output_temperature(self, position: int | None = 1) -> float:
        """Get source output temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.SOURCE_OUTPUT_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.SOURCE_OUTPUT_TEMPERATURE)
        return float(response[_key][_idx])

    async def get_compressor_input_temperature(self, position: int | None = 1) -> float:
        """Get compressor input temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.COMPRESSOR_INPUT_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COMPRESSOR_INPUT_TEMPERATURE)
        return float(response[_key][_idx])

    async def get_compressor_output_temperature(self, position: int | None = 1) -> float:
        """Get compressor output temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COMPRESSOR_OUTPUT_TEMPERATURE)
        return float(response[_key][_idx])

    async def get_compressor(self, position: int | None = 1) -> float:
        """Get compressor."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.COMPRESSOR,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.COMPRESSOR)
        return float(response[_key][_idx])

    async def get_high_pressure(self, position: int | None = 1) -> float:
        """Get high pressure in bar."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.HIGH_PRESSURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.HIGH_PRESSURE)
        return float(response[_key][_idx])

    async def get_low_pressure(self, position: int | None = 1) -> float:
        """Get low pressure in bar."""
        response: ValueResponse = await self._read_values(
            request=HeatPump.LOW_PRESSURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatPump.LOW_PRESSURE)
        return float(response[_key][_idx])


class HeatCircuitSection(BaseSection):
    """Class to send and retrieve the heat pump data."""

    def __init__(self, base_url: str, *, ssl: bool, session: ClientSession | None = None) -> None:
        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def get_temperature(self, position: int | None = 1) -> float:
        """Get temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.TEMPERATURE)
        return float(response[_key][_idx])

    async def get_day_temperature(self, position: int | None = 1) -> float:
        """Get day temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.DAY_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.DAY_TEMPERATURE)
        return float(response[_key][_idx])

    async def set_day_temperature(self, temperature: int, position: int = 1) -> None:
        """Set temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.DAY_TEMPERATURE: tuple(temperatures)})

    async def get_day_temperature_threshold(self, position: int | None = 1) -> float:
        """Get day temperature threshold."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.DAY_TEMPERATURE_THRESHOLD,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.DAY_TEMPERATURE_THRESHOLD)
        return float(response[_key][_idx])

    async def get_night_temperature(self, position: int | None = 1) -> float | None:
        """Get night temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.NIGHT_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.NIGHT_TEMPERATURE)
        return float(response[_key][_idx])

    async def set_night_temperature(self, temperature: int, position: int = 1) -> None:
        """Set night temperature."""
        temperatures: list[float | None] = [temperature if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.NIGHT_TEMPERATURE: tuple(temperatures)})

    async def get_night_temperature_threshold(self, position: int | None = 1) -> float:
        """Get night temperature threshold."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.NIGHT_TEMPERATURE_THRESHOLD,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.NIGHT_TEMPERATURE_THRESHOLD)
        return float(response[_key][_idx])

    async def get_holiday_temperature(self, position: int | None = 1) -> float:
        """Get holiday temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.HOLIDAY_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.HOLIDAY_TEMPERATURE)
        return float(response[_key][_idx])

    async def get_offset_temperature(self, position: int | None = 1) -> float:
        """Get offset temperature."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.OFFSET_TEMPERATURE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.OFFSET_TEMPERATURE)
        return float(response[_key][_idx])

    async def set_offset_temperature(self, offset: float, position: int = 1) -> None:
        """Set offset temperature."""
        offsets: list[float | None] = [offset if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.OFFSET_TEMPERATURE: tuple(offsets)})

    async def get_operating_mode(self, position: int | None = 1) -> int:
        """Get operating mode."""
        response: ValueResponse = await self._read_values(
            request=HeatCircuit.OPERATING_MODE,
            position=position,
        )
        _idx: int = position - 1 if position else 0
        _key: str = self._get_real_key(HeatCircuit.OPERATING_MODE)
        return int(response[_key][_idx])

    async def set_operating_mode(self, mode: int, position: int = 1) -> None:
        """Set operating mode."""
        modes: list[int | None] = [mode if position == p else None for p in range(1, position + 1)]
        await self._write_values(request={HeatCircuit.OPERATING_MODE: tuple(modes)})
