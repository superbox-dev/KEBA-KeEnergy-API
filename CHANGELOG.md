# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.10.0] - 2023-10-23

## Added

- Added heat pump state "inflow"
- Added `heat_circuit.set_holiday_temperature()` endpoint

## [1.9.0] - 2023-10-23

## Added

- Add **AWAY** and **PARTY** to heat circuit operating mode

## [1.8.1] - 2023-10-22

## Added

- Add APIError exception when can't convert value to human readable value.

## Changed

- Allow set operating mode in lower and uppercase.

## [1.8.0] - 2023-10-20

### Added

- Added `read_values_grouped_by_section()` endpoint.
- Added `attributes` to `read_values()` response. 


## [1.7.0] - 2023-10-19

### Added

- Added `hot_water_tank.get_lower_limit_temperature()` endpoint.
- Added `hot_water_tank.get_upper_limit_temperature()` endpoint.

## [1.6.2] - 2023-10-18

### Fixed

- Refactor `KebaKeEnergyAPI()` class for better mocking with pytest.

## [1.6.1] - 2023-10-17

### Fixed

- `InvalidJsonError` Class no inherit from `APIError` Class.

### Added

## [1.6.0] - 2023-10-14

- Added `heat_pump.get_name()` to read the **heat pump** name.
- Added `heat_circuit.get_name()` to read the **heat circuit** name.
- Added `human_readable` attribute to `read_values()` to get a human-readable name and not a number as response e.g. for `hot_water_tank.get_operating_mode()`

## [1.5.0] - 2023-10-13

### Added

- Added `get_system_info()` to read all system information.

## [1.4.3] - 2023-10-13

### Fixed

- Fixed error when mixing endpoints with and without position.

## [1.4.2] - 2023-10-13

### Added

- Get the device url with `client.device_url`.

## [1.4.1] - 2023-10-11

### Changed

- Downgrade aiohttp to version 3.8.5 (for home assistant compatibility).

## [1.4.0] - 2023-10-11

### Added

- Added `get_device_info()` to read all device information e.g. serial number as `dict`.

## [1.3.0] - 2023-10-10

### Added

- Added `get_number_of_hot_water_tanks()` to read number of hot water tanks.
- Added `get_number_of_heat_pumps()` to read number of heat pumps.
- Added `get_number_of_heating_circuits()` to read number of heating circuits.
- Added automatic set of position numbers for `read_values()` dependent on hardware. 

## [1.2.0] - 2023-10-09

### Added

- Added `read_values()` to read multiple values with one http request.
- Added `write_values()` to write multiple values with one http request.

## [1.1.0] - 2023-10-08

### Added

- Added device information endpoint for e.g. serial number
- Added ssl support for aiohttp.

## [1.0.0] - 2023-10-07

Initial release