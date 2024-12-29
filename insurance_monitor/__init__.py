from homeassistant.core import HomeAssistant

DOMAIN = "insurance_monitor"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Insurance Monitor component."""
    # Eventuele globale setup
    hass.data[DOMAIN] = []
    return True
