# Home Assistant Virtual Devices

A Home Assistant custom integration for creating smart virtual devices to abstract away the complexity of non-standard hardware.

## The Problem

Many smart home automations become brittle and hard to maintain because they have to deal with the quirks of specific hardware (like multi-step dimmers controlled by simple switches). This project aims to solve that by providing a set of "virtual devices" that present a clean, standard interface to Home Assistant while hiding the complex logic internally.

## V1 Goal: The Virtual Step-Dimmer

The initial focus of this project is to create a single virtual device:

* **Virtual Step-Dimmer Light:** A `light` entity that can be configured from the UI. It will control a physical switch-based step-dimmer by sending the correct sequence of on/off commands and using a power sensor to verify the current brightness level.

This will allow users to treat their complex step-dimmers as simple, standard dimmable lights in all their automations.

## Contributing

This project is in the early stages of development. Contributions and ideas are welcome!
