"""Constants for the Virtual Step-Dimmer integration."""

DOMAIN = "virtual_step_dimmer"

# Config Flow
CONF_SWITCH_ENTITY = "switch_entity"
CONF_SENSOR_ENTITY = "sensor_entity"
CONF_BRIGHTNESS_STEPS = "brightness_steps"
CONF_TOGGLE_DELAY_SEC = "toggle_delay_sec"
CONF_SETTLING_DELAY_SEC = "settling_delay_sec"

# Defaults
DEFAULT_TOGGLE_DELAY_SEC = 0.5
DEFAULT_SETTLING_DELAY_SEC = 2
SETTLING_DELAY_SEC = 2  # This is also used in tests

# Misc
LIGHT_BRIGHTNESS_MAX = 255
