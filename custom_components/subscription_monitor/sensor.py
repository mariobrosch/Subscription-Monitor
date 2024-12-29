from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, DEVICE_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Subscription Monitor sensors from a config entry."""
    subscription = entry.data
    async_add_entities([SubscriptionDeviceSensor(subscription)], True)

class SubscriptionDeviceSensor(SensorEntity):
    """Representation of a Subscription Monitor device."""

    def __init__(self, subscription):
        """Initialize the sensor."""
        self._subscription = subscription
        self._attr_name = f"Subscription: {subscription['type']}"
        self._attr_unique_id = subscription["subscription_id"]

    @property
    def state(self):
        """Return the state of the sensor."""
        # Gebruik een belangrijk attribuut als hoofdstatus
        return self._subscription.get("cost_per_period", "Unknown")

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        # Zorg ervoor dat alle ingevoerde gegevens hier worden weergegeven
        return {
            "Subscription ID": self._subscription.get("subscription_id", "Not specified"),
            "Service Provider": self._subscription.get("service_provider", "Not specified"),
            "Notice Period": self._subscription.get("notice_period", "Not specified"),
            "Period": self._subscription.get("period", "Not specified"),
            "Start Date": self._subscription.get("start_date", "Not specified"),
            "End Date": self._subscription.get("end_date", "Not specified"),
            "Remarks": self._subscription.get("remarks", "Not specified"),
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the subscription."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._subscription["subscription_id"])},
            name=self._attr_name,
            manufacturer="Subscription Monitor",
            model=DEVICE_NAME,
        )
