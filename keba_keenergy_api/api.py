"""Client to interact with KEBA KeEnergy API."""

from typing import Any

from aiohttp import ClientSession

from keba_keenergy_api.constants import Section
from keba_keenergy_api.constants import SectionPrefix
from keba_keenergy_api.endpoints import BaseEndpoints
from keba_keenergy_api.endpoints import HeatCircuitEndpoints
from keba_keenergy_api.endpoints import HeatPumpEndpoints
from keba_keenergy_api.endpoints import HotWaterTankEndpoints
from keba_keenergy_api.endpoints import Position
from keba_keenergy_api.endpoints import SystemEndpoints
from keba_keenergy_api.endpoints import Value
from keba_keenergy_api.endpoints import ValueResponse


class KebaKeEnergyAPI(BaseEndpoints):
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
    def system(self) -> SystemEndpoints:
        """Get system endpoints."""
        return SystemEndpoints(base_url=self.device_url, ssl=self.ssl, session=self.session)

    @property
    def hot_water_tank(self) -> HotWaterTankEndpoints:
        """Get hot water tank endpoints."""
        return HotWaterTankEndpoints(base_url=self.device_url, ssl=self.ssl, session=self.session)

    @property
    def heat_pump(self) -> HeatPumpEndpoints:
        """Get heat pump endpoints."""
        return HeatPumpEndpoints(base_url=self.device_url, ssl=self.ssl, session=self.session)

    @property
    def heat_circuit(self) -> HeatCircuitEndpoints:
        """Get heat circuit endpoints."""
        return HeatCircuitEndpoints(base_url=self.device_url, ssl=self.ssl, session=self.session)

    async def read_data(
        self,
        request: Section | list[Section],
        position: Position | int | list[int | None] | None = None,
        *,
        human_readable: bool = True,
        extra_attributes: bool = True,
    ) -> dict[str, ValueResponse]:
        """Read multiple data from API with one request."""
        if position is None:
            position = await self.system.get_positions()

        response: dict[str, list[Value]] = await self._read_data(
            request=request,
            position=position,
            human_readable=human_readable,
            extra_attributes=extra_attributes,
        )

        data: dict[str, ValueResponse] = {
            SectionPrefix.SYSTEM.value: {},
            SectionPrefix.HOT_WATER_TANK.value: {},
            SectionPrefix.HEAT_PUMP.value: {},
            SectionPrefix.HEAT_CIRCUIT.value: {},
        }

        for key, value in response.items():
            _key: str = ""

            if key.startswith(SectionPrefix.SYSTEM):
                _key = key.lower().replace(f"{SectionPrefix.SYSTEM.value}_", "")
                data[SectionPrefix.SYSTEM][_key] = value[0]
            elif key.startswith(SectionPrefix.HOT_WATER_TANK):
                _key = key.lower().replace(f"{SectionPrefix.HOT_WATER_TANK.value}_", "")
                data[SectionPrefix.HOT_WATER_TANK][_key] = value
            elif key.startswith(SectionPrefix.HEAT_PUMP):
                _key = key.lower().replace(f"{SectionPrefix.HEAT_PUMP.value}_", "")
                data[SectionPrefix.HEAT_PUMP][_key] = value
            elif key.startswith(SectionPrefix.HEAT_CIRCUIT):
                _key = key.lower().replace(f"{SectionPrefix.HEAT_CIRCUIT.value}_", "")
                data[SectionPrefix.HEAT_CIRCUIT][_key] = value

        return data

    async def write_data(self, request: dict[Section, list[Any]]) -> None:
        """Write multiple data to API with one request."""
        await self._write_values(request=request)
