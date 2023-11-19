"""All API Constants."""
from enum import Enum
from enum import IntEnum
from typing import Final
from typing import NamedTuple
from typing import TypeAlias

API_DEFAULT_TIMEOUT: int = 10


class EndpointPath:
    """The endpoint paths."""

    READ_WRITE_VARS: Final[str] = "/var/readWriteVars"
    DEVICE_CONTROL: Final[str] = "/deviceControl"
    SW_UPDATE: Final[str] = "/swupdate"


class SystemOperatingMode(IntEnum):
    """Available system operating modes."""

    SETUP: Final[int] = -1
    STANDBY: Final[int] = 0
    SUMMER: Final[int] = 1
    AUTO_HEAT: Final[int] = 2
    AUTO_COOL: Final[int] = 3
    AUTO: Final[int] = 4


class HotWaterTankOperatingMode(IntEnum):
    """Available hot water tank operating modes."""

    OFF: Final[int] = 0
    AUTO: Final[int] = 1
    ON: Final[int] = 2
    HEAT_UP: Final[int] = 3


class HeatPumpState(IntEnum):
    """Available heat pump stats."""

    STANDBY: Final[int] = 0
    FLOW: Final[int] = 1
    AUTO_HEAT: Final[int] = 2
    DEFROST: Final[int] = 3
    AUTO_COOL: Final[int] = 4
    INFLOW: Final[int] = 5


class HeatPumpOperatingMode(IntEnum):
    """Available heat pump operating modes."""

    OFF: Final[int] = 0
    ON: Final[int] = 1
    BACKUP: Final[int] = 2


class HeatCircuitOperatingMode(IntEnum):
    """Available heat circuit operating modes."""

    OFF: Final[int] = 0
    AUTO: Final[int] = 1
    DAY: Final[int] = 2
    NIGHT: Final[int] = 3
    AWAY: Final[int] = 4
    PARTY: Final[int] = 5
    EXTERN: Final[int] = 8


class HotWaterTankHeatRequest(str, Enum):
    """Available hot water tank heat request stats."""

    OFF: Final[str] = "false"
    ON: Final[str] = "true"


class HeatPumpHeatRequest(str, Enum):
    """Available heat pump heat request stats."""

    OFF: Final[str] = "false"
    ON: Final[str] = "true"


class HeatCircuitHeatRequest(str, Enum):
    """Available heat circuit heat request stats."""

    OFF: Final[str] = "0"
    ON: Final[str] = "1"
    TEMPORARY_OFF: Final[str] = "3"


class HeatCircuitExternalCoolRequest(str, Enum):
    """Available heat circuit external cool request stats."""

    OFF: Final[str] = "false"
    ON: Final[str] = "true"


class HeatCircuitExternalHeatRequest(str, Enum):
    """Available heat circuit external heat request stats."""

    OFF: Final[str] = "false"
    ON: Final[str] = "true"


SYSTEM_PREFIX: Final[str] = "APPL.CtrlAppl.sParam"
HOT_WATER_TANK_PREFIX: Final[str] = f"{SYSTEM_PREFIX}.hotWaterTank"
HEAT_PUMP_PREFIX: Final[str] = f"{SYSTEM_PREFIX}.heatpump"
HEAT_CIRCUIT_PREFIX: Final[str] = f"{SYSTEM_PREFIX}.heatCircuit"


class EndpointProperties(NamedTuple):
    """Properties from an endpoint."""

    value: str
    value_type: type[float | int | str]
    read_only: bool = True
    human_readable: type[Enum] | None = None


class System(Enum):
    """The system endpoint settings."""

    HOT_WATER_TANK_NUMBERS: Final[EndpointProperties] = EndpointProperties(
        "options.systemNumberOfHotWaterTanks",
        value_type=int,
    )
    HEAT_PUMP_NUMBERS: Final[EndpointProperties] = EndpointProperties(
        "options.systemNumberOfHeatPumps",
        value_type=int,
    )
    HEAT_CIRCUIT_NUMBERS: Final[EndpointProperties] = EndpointProperties(
        "options.systemNumberOfHeatingCircuits",
        value_type=int,
    )
    OPERATING_MODE: Final[EndpointProperties] = EndpointProperties(
        "param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=SystemOperatingMode,
    )
    OUTDOOR_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "outdoorTemp.values.actValue",
        value_type=float,
    )


class HotWaterTank(Enum):
    """The hot water tank endpoint settings."""

    TEMPERATURE: Final[EndpointProperties] = EndpointProperties("topTemp.values.actValue", float)
    OPERATING_MODE: Final[EndpointProperties] = EndpointProperties(
        "param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HotWaterTankOperatingMode,
    )
    MIN_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "param.reducedSetTempMax.value",
        float,
        read_only=False,
    )
    MAX_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "param.normalSetTempMax.value",
        float,
        read_only=False,
    )
    HEAT_REQUEST: Final[EndpointProperties] = EndpointProperties(
        "values.heatRequestTop",
        value_type=str,
        human_readable=HotWaterTankHeatRequest,
    )


class HeatPump(Enum):
    """The heat pump endpoint settings."""

    NAME: Final[EndpointProperties] = EndpointProperties("param.name", value_type=str)
    STATE: Final[EndpointProperties] = EndpointProperties(
        "values.heatpumpState",
        value_type=int,
        read_only=False,
        human_readable=HeatPumpState,
    )
    OPERATING_MODE: Final[EndpointProperties] = EndpointProperties(
        "param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HeatPumpOperatingMode,
    )
    CIRCULATION_PUMP: Final[EndpointProperties] = EndpointProperties(
        "CircPump.values.setValueScaled",
        value_type=float,
    )
    INFLOW_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "TempHeatFlow.values.actValue",
        value_type=float,
    )
    REFLUX_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "TempHeatReflux.values.actValue",
        value_type=float,
    )
    SOURCE_INPUT_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "TempSourceIn.values.actValue",
        value_type=float,
    )
    SOURCE_OUTPUT_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "TempSourceOut.values.actValue",
        value_type=float,
    )
    COMPRESSOR_INPUT_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "TempCompressorIn.values.actValue",
        value_type=float,
    )
    COMPRESSOR_OUTPUT_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "TempCompressorOut.values.actValue",
        value_type=float,
    )
    COMPRESSOR: Final[EndpointProperties] = EndpointProperties(
        "Compressor.values.setValueScaled",
        value_type=float,
    )
    HIGH_PRESSURE: Final[EndpointProperties] = EndpointProperties(
        "HighPressure.values.actValue",
        value_type=float,
    )
    LOW_PRESSURE: Final[EndpointProperties] = EndpointProperties(
        "LowPressure.values.actValue",
        value_type=float,
    )
    HEAT_REQUEST: Final[EndpointProperties] = EndpointProperties(
        "values.request",
        value_type=str,
        human_readable=HeatPumpHeatRequest,
    )


class HeatCircuit(Enum):
    """The heat circuit endpoint settings."""

    NAME: Final[EndpointProperties] = EndpointProperties(
        "param.name",
        value_type=str,
    )
    TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "values.setValue",
        value_type=float,
    )
    DAY_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "param.normalSetTemp",
        value_type=float,
        read_only=False,
    )
    DAY_TEMPERATURE_THRESHOLD: Final[EndpointProperties] = EndpointProperties(
        "param.thresholdDayTemp.value",
        value_type=float,
    )
    NIGHT_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "param.reducedSetTemp",
        value_type=float,
        read_only=False,
    )
    NIGHT_TEMPERATURE_THRESHOLD: Final[EndpointProperties] = EndpointProperties(
        "param.thresholdNightTemp.value",
        value_type=float,
    )
    HOLIDAY_TEMPERATURE: Final[EndpointProperties] = EndpointProperties(
        "param.holidaySetTemp",
        value_type=float,
        read_only=False,
    )
    TEMPERATURE_OFFSET: Final[EndpointProperties] = EndpointProperties(
        "param.offsetRoomTemp",
        value_type=float,
        read_only=False,
    )
    HEAT_REQUEST: Final[EndpointProperties] = EndpointProperties(
        "values.heatRequest",
        value_type=str,
        human_readable=HeatCircuitHeatRequest,
    )
    EXTERNAL_COOL_REQUEST: Final[EndpointProperties] = EndpointProperties(
        "param.external.coolRequest",
        value_type=str,
        human_readable=HeatCircuitExternalCoolRequest,
    )
    EXTERNAL_HEAT_REQUEST: Final[EndpointProperties] = EndpointProperties(
        "param.external.heatRequest",
        value_type=str,
        human_readable=HeatCircuitExternalHeatRequest,
    )
    OPERATING_MODE: Final[EndpointProperties] = EndpointProperties(
        "param.operatingMode",
        value_type=int,
        read_only=False,
        human_readable=HeatCircuitOperatingMode,
    )


class SectionPrefix(str, Enum):
    """Section prefixes."""

    SYSTEM: Final[str] = "system"
    HOT_WATER_TANK: Final[str] = "hot_water_tank"
    HEAT_PUMP: Final[str] = "heat_pump"
    HEAT_CIRCUIT = "heat_circuit"


Section: TypeAlias = System | HotWaterTank | HeatPump | HeatCircuit
