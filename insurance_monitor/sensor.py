from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Insurance Monitor sensors from a config entry."""
    insurance = config_entry.data
    async_add_entities([InsuranceSensor(insurance)], True)

class InsuranceSensor(SensorEntity):
    def __init__(self, insurance):
        self._insurance = insurance

    @property
    def name(self):
        return f"Insurance {self._insurance['type']}"

    @property
    def state(self):
        """Return the cost per period as the state."""
        return self._insurance.get("cost_per_period", 0)

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "policy_number": self._insurance["policy_number"],
            "period": self._insurance.get("period", "none"),
            "start_date": self._insurance["start_date"],
            "end_date": self._insurance.get("end_date"),
            "type": self._insurance["type"],
            "insurance_company": self._insurance["insurance_company"],
            "remarks": self._insurance.get("remarks", ""),  # Nieuw attribuut voor opmerkingen
        }
