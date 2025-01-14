from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import ServiceCall, callback

from .const import DOMAIN, SERVICE_UPDATE_SUBSCRIPTION

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up Subscription Monitor sensors from a config entry."""
    # ...existing code...

    async def handle_update_subscription(call: ServiceCall) -> None:
        """Handle the service call."""
        entity_id = call.data.get(ATTR_ENTITY_ID)
        value = call.data.get("value")

        if not entity_id or not value:
            return

        target_entities = [
            entity for entity in entities 
            if entity.entity_id == entity_id
        ]

        for entity in target_entities:
            await entity.async_set_value(value)

    # Register the service
    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_SUBSCRIPTION,
        handle_update_subscription
    )

    async_add_entities(entities, True)

class SubscriptionAttributeSensor(SensorEntity):
    """Representation of a Subscription Monitor attribute sensor."""
    
    # ...existing code...

    @property
    def device_class(self):
        """Return the device class."""
        if self._attribute == "cost_per_period":
            return SensorDeviceClass.MONETARY
        elif self._attribute in ["start_date", "end_date"]:
            return SensorDeviceClass.TIMESTAMP
        return None

    async def async_set_value(self, value):
        """Update the sensor value."""
        self._subscription[self._attribute] = value
        self.async_write_ha_state()
        
        # Update configuration entry
        new_data = dict(self.hass.config_entries.async_get_entry(
            self._subscription["entry_id"]
        ).data)
        new_data[self._attribute] = value
        self.hass.config_entries.async_update_entry(
            entry_id=self._subscription["entry_id"],
            data=new_data
        )
        
        await self.async_update_device_info()
