from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

class SubscriptionMonitorOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Subscription Monitor."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        try:
            if user_input is not None:
                return self.async_create_entry(title="", data=user_input)

            subscription = self.config_entry.data

            options_schema = vol.Schema({
                vol.Optional("category", default=subscription.get("category", "")): str,
                vol.Optional("type", default=subscription.get("type", "")): str,
                vol.Optional("notice_period", default=subscription.get("notice_period", "")): str,
                vol.Optional("remarks", default=subscription.get("remarks", "")): str,
            })

            return self.async_show_form(step_id="init", data_schema=options_schema)
        except Exception as e:
            _LOGGER.error("Error in options flow: %s", e)
            return self.async_abort(reason="unknown_error")
