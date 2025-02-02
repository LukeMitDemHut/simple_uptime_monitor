# sensor.py
import logging
import time
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN, CONF_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors based on user configuration."""
    # Read configuration parameters from the entry
    sensor_name = config_entry.data.get("name")
    url = config_entry.data.get("url")
    interval = config_entry.data.get("interval")

    # Create two sensors: one for the status and one for the response time
    status_sensor = URLStatusSensor(sensor_name, url, config_entry.entry_id)
    response_time_sensor = URLResponseTimeSensor(sensor_name, url, config_entry.entry_id)

    async_add_entities([status_sensor, response_time_sensor])

    async def update_sensors(now):
        _LOGGER.debug("Pinging %s", url)
        start_time = time.monotonic()
        error_message = None
        status_code = None
        response_size = None
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        status_code = response.status
                        is_up = response.status == 200
                        status_sensor.set_status(is_up, status_code=status_code)
                        elapsed = time.monotonic() - start_time
                        response_time_sensor.set_response_time(round(elapsed * 1000, 2))

                        # Get the response size from Content-Length header, if available
                        response_size = response.content_length
                        if response_size is None:
                            # If no Content-Length header, calculate the size by reading the content
                            response_size = len(await response.read())
                        
                        status_sensor.set_response_size(response_size)

        except Exception as e:
            _LOGGER.error("Error pinging %s: %s", url, e)
            is_up = False
            error_message = str(e)
            status_sensor.set_status(is_up, status_code=status_code, error=error_message)
            response_time_sensor.set_response_time(None)

        # Set the last checked timestamp
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        status_sensor.set_last_checked(now_str)

        # Update the states of the sensors
        status_sensor.async_schedule_update_ha_state()
        response_time_sensor.async_schedule_update_ha_state()

    # Update sensors immediately upon setup
    await update_sensors(None)

    # Register the callback based on the configured update interval
    async_track_time_interval(hass, update_sensors, timedelta(seconds=interval))

class URLStatusSensor(Entity):
    """Sensor that shows the status (up/down) and additional metrics."""

    def __init__(self, name, url, config_entry_id):
        self._name = f"{name} Status"
        self._url = url
        self._is_up = False
        self._status_code = None
        self._error = None
        self._last_checked = None
        self._response_size = None
        self._failure_count = 0
        self._config_entry_id = config_entry_id
        self._unique_id = f"{config_entry_id}_status"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return "up" if self._is_up else "down"

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def icon(self):
        return "mdi:cloud-check" if self._is_up else "mdi:cloud-alert"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config_entry_id)},
            "name": self._name,
            "manufacturer": "Simple Uptime Monitor",
            "model": "Status Sensor",
        }

    def set_status(self, is_up, status_code=None, error=None):
        self._is_up = is_up
        self._status_code = status_code
        self._error = error
        if not is_up:
            self._failure_count += 1
        else:
            self._failure_count = 0

    def set_last_checked(self, timestamp):
        self._last_checked = timestamp

    def set_response_size(self, size):
        self._response_size = size

    @property
    def extra_state_attributes(self):
        return {
            "url": self._url,
            "status_code": self._status_code,
            "error": self._error,
            "last_checked": self._last_checked,
            "failure_count": self._failure_count,
            "response_size": self._response_size,
        }


class URLResponseTimeSensor(Entity):
    """Sensor that shows the response time in milliseconds."""

    def __init__(self, name, url, config_entry_id):
        self._name = f"{name} Uptime Monitor"
        self._url = url
        self._response_time = None
        self._config_entry_id = config_entry_id
        self._unique_id = f"{config_entry_id}_response_time"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._response_time

    @property
    def unit_of_measurement(self):
        return "ms"

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config_entry_id)},
            "name": self._name,
            "manufacturer": "Simple Uptime Monitor",
            "model": "Response Time Sensor",
        }

    def set_response_time(self, response_time):
        self._response_time = response_time

    @property
    def extra_state_attributes(self):
        return {
            "url": self._url
        }
