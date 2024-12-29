from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Subscription Monitor sensors from a config entry."""
    subscription = entry.data
    device_id = f"{DOMAIN}_{subscription['subscription_id']}"
    device_info = DeviceInfo(
        identifiers={(DOMAIN, subscription['subscription_id'])},
        name=f"Subscription: {subscription['category']} - {subscription['service_provider']}",
        manufacturer=subscription['service_provider'],
        model=f"{subscription['category']}-{subscription['type']}",
        sw_version="1.0",
        via_device=(DOMAIN, device_id)
    )
    entities = [
        SubscriptionAttributeSensor(subscription, "subscription_id", device_info),
        SubscriptionAttributeSensor(subscription, "service_provider", device_info),
        SubscriptionAttributeSensor(subscription, "notice_period", device_info),
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
        self._attr_name = f"Subscription {attribute.replace('_', ' ').title()}"
        self._attr_unique_id = f"{subscription['subscription_id']}-{attribute}"
        self._attr_device_info = device_info

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._subscription.get(self._attribute, "Not specified")

