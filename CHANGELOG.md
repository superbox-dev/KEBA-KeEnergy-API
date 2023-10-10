# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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