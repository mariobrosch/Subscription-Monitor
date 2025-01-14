from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Subscription Monitor."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {"entities": []}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Subscription Monitor from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {"entities": []}

    hass.data[DOMAIN][entry.entry_id] = entry.data

    entry.add_update_listener(async_update_options)

    # Forward the entry to the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry):
    """Update options."""
    # Update the stored data
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Notify sensors to update their state
    for entity in hass.data[DOMAIN]["entities"]:
        if entity.entry_id == entry.entry_id:
            entity.async_schedule_update_ha_state(True)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
