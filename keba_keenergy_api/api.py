"""Client to interact with KEBA KeEnergy API."""
from typing import Any

from aiohttp import ClientSession

from keba_keenergy_api.constants import Control
from keba_keenergy_api.constants import Outdoor
from keba_keenergy_api.constants import SystemPrefix
from keba_keenergy_api.endpoints import BaseSection
from keba_keenergy_api.endpoints import DeviceSection
from keba_keenergy_api.endpoints import HeatCircuitSection
from keba_keenergy_api.endpoints import HeatPumpSection
from keba_keenergy_api.endpoints import HotWaterTankSection
from keba_keenergy_api.endpoints import OptionsSection
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.endpoints import ValueResponse


class KebaKeEnergyAPI(BaseSection):
    """Client to interact with KEBA KeEnergy API."""

    def __init__(self, host: str, *, ssl: bool = False, session: ClientSession | None = None) -> None:
        """Initialize with Client Session and host."""
        self.host: str = host
        self.schema: str = "https" if ssl else "http"

        self.ssl: bool = ssl
        self.session: ClientSession | None = session

        super().__init__(base_url=self.device_url, ssl=ssl, session=session)

    @property
    def device_url(self) -> str:
        """Get device url."""
        return f"{self.schema}://{self.host}"

    @property
    def device(self) -> DeviceSection:
        """Get device endpoints."""
        return DeviceSection(base_url=self.device_url, ssl=self.ssl, session=self.session)

    @property
    def options(self) -> OptionsSection:
        """Get options endpoints."""
        return OptionsSection(base_url=self.device_url, ssl=self.ssl, session=self.session)

    @property
    def hot_water_tank(self) -> HotWaterTankSection:
        """Get hot water tank endpoints."""
        return HotWaterTankSection(base_url=self.device_url, ssl=self.ssl, session=self.session)

    @property
    def heat_pump(self) -> HeatPumpSection:
        """Get heat pump endpoints."""
        return HeatPumpSection(base_url=self.device_url, ssl=self.ssl, session=self.session)

    @property
    def heat_circuit(self) -> HeatCircuitSection:
        """Get heat circuit endpoints."""
        return HeatCircuitSection(base_url=self.device_url, ssl=self.ssl, session=self.session)

    async def read_values(
        self,
        request: Control | list[Control],
        position: Position | int | list[int | None] | None = None,
        *,
        human_readable: bool = True,
        extra_attributes: bool = True,
    ) -> ValueResponse:
        """Read multiple values from API with one request."""
        if position is None:
            position = await self.options.get_positions()

        return await self._read_values(
            request=request,
            position=position,
            human_readable=human_readable,
            extra_attributes=extra_attributes,
        )

    async def read_values_grouped_by_section(
        self,
        request: Control | list[Control],
        position: Position | int | list[int | None] | None = None,
        *,
        human_readable: bool = True,
        extra_attributes: bool = True,
    ) -> dict[str, ValueResponse]:
        """Read multiple grouped values from API with one request."""
        response: ValueResponse = await self.read_values(
            request=request,
            position=position,
            human_readable=human_readable,
            extra_attributes=extra_attributes,
        )

        data: dict[str, ValueResponse] = {
            SystemPrefix.OUTDOOR[0:-1]: {},
            SystemPrefix.OPTIONS[0:-1]: {},
            SystemPrefix.HOT_WATER_TANK[0:-1]: {},
            SystemPrefix.HEAT_PUMP[0:-1]: {},
            SystemPrefix.HEAT_CIRCUIT[0:-1]: {},
        }

        for key, value in response.items():
            if key.startswith(SystemPrefix.OUTDOOR):
                data[SystemPrefix.OUTDOOR[0:-1]][key.lower()] = value
            elif key.startswith(SystemPrefix.OPTIONS):
                data[SystemPrefix.OPTIONS[0:-1]][key.lower()] = value
            elif key.startswith(SystemPrefix.HOT_WATER_TANK):
                data[SystemPrefix.HOT_WATER_TANK[0:-1]][key.lower()] = value
            elif key.startswith(SystemPrefix.HEAT_PUMP):
                data[SystemPrefix.HEAT_PUMP[0:-1]][key.lower()] = value
            elif key.startswith(SystemPrefix.HEAT_CIRCUIT):
                data[SystemPrefix.HEAT_CIRCUIT[0:-1]][key.lower()] = value

        return data

    async def write_values(self, request: dict[Control, list[Any]]) -> None:
        """Write multiple values to API with one request."""
        await self._write_values(request=request)

    async def get_outdoor_temperature(self) -> float:
        """Get outdoor temperature."""
        response: dict[str, Any] = await self._read_values(
            request=Outdoor.TEMPERATURE,
            position=None,
            extra_attributes=True,
        )
        _key: str = self._get_real_key(Outdoor.TEMPERATURE)
        return float(response[_key][0]["value"])
