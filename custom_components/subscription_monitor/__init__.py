from homeassistant.core import HomeAssistant

DOMAIN = "subscription_monitor"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Subscription Monitor component."""
    # Eventuele globale setup
    hass.data[DOMAIN] = []
    return True
