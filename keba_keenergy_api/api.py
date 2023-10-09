"""Client to interact with KEBA KeEnergy API."""
from typing import Any

from aiohttp import ClientSession

from keba_keenergy_api.constants import Control
from keba_keenergy_api.constants import Outdoor
from keba_keenergy_api.endpoints import BaseSection
from keba_keenergy_api.endpoints import DeviceSection
from keba_keenergy_api.endpoints import HeatCircuitSection
from keba_keenergy_api.endpoints import HeatPumpSection
from keba_keenergy_api.endpoints import HotWaterTankSection


class KebaKeEnergyAPI(BaseSection):
    """Client to interact with KEBA KeEnergy API."""

    def __init__(self, host: str, *, ssl: bool = False, session: ClientSession | None = None) -> None:
        """Initialize with Client Session and host."""
        schema: str = "https" if ssl else "http"
        base_url: str = f"{schema}://{host}"

        self.device: DeviceSection = DeviceSection(base_url=base_url, ssl=ssl, session=session)
        self.hot_water_tank: HotWaterTankSection = HotWaterTankSection(base_url=base_url, ssl=ssl, session=session)
        self.heat_pump: HeatPumpSection = HeatPumpSection(base_url=base_url, ssl=ssl, session=session)
        self.heat_circuit: HeatCircuitSection = HeatCircuitSection(base_url=base_url, ssl=ssl, session=session)

        super().__init__(base_url=base_url, ssl=ssl, session=session)

    async def read_values(
        self,
        request: Control | list[Control],
        position: int | None | list[int | None] = 1,
    ) -> dict[str, dict[str, Any]]:
        return await self._read_values(
            request=request,
            position=position,
        )

    async def write_values(
        self,
        request: dict[Control, Any],
        position: int | None | list[int | None] = 1,
    ) -> None:
        await self._write_values(
            request=request,
            position=position,
        )

    async def get_outdoor_temperature(self) -> float:
        """Get outdoor temperature."""
        response: dict[str, Any] = await self._read_values(request=Outdoor.TEMPERATURE, position=None)
        _key: str = self._get_real_key(Outdoor.TEMPERATURE)
        value: float = response["1"][_key]
        return value
