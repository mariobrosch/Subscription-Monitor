from homeassistant.components.sensor import SensorEntity
# from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up Subscription Monitor sensors from a config entry."""
    subscription = entry.data
    device_id = f"{DOMAIN}_{subscription['service_provider']}_{subscription['subscription_id']}"
    device_info = DeviceInfo(
        identifiers={(DOMAIN, f"{subscription['service_provider']}_{subscription['subscription_id']}")},
        name=f"Subscription: {subscription['category']} - {subscription['service_provider']}",
        manufacturer=f"mariobrosch",
        model=f"{subscription['category']}-{subscription['service_provider']}-{subscription['type']}",
        sw_version="1.0",
        via_device=(DOMAIN, device_id)
    )
    entities = [
        SubscriptionAttributeSensor(subscription, "subscription_id", device_info),
        SubscriptionAttributeSensor(subscription, "service_provider", device_info),
        SubscriptionAttributeSensor(subscription, "notice_period", device_info),
        SubscriptionAttributeSensor(subscription, "cost_per_period", device_info),
        SubscriptionAttributeSensor(subscription, "period", device_info),
        SubscriptionAttributeSensor(subscription, "start_date", device_info),
        SubscriptionAttributeSensor(subscription, "end_date", device_info),
        SubscriptionAttributeSensor(subscription, "remarks", device_info),
        SubscriptionAttributeSensor(subscription, "category", device_info),
        SubscriptionAttributeSensor(subscription, "type", device_info)
    ]
    async_add_entities(entities, True)

class SubscriptionAttributeSensor(SensorEntity):
    """Representation of a Subscription Monitor attribute sensor."""

    def __init__(self, subscription, attribute, device_info):
        """Initialize the sensor."""
        self._subscription = subscription
        self._attribute = attribute
        self._attr_name = f"{subscription['service_provider']} {subscription['subscription_id']} {attribute.replace('_', ' ').title()}"
        self._attr_unique_id = f"{subscription['service_provider']}-{subscription['subscription_id']}-{attribute}"
        self._attr_entity_id = f"sensor.{subscription['service_provider']}_{subscription['subscription_id']}_{attribute}"
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._subscription.get(self._attribute, "Not specified")

    async def async_set_value(self, value):
        """Set the value of the sensor."""
        self._subscription[self._attribute] = value
        self.async_write_ha_state()
        await self.async_update_device_info()

    async def async_update_device_info(self):
        """Update the device info if a property changes."""
        device_registry = await self.hass.helpers.device_registry.async_get_registry()
        device_entry = device_registry.async_get_device(self._attr_device_info["identifiers"])
        if device_entry:
            device_registry.async_update_device(
                device_entry.id,
                name=f"Subscription: {self._subscription['category']} - {self._subscription['service_provider']}",
                model=f"{self._subscription['category']}-{self._subscription['service_provider']}-{self._subscription['type']}"
            )

