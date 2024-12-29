from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN
from datetime import datetime

class SubscriptionMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Subscription Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            user_input["cost_per_period"] = user_input.get("cost_per_period", 0)
            user_input["period"] = user_input.get("period", "none")
            user_input["notice_period"] = user_input.get("notice_period", "")
            user_input["start_date"] = user_input.get("start_date")
            user_input["end_date"] = user_input.get("end_date")
                        

            try:
                float(user_input["cost_per_period"])
                return self.async_create_entry(title=user_input["category"], data=user_input)
            except ValueError:
                errors["cost_per_period"] = "invalid_number"

        data_schema = vol.Schema({
            vol.Required("subscription_id"): str,  
            vol.Optional("cost_per_period", default=0): vol.Coerce(float),
            vol.Optional("period", default="none"): vol.In(["none", "day", "week", "month", "quarter", "year"]),
            vol.Required("start_date"): str,
            vol.Optional("end_date", default="31-12-2100"): str,
            vol.Required("category"): str,
            vol.Optional("type", default=""): str,
            vol.Required("service_provider"): str, 
            vol.Optional("notice_period", default=""): str,  
            vol.Optional("remarks", default=""): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
            