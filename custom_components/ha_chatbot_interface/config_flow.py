import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_API_ENDPOINT, CONF_API_KEY

# Define the schema for the user step
USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_ENDPOINT): cv.url,
        vol.Required(CONF_API_KEY): cv.string,
    }
)

# Define the schema for the options step
OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional("temperature", default=1.0): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=5.0)),
        vol.Optional("top_p", default=0.9): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=1.0)),
    }
)

class HaChatbotInterfaceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Create the config entry with the provided user input
            return self.async_create_entry(title="HA Chatbot Interface", data=user_input)

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
        if user_input is not None:
            # Update the options and save them to the config entry
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=OPTIONS_SCHEMA)
