# Edenic Bluelab for Home Assistant

A custom Home Assistant integration for monitoring Edenic Bluelab Pro Controller devices.

This integration polls the Edenic cloud API and exposes live nutrient monitoring data as Home Assistant sensors, including:

- pH
- Temperature
- EC (electrical conductivity)
- Alarm summary
- Individual alarm/lockout binary sensors

It is designed to work as a standard custom component and supports device selection, alarm mode configuration, and polling interval adjustment.

## Features

- Live telemetry sensors for each configured Bluelab device
- Binary sensors for active alarm and lockout states
- Device-level alarm summary sensor
- Per-device grouping in Home Assistant
- Configurable alarm display mode:
  - individual
  - summary
  - all
- Adjustable polling interval

## Requirements

- Home Assistant instance
- Edenic organisation key and API key
- One or more labelled Edenic Bluelab Pro Controller devices

> Only devices with a label in the Edenic system are selectable in the integration setup flow.

## Installation

### Option 1: Manual install

1. Copy the `custom_components/edenic_bluelab` directory into your Home Assistant configuration directory under `custom_components/`.
2. Restart Home Assistant.
3. Go to Settings > Devices & Services > Add Integration.
4. Search for `Edenic Bluelab` and complete the setup flow.

### Option 2: HACS

1. Add this repository as a custom repository in HACS.
2. Install the integration from HACS.
3. Restart Home Assistant.
4. Add the integration from the Home Assistant UI.

## Configuration

During setup, you will be asked to provide:

- Organisation key
- API key
- Device selection

After setup, you can adjust options via:

- Settings > Devices & Services > Edenic Bluelab > Configure

Available options include:

- Alarm mode
  - `individual`: expose one binary sensor per alarm/lockout
  - `summary`: expose the alarm summary sensor only
  - `all`: expose both summary and individual alarm sensors
- Scan interval (seconds)

## Entities created

### Sensors

For each selected device:

- `pH <device label>`
- `Temperature <device label>`
- `EC <device label>`
- `Alarms <device label>` (summary sensor)

### Binary sensors

When the alarm mode includes individual or all alarms, a binary sensor is created for each configured device alarm or lockout, for example:

- EC low alarm
- EC high alarm
- pH low alarm
- pH high alarm
- Temperature low alarm
- Temperature high alarm
- Other lockout
- Ineffective control lockout
- Low EC lockout
- Normally closed lockout
- Normally open lockout

## Troubleshooting

### No devices found

This usually means:

- the organisation key is incorrect
- the API key is invalid
- no labelled Bluelab devices are associated with the org

### Authentication errors

Verify that the provided API key is valid and still active in Edenic.

### Entities missing after changing alarm mode

The integration cleans up stale entity registrations when options are changed, so Home Assistant will remove entities that are no longer expected.

## Development

This project includes support files for a HA custom component development workflow. The integration uses:

- `config_flow.py` for setup and options UI
- `coordinator.py` for polling and data refresh
- `sensor.py` for telemetry and summary sensors
- `binary_sensor.py` for alarm binary sensors
- `api.py` for Edenic API calls

## License

This project is licensed under the MIT license. See the `LICENSE` file for details.

## Project status

This component is intended for Home Assistant custom integrations and may be updated over time to match API or feature changes from Edenic.

