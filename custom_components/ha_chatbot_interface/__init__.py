"""Custom chatbot component for Home Assistant."""
from .const import DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, DOMAIN)
    )
    return True