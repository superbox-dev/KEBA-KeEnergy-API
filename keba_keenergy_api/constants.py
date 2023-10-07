"""All API Constants."""
from typing import Final

API_DEFAULT_TIMEOUT: int = 10


class HotWaterTankOperatingMode:
    OFF: Final[int] = 0
    HEAT_UP: Final[int] = 3


class HeatPumpStatus:
    STANDBY: Final[int] = 0
    FLOW: Final[int] = 1
    AUTO: Final[int] = 2


class HeatCircuitOperatingMode:
    OFF: Final[int] = 0
    AUTO: Final[int] = 1
    DAY: Final[int] = 2
    NIGHT: Final[int] = 3
