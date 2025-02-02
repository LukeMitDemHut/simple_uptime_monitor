# config_flow.py
import voluptuous as vol
import logging

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_URL

from .const import DOMAIN, CONF_INTERVAL

_LOGGER = logging.getLogger(__name__)

# Define the schema for the configuration input
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default="Google"): str,
    vol.Required(CONF_URL, default="https://www.google.com"): str,
    vol.Required(CONF_INTERVAL, default=30): int,
})

class SimpleUptimeMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the Simple Uptime Monitor integration."""
    
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial configuration step."""
        if user_input is not None:
            # Create the config entry with the user-provided data
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA
        )
