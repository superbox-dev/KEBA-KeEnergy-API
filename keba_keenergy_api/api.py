"""Client to interact with KEBA KeEnergy API."""
import json
from typing import Any

from aiohttp import ClientSession

from keba_keenergy_api.endpoints import BaseEndpoint
from keba_keenergy_api.endpoints import Device
from keba_keenergy_api.endpoints import HeatCircuit
from keba_keenergy_api.endpoints import HeatPump
from keba_keenergy_api.endpoints import HotWaterTank


class KebaKeEnergyAPI(BaseEndpoint):
    """Client to interact with KEBA KeEnergy API."""

    def __init__(self, host: str, *, ssl: bool = False, session: ClientSession | None = None) -> None:
        """Initialize with Client Session and host."""
        schema: str = "https" if ssl else "http"
        base_url: str = f"{schema}://{host}/var/readWriteVars"

        self.device: Device = Device(base_url=f"{schema}://{host}/deviceControl", ssl=ssl, session=session)
        self.hot_water_tank: HotWaterTank = HotWaterTank(base_url=base_url, ssl=ssl, session=session)
        self.heat_pump: HeatPump = HeatPump(base_url=base_url, ssl=ssl, session=session)
        self.heat_circuit: HeatCircuit = HeatCircuit(base_url=base_url, ssl=ssl, session=session)

        super().__init__(payload_type="APPL.CtrlAppl.sParam", base_url=base_url, ssl=ssl, session=session)

    async def get_outdoor_temperature(self) -> float:
        """Get outdoor temperature."""
        payload: dict[str, str] = {
            "name": f"{self._payload_type}.outdoorTemp.values.actValue",
        }

        data: list[dict[str, Any]] = await self._post(payload=json.dumps([payload]))
        return float(data[0]["value"])
