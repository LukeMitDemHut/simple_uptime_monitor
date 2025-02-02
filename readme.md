# Simple Uptime Monitor

This is a custom integration for Home Assistant that monitors the uptime and response time of a specified URLs.

## What This Integration Does
The Simple Uptime Monitor integration allows you to:
- Monitor the availability (up or down) of specified URLs.
- Track the response time of the URLs in milliseconds.
- Access detailed metrics such as status codes, error messages, response size, and failure counts.
- All monitoring is done directly on your local Home Assistant instance, giving you complete control over your data and the monitoring process.

## Benefits Over a Cloud-Hosted Uptime Monitor
- Privacy and Control: Unlike cloud-based uptime monitoring services, this integration runs locally on your Home Assistant instance. This means your monitoring data (including URLs and response times) never leaves your home network, ensuring full control over your data.
- No Subscription Fees: Many cloud-based uptime monitoring services require a subscription for advanced features or higher monitoring frequencies. With this integration, you can monitor as many URLs as you want without worrying about subscription costs or limitations.
- Customization: Being integrated into Home Assistant, you can easily customize how and when you receive notifications or take automated actions based on the status of your URLs.
- Offline Monitoring: Since it runs locally, the monitoring continues to work even if you don't have internet access. This can be useful for monitoring local services or devices that may not be accessible from outside your network.

## Installation

### Manual Installation

1. Download the `simple_uptime_monitor` directory and place it in your Home Assistant `custom_components` directory.
2. Restart Home Assistant.

### Installation via HACS

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Go to HACS in the Home Assistant web interface.
3. Click on the `Integrations` tab.
4. Click the three dots in the top right corner and select `Custom repositories`.
5. Add the repository URL: `https://github.com/LukeMitDemHut/simple_uptime_monitor` and select `Integration` as the category.
6. Find `Simple Uptime Monitor` in the HACS integrations list and install it.
7. Restart Home Assistant.

### Installation via Home Assistant My Link
Click the following Button and add the integration to your HomeAssistant.

[![Open your Home Assistant instance and show the add integration dialog with a specific integration pre-selected.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=LukeMitDemHut&repository=simple_uptime_monitor&category=integration)

## Configuration

1. Go to the Home Assistant web interface.
2. Navigate to `Configuration` > `Integrations`.
3. Click the `+ Add Integration` button.
4. Search for `Simple Uptime Monitor` and follow the setup instructions.

## Options

- **Name**: The name of the sensor.
- **URL**: The URL to monitor.
- **Interval**: The interval in seconds between checks.

## Sensors

This integration creates two sensors:
- **Status Sensor**: Indicates whether the URL is up or down and provides additional metrics such as status code, error message, last checked timestamp, failure count, and response size.
- **Response Time Sensor**: Shows the response time of the URL in milliseconds.

## Example Configuration

```yaml
simple_uptime_monitor:
  name: Google
  url: https://www.google.com
  interval: 30
```

## Attributes

### Status Sensor

- `url`: The monitored URL.
- `status_code`: The HTTP status code of the response.
- `error`: Any error message encountered during the check.
- `last_checked`: The timestamp of the last check.
- `failure_count`: The number of consecutive failures.
- `response_size`: The size of the response in bytes.

### Response Time Sensor

- `url`: The monitored URL.
- `response_time`: The response time in milliseconds.

## License

This project is licensed under the MIT License.
