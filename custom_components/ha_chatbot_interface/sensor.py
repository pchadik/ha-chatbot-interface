import aiohttp
import logging
import voluptuous as vol
import json

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA
# from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_API_KEY

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)

CONF_API_ENDPOINT = 'api_endpoint'

DOMAIN = 'ha_chatbot_interface'

# Generation parameters
# Reference: https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
params = {
    'max_new_tokens': 50,
    'do_sample': True,
    'temperature': 1.99,
    'top_p': 0.18,
    'typical_p': 1,
    'repetition_penalty': 1.05,
    'encoder_repetition_penalty': 1.0,
    'top_k': 30,
    'min_length': 0,
    'no_repeat_ngram_size': 0,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 10,
    'early_stopping': True,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_ENDPOINT): cv.url,
        vol.Required(CONF_API_KEY): cv.string,
    }
)

async def async_setup(hass, config):
    """Empty setup function."""
    return True

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Empty setup function (no longer used)."""
    pass
    
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    api_endpoint = config[CONF_API_ENDPOINT]
    api_key = config[CONF_API_KEY]

    session = async_get_clientsession(hass)

    chatbot = Chatbot(session, api_endpoint, api_key)

    sensor = ChatbotSensor(chatbot)

    async def handle_send_message(call):
        message = call.data.get('message')
        _LOGGER.debug("Sending message to chatbot: %s", message)
        await sensor.async_send_message(message)

    hass.services.async_register(DOMAIN, 'send_message', handle_send_message)

    async_add_entities([sensor])

# Remove the async_send_message function outside of any class

class Chatbot:
    def __init__(self, session, api_endpoint, api_key=None):
        self._session = session
        self._api_endpoint = api_endpoint
        self._api_key = api_key

    async def send_message(self, message, options):
        headers = {'Content-Type': 'application/json'}
        if self._api_key:
            headers['Authorization'] = f'Bearer {self._api_key}'

        params.update(options)

        payload = {
            "data": [
                message,
                params['max_new_tokens'],
                params['do_sample'],
                params['temperature'],
                params['top_p'],
                params['typical_p'],
                params['repetition_penalty'],
                params['encoder_repetition_penalty'],
                params['top_k'],
                params['min_length'],
                params['no_repeat_ngram_size'],
                params['num_beams'],
                params['penalty_alpha'],
                params['length_penalty'],
                params['early_stopping'],
            ]}

        try:
            async with self._session.post(self._api_endpoint, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    response_data = await resp.json()
                    return response_data['data'][0]
                else:
                    _LOGGER.error(f'Error {resp.status}: {await resp.text()}')
                    return None
        except aiohttp.ClientError as err:
            _LOGGER.error(f'Error while sending message to chatbot: {err}')
            return None

class ChatbotSensor(Entity):
    def __init__(self, chatbot, entry):
        self._chatbot = chatbot
        self._entry = entry
        self._state = None

    @property
    def name(self):
        return "Chatbot"

    @property
    def state(self):
        return self._state

    @property
    def should_poll(self):
        return False

    async def async_send_message(self, message):
        _LOGGER.debug("API endpoint: %s", self._chatbot._api_endpoint)
        _LOGGER.debug("Sending message to chatbot: %s", message)
        response = await self._chatbot.send_message(message, self._entry.options)
        self._state = response
        _LOGGER.debug("Received response from chatbot: %s", response)
        await self.async_update_ha_state()