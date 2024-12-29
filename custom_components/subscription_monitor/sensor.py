from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Subscription Monitor sensors from a config entry."""
    insurance = config_entry.data
    async_add_entities([SubscriptionSensor(insurance)], True)

class SubscriptionSensor(SensorEntity):
    def __init__(self, subscription):
        self._subscription = subscription

    @property
    def name(self):
        return f"Subscription {self._subscription['type']}"

    @property
    def state(self):
        """Return the cost per period as the state."""
        return self._subscription.get("cost_per_period", 0)

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "subscription_id": self._subscription["subscription_id"],
            "period": self._subscription.get("period", "none"),
            "start_date": self._subscription["start_date"],
            "end_date": self._subscription.get("end_date"),
            "type": self._subscription["type"],
            "company": self._subscription["company"],
            "remarks": self._subscription.get("remarks", ""), 
            "who": self._subscription.get("who", ""), 
        }
