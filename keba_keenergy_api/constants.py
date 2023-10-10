"""All API Constants."""
from enum import Enum
from typing import Final
from typing import NamedTuple
from typing import TypeAlias

API_DEFAULT_TIMEOUT: int = 10


class Endpoint:
    READ_VALUES: Final[str] = "/var/readWriteVars"
    WRITE_VALUES: Final[str] = "/var/readWriteVars?action=set"
    DEVICE_INFO: Final[str] = "/deviceControl?action=getDeviceInfo"


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


OPTIONS_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.options"
OUTDOOR_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.outdoorTemp"
HOT_WATER_TANK_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.hotWaterTank"
HEAT_PUMP_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.heatpump"
HEAT_CIRCUIT_PREFIX: Final[str] = "APPL.CtrlAppl.sParam.heatCircuit"


class ControlValue(NamedTuple):
    value: str
    data_type: type[float | int]
    read_only: bool


class Options(Enum):
    HOT_WATER_TANK_NUMBERS: Final[ControlValue] = ControlValue("systemNumberOfHotWaterTanks", int, read_only=True)
    HEAT_PUMP_NUMBERS: Final[ControlValue] = ControlValue("systemNumberOfHeatPumps", int, read_only=True)
    HEAT_CIRCUIT_NUMBERS: Final[ControlValue] = ControlValue("systemNumberOfHeatingCircuits", int, read_only=True)


class Outdoor(Enum):
    TEMPERATURE: Final[ControlValue] = ControlValue("values.actValue", float, read_only=True)


class HotWaterTank(Enum):
    TEMPERATURE: Final[ControlValue] = ControlValue("topTemp.values.actValue", float, read_only=True)
    OPERATING_MODE: Final[ControlValue] = ControlValue("param.operatingMode", int, read_only=False)
    MIN_TEMPERATURE: Final[ControlValue] = ControlValue("param.reducedSetTempMax.value", float, read_only=False)
    MAX_TEMPERATURE: Final[ControlValue] = ControlValue("param.normalSetTempMax.value", float, read_only=False)


class HeatPump(Enum):
    STATUS: Final[ControlValue] = ControlValue("values.heatpumpState", int, read_only=False)
    CIRCULATION_PUMP: Final[ControlValue] = ControlValue("CircPump.values.setValueScaled", float, read_only=True)
    INFLOW_TEMPERATURE: Final[ControlValue] = ControlValue("TempHeatFlow.values.actValue", float, read_only=True)
    REFLUX_TEMPERATURE: Final[ControlValue] = ControlValue("TempHeatReflux.values.actValue", float, read_only=True)
    SOURCE_INPUT_TEMPERATURE: Final[ControlValue] = ControlValue("TempSourceIn.values.actValue", float, read_only=True)
    SOURCE_OUTPUT_TEMPERATURE: Final[ControlValue] = ControlValue(
        "TempSourceOut.values.actValue",
        float,
        read_only=True,
    )
    COMPRESSOR_INPUT_TEMPERATURE: Final[ControlValue] = ControlValue(
        "TempCompressorIn.values.actValue",
        float,
        read_only=True,
    )
    COMPRESSOR_OUTPUT_TEMPERATURE: Final[ControlValue] = ControlValue(
        "TempCompressorOut.values.actValue",
        float,
        read_only=True,
    )
    COMPRESSOR: Final[ControlValue] = ControlValue("Compressor.values.setValueScaled", float, read_only=True)
    HIGH_PRESSURE: Final[ControlValue] = ControlValue("HighPressure.values.actValue", float, read_only=True)
    LOW_PRESSURE: Final[ControlValue] = ControlValue("LowPressure.values.actValue", float, read_only=True)


class HeatCircuit(Enum):
    TEMPERATURE: Final[ControlValue] = ControlValue("values.setValue", float, read_only=True)
    DAY_TEMPERATURE: Final[ControlValue] = ControlValue("param.normalSetTemp", float, read_only=False)
    DAY_TEMPERATURE_THRESHOLD: Final[ControlValue] = ControlValue("param.thresholdDayTemp.value", float, read_only=True)
    NIGHT_TEMPERATURE: Final[ControlValue] = ControlValue("param.reducedSetTemp", float, read_only=False)
    NIGHT_TEMPERATURE_THRESHOLD: Final[ControlValue] = ControlValue(
        "param.thresholdNightTemp.value",
        float,
        read_only=True,
    )
    HOLIDAY_TEMPERATURE: Final[ControlValue] = ControlValue("param.holidaySetTemp", float, read_only=True)
    OFFSET_TEMPERATURE: Final[ControlValue] = ControlValue("param.offsetRoomTemp", float, read_only=False)
    OPERATING_MODE: Final[ControlValue] = ControlValue("param.operatingMode", int, read_only=False)


Control: TypeAlias = Outdoor | Options | HotWaterTank | HeatPump | HeatCircuit
