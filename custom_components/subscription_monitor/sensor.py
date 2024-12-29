from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Subscription Monitor sensors from a config entry."""
    subscription = entry.data
    async_add_entities([SubscriptionSensor(subscription)], True)

class SubscriptionSensor(SensorEntity):

    def __init__(self, subscription):
        """Initialize the sensor."""
        self._subscription = subscription
        # We are grouping the subscriptions by category, this makes it easier to group them automatically in the integration by for example streaming or insurances
        self._attr_name = f"Subscription: {subscription['category']} - {subscription["service_provider"]}"
        self._attr_unique_id = subscription["subscription_id"] + subscription["service_provider"]

    @property
    def state(self):
        """Return the state of the sensor."""
        # We can only display one value as state, so we just return one of the required fields and that's the id
        return self._subscription.get("subscription_id", "Unknown")

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
            "Category": self._subscription.get("category", "Not specified"),
            "Type": self._subscription.get("type", "Not specified"),
        }
    
