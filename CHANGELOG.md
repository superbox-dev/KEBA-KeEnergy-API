# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.12.6] - 2024-03-27

### Fixed

- Fix missing heat request state `OUTDOOR_TEMPERATURE_OFF`

## [1.12.5] - 2024-02-25

### Changed

- Support Python 3.12

## [1.12.4] - 2024-01-30

### Changed

- Bump aiohttp to 3.9.4

## [1.12.3] - 2023-12-08

### Changed

- Bump aiohttp to 3.9.1
- Bump aioresponses to 0.7.6

## [1.12.2] - 2023-11-19

### Changed

- Rename `HeatCircuitOperatingMode.AWAY` to `HeatCircuitOperatingMode.HOLIDAY`.

## [1.12.1] - 2023-11-19

### Changed

- Rename endpoint `get_offset_temperture()` to `get_temperture_offset()`.

## [1.12.0] - 2023-11-18

### Added

- Add `system.get_operation_mode()` endpoint.
- Add `system.set_operation_mode()` endpoint.
- Add `heat_pump.get_operation_mode()` endpoint.
- Add `heat_pump.set_operation_mode()` endpoint.
- Add `heat_circuit.get_external_cool_request()` endpoint.
- Add `heat_circuit.get_external_heat_request()` endpoint.

### Changed

- Convert attributes keys to lower case.
- Merge options and devices endpoint to system endpoint.
- Rename `read_values()` to `read_data()`
- Rename `write_values()` to `write_data()`
- Rename `heat_pump.get_status()` to `heat_pump.get_state()`

## [1.11.1] - 2023-10-25

### Fixed

- Fix response keys from `read_values_grouped_by_section()`.

## [1.11.0] - 2023-10-25

### Added

- Add `heat_pump.get_heat_request()` endpoint.
- Add `heat_circuit.get_heat_request()` endpoint.
- Add `hot_water_tank.get_heat_request()` endpoint.

## [1.10.1] - 2023-10-24

### Changed 

- Refactor `SystemPrefix` enum variables.

## [1.10.0] - 2023-10-23

### Added

- Add heat pump state "inflow"
- Add `heat_circuit.set_holiday_temperature()` endpoint

## [1.9.0] - 2023-10-23

### Added

- Add **AWAY** and **PARTY** to heat circuit operating mode

## [1.8.1] - 2023-10-22

### Added

- Add APIError exception when can't convert value to human readable value.

### Changed

- Allow set operating mode in lower and uppercase.

## [1.8.0] - 2023-10-20

### Added

- Add `read_values_grouped_by_section()` endpoint.
- Add `attributes` to `read_values()` response. 


## [1.7.0] - 2023-10-19

### Added

- Add `hot_water_tank.get_lower_limit_temperature()` endpoint.
- Add `hot_water_tank.get_upper_limit_temperature()` endpoint.

## [1.6.2] - 2023-10-18

### Fixed

- Refactor `KebaKeEnergyAPI()` class for better mocking with pytest.

## [1.6.1] - 2023-10-17

### Fixed

- `InvalidJsonError` Class no inherit from `APIError` Class.

### Added

## [1.6.0] - 2023-10-14

- Add `heat_pump.get_name()` to read the **heat pump** name.
- Add `heat_circuit.get_name()` to read the **heat circuit** name.
- Add `human_readable` attribute to `read_values()` to get a human-readable name and not a number as response e.g. for `hot_water_tank.get_operating_mode()`

## [1.5.0] - 2023-10-13

### Added

- Add `get_system_info()` to read all system information.

## [1.4.3] - 2023-10-13

### Fixed

- Fix error when mixing endpoints with and without position.

## [1.4.2] - 2023-10-13

### Added

- Get the device url with `client.device_url`.

## [1.4.1] - 2023-10-11

### Changed

- Downgrade aiohttp to version 3.8.5 (for home assistant compatibility).

## [1.4.0] - 2023-10-11

### Added

- Add `get_device_info()` to read all device information e.g. serial number as `dict`.

## [1.3.0] - 2023-10-10

### Added

- Add `get_number_of_hot_water_tanks()` to read number of hot water tanks.
- Add `get_number_of_heat_pumps()` to read number of heat pumps.
- Add `get_number_of_heating_circuits()` to read number of heating circuits.
- Add automatic set of position numbers for `read_values()` dependent on hardware. 

## [1.2.0] - 2023-10-09

### Added

- Add `read_values()` to read multiple values with one http request.
- Add `write_values()` to write multiple values with one http request.

## [1.1.0] - 2023-10-08

### Added

- Add device information endpoint for e.g. serial number
- Add ssl support for aiohttp.

## [1.0.0] - 2023-10-07

Initial release
