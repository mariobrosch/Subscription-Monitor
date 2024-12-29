from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class SubscriptionMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Subscription Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Vul standaardwaarden in als optionele velden niet zijn ingevuld
            user_input["cost_per_period"] = user_input.get("cost_per_period", 0)
            user_input["period"] = user_input.get("period", "none")
            user_input["notice_period"] = user_input.get("notice_period", "")

            try:
                # Controleer of kosten een geldig getal zijn
                float(user_input["cost_per_period"])
                return self.async_create_entry(title=user_input["type"], data=user_input)
            except ValueError:
                errors["cost_per_period"] = "invalid_number"

        # Formulier om gegevens in te vullen
        data_schema = vol.Schema({
            vol.Required("subscription_id"): str,  # Vervangen door subscription_id
            vol.Optional("cost_per_period", default=0): vol.Coerce(float),
            vol.Optional("period", default="none"): vol.In(["none", "day", "week", "month", "quarter", "year"]),
            vol.Required("start_date"): str,
            vol.Optional("end_date"): str,
            vol.Required("type"): str,
            vol.Required("service_provider"): str,  # Dienstverlener
            vol.Optional("notice_period", default=""): str,  # Opzegtermijn
            vol.Optional("remarks"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
