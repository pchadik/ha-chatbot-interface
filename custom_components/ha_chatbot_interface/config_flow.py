import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN, CONF_API_ENDPOINT, CONF_API_KEY, CONF_TEMPERATURE, CONF_TOP_P

#def url_validator(value):
#    return cv.url(value)

#def temperature_validator(value):
#    value = float(value)
#    if 0.1 <= value <= 5.0:
#        return value
#    raise vol.Invalid("Temperature must be between 0.1 and 5.0.")

#def top_p_validator(value):
#    value = float(value)
#    if 0.1 <= value <= 1.0:
#        return value
#    raise vol.Invalid("Top_p must be between 0.1 and 1.0.")

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_ENDPOINT): str,
        vol.Optional(CONF_API_KEY): str,
    }
)

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_TEMPERATURE, default=1.0): float,
        vol.Optional(CONF_TOP_P, default=0.9): float,
    },
    extra=vol.ALLOW_EXTRA
)

class HaChatbotInterfaceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        _LOGGER.debug("async_step_user called with user_input: %s", user_input)
        if user_input is not None:
            # Create the config entry with the provided user input
            return self.async_create_entry(title="Home Assistant Chatbot Interface", data=user_input)

        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)

    async def async_step_import(self, import_data):
        """Handle importing data from configuration.yaml."""
        return await self.async_step_user(import_data)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HaChatbotInterfaceOptionsFlowHandler(config_entry)

class HaChatbotInterfaceOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        _LOGGER.debug("async_step_init called with user_input: %s", user_input)
        if user_input is not None:
            # Update the options and save them to the config entry
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=OPTIONS_SCHEMA)
