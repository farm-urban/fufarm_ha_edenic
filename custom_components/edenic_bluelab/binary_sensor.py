"""Binary sensor platform for the Edenic Bluelab integration (individual alarms)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ALARM_MODE_ALL,
    ALARM_MODE_INDIVIDUAL,
    ALARMS,
    CONF_ALARM_MODE,
    DEFAULT_ALARM_MODE,
    DOMAIN,
)
from .coordinator import EdenicCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .const import AlarmDefinition


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up one binary sensor per alarm/lockout, per device."""
    coordinator: EdenicCoordinator = hass.data[DOMAIN][entry.entry_id]
    alarm_mode = entry.options.get(CONF_ALARM_MODE, DEFAULT_ALARM_MODE)

    if alarm_mode not in (ALARM_MODE_INDIVIDUAL, ALARM_MODE_ALL):
        return

    entities = [
        EdenicAlarmBinarySensor(coordinator, device, alarm)
        for device in coordinator.devices
        for alarm in ALARMS
    ]
    async_add_entities(entities)


class EdenicAlarmBinarySensor(CoordinatorEntity[EdenicCoordinator], BinarySensorEntity):
    """Represents a single alarm or lockout attribute for a device."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(
        self,
        coordinator: EdenicCoordinator,
        device: dict[str, str],
        alarm_def: AlarmDefinition,
    ) -> None:
        """Initialize the binary sensor for one alarm definition."""
        super().__init__(coordinator)
        self._device_id = device["id"]
        self._alarm_def = alarm_def
        self._attr_name = f"{alarm_def.name} {device['label']}"
        self._attr_unique_id = f"{self._device_id}_{alarm_def.key.replace('.', '_')}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=device["label"],
            manufacturer="Bluelab",
            model="Pro Controller",
        )

    @property
    def is_on(self) -> bool | None:
        """Return True if this alarm/lockout is currently active."""
        data = self.coordinator.data.get(self._device_id)
        if data is None:
            return None
        return data.alarms.get(self._alarm_def.key, False)
