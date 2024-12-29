from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.typing import StateType
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Subscription Monitor sensor from a config entry."""
    subscription = entry.data
    async_add_entities([SubscriptionSensor(subscription)], True)

class SubscriptionSensor(SensorEntity):
    """Representation of a Subscription Monitor sensor."""

    def __init__(self, subscription):
        self._subscription = subscription

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Subscription: {self._subscription['type']}"

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._subscription.get("cost_per_period", "Unknown")

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes."""
        return {
            "Subscription ID": self._subscription["subscription_id"],
            "Service Provider": self._subscription["service_provider"],
            "Notice Period": self._subscription.get("notice_period", "Not specified"),
            "Period": self._subscription.get("period", "None"),
            "Start Date": self._subscription["start_date"],
            "End Date": self._subscription.get("end_date", "No end date"),
            "Remarks": self._subscription.get("remarks", ""),
        }
