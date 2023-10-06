import json
import re
from typing import Any

import yarl
from aioresponses import CallbackResult

RE_ENDPOINTS = re.compile(r"^/var/readWriteVars(?:\?action=set)?$")


def mock_kenergy_api_callback(  # noqa: C901, PLR0912, PLR0915
    url: yarl.URL,
    data: str,
    **kwargs: Any,  # noqa: ARG001, ANN401
) -> CallbackResult:
    """Mock the KEBA KeEnergy API."""
    m = RE_ENDPOINTS.match(url.path)

    if m is None:
        return CallbackResult(status=404)

    _data: list[dict[str, str]] = json.loads(data)
    name: str = _data[0]["name"]
    value: str | None = _data[0].get("value")

    result: CallbackResult = CallbackResult(status=404)

    if name == "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.outdoorTemp.values.actValue", "value": "10.808357"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].topTemp.values.actValue", "value": "58.900002"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}"
            if value
            else '[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.operatingMode", "value": "3"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}"
            if value
            else '[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.reducedSetTempMax.value", "value": "0"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}"
            if value
            else '[{"name": "APPL.CtrlAppl.sParam.hotWaterTank[0].param.normalSetTempMax.value", "value": "47"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}" if value else '[{"name": "APPL.CtrlAppl.sParam.heatpump[0].values.heatpumpState", "value": "0"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].CircPump.values.setValueScaled", "value": "0.5"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatFlow.values.actValue", "value": "24.200001"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempHeatReflux.values.actValue", "value": "23.200001"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceIn.values.actValue", "value": "22.700001"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempSourceOut.values.actValue", "value": "24.6"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorIn.values.actValue", "value": "26.4"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].TempCompressorOut.values.actValue", "value": "26.5"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].Compressor.values.setValueScaled", "value": "0.3"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].HighPressure.values.actValue", "value": "15.018749"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatpump[0].LowPressure.values.actValue", "value": "14.8125"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].values.setValue", "value": "22"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}"
            if value
            else '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.normalSetTemp", "value": "23"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdDayTemp.value", "value": "16"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}"
            if value
            else '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.reducedSetTemp", "value": "23"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.thresholdNightTemp.value", "value": "16"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body='[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.holidaySetTemp", "value": "14"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}"
            if value
            else '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.offsetRoomTemp", "value": "2"}]',
        )
    elif name == "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode":
        result = CallbackResult(
            status=200,
            headers={"Content-Type": "application/json;charset=utf-8"},
            body="{}"
            if value
            else '[{"name": "APPL.CtrlAppl.sParam.heatCircuit[0].param.operatingMode", "value": "3"}]',
        )

    return result
