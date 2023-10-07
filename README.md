![coverage-badge](https://raw.githubusercontent.com/superbox-dev/KEBA-KeEnergy-API/main/coverage.svg)
[![CI](https://github.com/superbox-dev/KEBA-KeEnergy-API/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/superbox-dev/KEBA-KeEnergy-API/actions/workflows/ci.yml)
[![Version](https://img.shields.io/pypi/pyversions/keba-keenergy-api.svg)](https://pypi.python.org/pypi/keba-keenergy-api)

[![license-url](https://img.shields.io/pypi/l/keba-keenergy-api.svg)](https://github.com/superbox-dev/KEBA-KeEnergy-API/blob/main/LICENSE)
![Typing: strict](https://img.shields.io/badge/typing-strict-green.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-black)
![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)

# KEBA KeEnergy API

A thin Python wrapper for the KEBA KeEnergy API.

## Getting started

```bash
pip install keba-keenergy-api
```

## Usage

```python
import asyncio

from keba_keyenergy_api import KebaKeEnergyAPI
from keba_keyenergy_api.constants import HeatCircuitOperatingMode


async def main() -> None:
    client = KebaKeEnergyAPI(host="YOUR-IP-OR-HOSTNAME", ssl=True)

    # Get current outdoor temperature
    outdoor_temperature: float = await client.get_outdoor_temperature()

    # Get heat circuit temperature from heat circuit 2
    heat_circuit_temperature: float = await client.heat_circuit.get_temperature(position=2)

    # Enable "day" mode for heat circuit
    await client.heat_circuit.set_operating_mode(mode=HeatCircuitOperatingMode.DAY)


asyncio.run(main())
```

By default, the library creates a new connection to `KEBA KeEnergy API` with each coroutine. If you are calling a large number of coroutines, an `aiohttp ClientSession()` can be used for connection pooling:


```python
import asyncio

from keba_keyenergy_api import KebaKeEnergyAPI
from keba_keyenergy_api.constants import HeatCircuitOperatingMode

from aiohttp import ClientSession

async def main() -> None:
    async with ClientSession() as session:
        client = KebaKeEnergyAPI(host="YOUR-IP-OR-HOSTNAME", session=session, ssl=True)
        ...

asyncio.run(main())
```


### API endpoints


| Endpoint                     | Type    | Description              |
|------------------------------|---------|--------------------------|
| `.get_outdoor_temperature()` | `float` | Get outdoor temperature. |


#### Hot water tank

| Endpoint                   | Type    | Description                                                                          |
|----------------------------|---------|--------------------------------------------------------------------------------------|
| `.get_temperature()`       | `float` | Get temperature.                                                                     |
| `.get_operating_mode()`    | `int`   | Get operating mode as integer (0 is `OFF`, 1 is `AUTO`, 2 is `DAY` and 3 is `NIGHT`. |
| `.set_operating_mode(0)`   | `int`   | Set operating mode.                                                                  |
| `.get_min_temperature()`   | `float` | Get minimum temperature.                                                             |
| `.set_min_temperature(20)` | `float` | Set minimum temperature.                                                             |
| `.get_max_temperature()`   | `float` | Get maximum temperature.                                                             |
| `.set_max_temperature(22)` | `float` | Set maximum temperature.                                                             |

### Heat pump

| Endpoint                               | Type     | Description                                                                 |
|----------------------------------------|----------|-----------------------------------------------------------------------------|
| `.get_status()`                        | `int`    | Get operating mode as integer (0 is `STANDBY`, 1 is `FLOW` and 2 is `AUTO`. |
| `.get_circulation_pump()`              | `float`  | Get circulation pump in percent.                                            |
| `.get_inflow_temperature()`            | `float`  | Get inflow temperature.                                                     |
| `.get_reflux_temperature()`            | `float`  | Get reflux temperature.                                                     |
| `.get_source_input_temperature()`      | `float`  | Get source input temperature.                                               |
| `.get_source_output_temperature()`     | `float`  | Get source output temperature.                                              |
| `.get_compressor_input_temperature()`  | `float`  | Get compressor input temperature.                                           |
| `.get_compressor_output_temperature()` | `float`  | Get compressor output temperature.                                          |
| `.get_compressor()`                    | `float`  | Get compressor in percent.                                                  |
| `.get_high_pressure()`                 | `float`  | Get high pressure.                                                          |
| `.get_low_pressure()`                  | `float`  | Get low pressure.                                                           |

### Heat circuit

| Endpoint                             | Type    | Description                                         |
|--------------------------------------|---------|-----------------------------------------------------|
| `.get_temperature()`                 | `float` | Get temperature.                                    |
| `.get_day_temperature()`             | `float` | Get day temperature.                                |
| `.set_day_temperature(20)`           | `float` | Set day temperature.                                |
| `.get_day_temperature_threshold()`   | `float` | Get day temperature threshold.                      |
| `.get_night_temperature()`           | `float` | Get night temperature.                              |
| `.set_night_temperature(16)`         | `float` | Set night temperature.                              |
| `.get_night_temperature_threshold()` | `float` | Get night temperature threshold.                    |
| `.get_holiday_temperature()`         | `float` | Get holiday temperature.                            |
| `.get_offset_temperature()`          | `float` | Get offset temperature.                             |
| `.set_offset_temperature(2)`         | `float` | Set offset temperature.                             |
| `.get_operating_mode()`              | `int`   | Get operating mode (0 is `OFF` and 3 is `HEAT_UP`). |
| `.set_operating_mode(3)`             | `int`   | Set operating mode.                                 |

## Changelog

The changelog lives in the [CHANGELOG.md](CHANGELOG.md) document. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Contributing

We're happy about your contributions to the project!

You can get started by reading the [CONTRIBUTING.md](CONTRIBUTING.md).

## Donation

We put a lot of time into this project. If you like it, you can support us with a donation.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F2F0KXO6D)