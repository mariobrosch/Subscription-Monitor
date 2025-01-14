from homeassistant.components.sensor import SensorEntity
# from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up Subscription Monitor sensors from a config entry."""
    subscription = dict(entry.data)  # Create a new dictionary from entry data
    subscription["entry_id"] = entry.entry_id  # Add entry_id to subscription data
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
        SubscriptionAttributeSensor(subscription, "subscription_id", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "service_provider", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "notice_period", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "cost_per_period", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "period", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "start_date", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "end_date", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "remarks", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "category", device_info, entry.entry_id),
        SubscriptionAttributeSensor(subscription, "type", device_info, entry.entry_id)
    ]
    async_add_entities(entities, True)

    # Register entities in hass.data
    hass.data[DOMAIN]["entities"].extend(entities)

class SubscriptionAttributeSensor(SensorEntity):
    """Representation of a Subscription Monitor attribute sensor."""

    def __init__(self, subscription, attribute, device_info, entry_id):
        """Initialize the sensor."""
        self._subscription = subscription
        self._attribute = attribute
        self._attr_name = f"{subscription['service_provider']} {subscription['subscription_id']} {attribute.replace('_', ' ').title()}"
        self._attr_unique_id = f"{subscription['service_provider']}-{subscription['subscription_id']}-{attribute}"
        self._attr_entity_id = f"sensor.{subscription['service_provider']}_{subscription['subscription_id']}_{attribute}"
        self._attr_device_info = device_info
        self.entry_id = entry_id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.hass.data[DOMAIN][self._subscription["entry_id"]].get(self._attribute, "Not specified")

