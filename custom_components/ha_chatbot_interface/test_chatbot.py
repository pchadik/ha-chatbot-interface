import pytest
from unittest.mock import AsyncMock, MagicMock

from homeassistant.components.ha_chatbot_interface.sensor import Chatbot

@pytest.mark.asyncio
async def test_async_send_message():
    session = MagicMock()
    api_endpoint = 'http://192.168.1.XXX:XXXX/api/chatbot'
    api_key = 'your_api_key_here'

    chatbot = Chatbot(session, api_endpoint, api_key)

    message = "What's the weather like today?"
    expected_response = {'response': 'It is sunny and 75 degrees.'}

    session.post.return_value.__aenter__.return_value.json = AsyncMock(return_value=expected_response)
    session.post.return_value.__aenter__.return_value.status = 200

    response = await chatbot.async_send_message(message)

    assert response == expected_response['response']
