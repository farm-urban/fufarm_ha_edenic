"""Data update coordinator for the Edenic Bluelab integration."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EdenicApiError, EdenicAuthError, get_device_attributes, get_telemetry
from .const import DEFAULT_SCAN_INTERVAL

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOG = logging.getLogger(__name__)


@dataclass
class EdenicDeviceData:
    """Latest telemetry and alarm data for a single device."""

    telemetry: dict[str, Any]
    alarms: dict[str, bool]


class EdenicCoordinator(DataUpdateCoordinator[dict[str, EdenicDeviceData]]):
    """Polls the Edenic API for all configured devices on an interval."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        devices: list[dict[str, str]],
        scan_interval: int | None = None,
    ) -> None:
        """Initialize the Edenic data coordinator."""
        super().__init__(
            hass,
            _LOG,
            name=f"{entry.title} coordinator",
            update_interval=timedelta(seconds=scan_interval)
            if scan_interval
            else DEFAULT_SCAN_INTERVAL,
        )
        self.api_key: str = entry.data["api_key"]
        self.devices = devices

    async def _async_update_data(self) -> dict[str, EdenicDeviceData]:
        result: dict[str, EdenicDeviceData] = {}
        for device in self.devices:
            device_id = device["id"]
            try:
                telemetry = await self.hass.async_add_executor_job(
                    get_telemetry, device_id, self.api_key
                )
                alarms = await self.hass.async_add_executor_job(
                    get_device_attributes, device_id, self.api_key
                )
            except EdenicAuthError as err:
                message = "Edenic API key is no longer valid"
                raise ConfigEntryAuthFailed(message) from err
            except EdenicApiError as err:
                message = f"Error updating {device['label']}: {err}"
                raise UpdateFailed(message) from err
            result[device_id] = EdenicDeviceData(telemetry=telemetry, alarms=alarms)
        return result
