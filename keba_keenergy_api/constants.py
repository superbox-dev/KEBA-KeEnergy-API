"""All API Constants."""
from enum import Enum
from enum import IntEnum
from typing import Final
from typing import NamedTuple
from typing import TypeAlias

API_DEFAULT_TIMEOUT: int = 10


class Endpoint:
    READ_VALUES: Final[str] = "/var/readWriteVars"
    WRITE_VALUES: Final[str] = "/var/readWriteVars?action=set"
    DEVICE_INFO: Final[str] = "/deviceControl?action=getDeviceInfo"
    SYSTEM_INFO: Final[str] = "/swupdate?action=getSystemInstalled"


class HotWaterTankOperatingMode(IntEnum):
    OFF: Final[int] = 0
    AUTO: Final[int] = 1
    ON: Final[int] = 2
    HEAT_UP: Final[int] = 3


class HeatPumpStatus(IntEnum):
    STANDBY: Final[int] = 0
    FLOW: Final[int] = 1
    AUTO: Final[int] = 2


class HeatCircuitOperatingMode(IntEnum):
    OFF: Final[int] = 0
    AUTO: Final[int] = 1
    DAY: Final[int] = 2
    NIGHT: Final[int] = 3
    AWAY: Final[int] = 4
    PARTY: Final[int] = 5


OPTIONS_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.options"
OUTDOOR_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.outdoorTemp"
HOT_WATER_TANK_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.hotWaterTank"
HEAT_PUMP_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.heatpump"
HEAT_CIRCUIT_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.heatCircuit"


class ControlValue(NamedTuple):
    value: str
    data_type: type[float | int | str]
    read_only: bool = True
    human_readable: type[IntEnum] | None = None


class Options(Enum):
    HOT_WATER_TANK_NUMBERS: Final[ControlValue] = ControlValue("systemNumberOfHotWaterTanks", int)
    HEAT_PUMP_NUMBERS: Final[ControlValue] = ControlValue("systemNumberOfHeatPumps", int)
    HEAT_CIRCUIT_NUMBERS: Final[ControlValue] = ControlValue("systemNumberOfHeatingCircuits", int)


class Outdoor(Enum):
    TEMPERATURE: Final[ControlValue] = ControlValue("values.actValue", float)


class HotWaterTank(Enum):
    TEMPERATURE: Final[ControlValue] = ControlValue("topTemp.values.actValue", float)
    OPERATING_MODE: Final[ControlValue] = ControlValue(
        "param.operatingMode",
        int,
        read_only=False,
        human_readable=HotWaterTankOperatingMode,
    )
    MIN_TEMPERATURE: Final[ControlValue] = ControlValue(
        "param.reducedSetTempMax.value",
        float,
        read_only=False,
    )
    MAX_TEMPERATURE: Final[ControlValue] = ControlValue("param.normalSetTempMax.value", float, read_only=False)


class HeatPump(Enum):
    NAME: Final[ControlValue] = ControlValue("param.name", str)
    STATUS: Final[ControlValue] = ControlValue(
        "values.heatpumpState",
        int,
        read_only=False,
        human_readable=HeatPumpStatus,
    )
    CIRCULATION_PUMP: Final[ControlValue] = ControlValue("CircPump.values.setValueScaled", float)
    INFLOW_TEMPERATURE: Final[ControlValue] = ControlValue("TempHeatFlow.values.actValue", float)
    REFLUX_TEMPERATURE: Final[ControlValue] = ControlValue("TempHeatReflux.values.actValue", float)
    SOURCE_INPUT_TEMPERATURE: Final[ControlValue] = ControlValue("TempSourceIn.values.actValue", float)
    SOURCE_OUTPUT_TEMPERATURE: Final[ControlValue] = ControlValue("TempSourceOut.values.actValue", float)
    COMPRESSOR_INPUT_TEMPERATURE: Final[ControlValue] = ControlValue("TempCompressorIn.values.actValue", float)
    COMPRESSOR_OUTPUT_TEMPERATURE: Final[ControlValue] = ControlValue("TempCompressorOut.values.actValue", float)
    COMPRESSOR: Final[ControlValue] = ControlValue("Compressor.values.setValueScaled", float)
    HIGH_PRESSURE: Final[ControlValue] = ControlValue("HighPressure.values.actValue", float)
    LOW_PRESSURE: Final[ControlValue] = ControlValue("LowPressure.values.actValue", float)


class HeatCircuit(Enum):
    NAME: Final[ControlValue] = ControlValue("param.name", str)
    TEMPERATURE: Final[ControlValue] = ControlValue("values.setValue", float)
    DAY_TEMPERATURE: Final[ControlValue] = ControlValue("param.normalSetTemp", float, read_only=False)
    DAY_TEMPERATURE_THRESHOLD: Final[ControlValue] = ControlValue("param.thresholdDayTemp.value", float)
    NIGHT_TEMPERATURE: Final[ControlValue] = ControlValue("param.reducedSetTemp", float, read_only=False)
    NIGHT_TEMPERATURE_THRESHOLD: Final[ControlValue] = ControlValue("param.thresholdNightTemp.value", float)
    HOLIDAY_TEMPERATURE: Final[ControlValue] = ControlValue("param.holidaySetTemp", float)
    OFFSET_TEMPERATURE: Final[ControlValue] = ControlValue("param.offsetRoomTemp", float, read_only=False)
    OPERATING_MODE: Final[ControlValue] = ControlValue(
        "param.operatingMode",
        int,
        read_only=False,
        human_readable=HeatCircuitOperatingMode,
    )


class SystemPrefix(str, Enum):
    """System prefixes."""

    OPTIONS: Final[str] = "OPTIONS_"
    OUTDOOR: Final[str] = "OUTDOOR_"
    HOT_WATER_TANK: Final[str] = "HOT_WATER_TANK_"
    HEAT_PUMP: Final[str] = "HEAT_PUMP_"
    HEAT_CIRCUIT = "HEAT_CIRCUIT_"


Control: TypeAlias = Options | Outdoor | HotWaterTank | HeatPump | HeatCircuit
