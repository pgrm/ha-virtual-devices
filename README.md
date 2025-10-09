# Home Assistant Virtual Devices

A Home Assistant custom integration for creating smart virtual devices to abstract away the complexity of non-standard hardware.

## The Problem

Many smart home automations become brittle and hard to maintain because they have to deal with the quirks of specific hardware (like multi-step dimmers controlled by simple switches). This project aims to solve that by providing a set of "virtual devices" that present a clean, standard interface to Home Assistant while hiding the complex logic internally.

## V1 Goal: The Virtual Step-Dimmer

The initial focus of this project is to create a single virtual device:

- **Virtual Step-Dimmer Light:** A `light` entity that can be configured from the UI. It will control a physical switch-based step-dimmer by sending the correct sequence of on/off commands and using a power sensor to verify the current brightness level.

This will allow users to treat their complex step-dimmers as simple, standard dimmable lights in all their automations.

## Roadmap

The project is currently in the initial setup phase. The roadmap is structured around delivering the **Virtual Step-Dimmer** as the first virtual device.

- [ ] **Phase 1: Project Scoping & Setup**

  - [x] Define MVP and technical stack (`PROJECT_BLUEPRINT.md`).
  - [x] Set up repository and license.
  - [x] Set up development tooling (`Poetry`, `Makefile`, `ruff`).
  - [ ] Configure CI/CD pipeline with GitHub Actions.
  - [ ] Configure VS Code Dev Container for local development.

- [ ] **Phase 2: MVP Implementation (Virtual Step-Dimmer)**

  - [ ] Implement basic Config Flow UI.
  - [ ] Create the virtual `light` entity.
  - [ ] Develop and test the core state machine logic.
  - [ ] Integrate the logic into the entity to provide full functionality.

- [ ] **Phase 3: V2 and Beyond**
  - [ ] **Room Scene Controller:** A higher-level entity for managing scenes across multiple devices.
  - [ ] **Stateful Toggle Switch:** The original "Hallway Switch" problem.

## Contributing

This project is in the early stages of development. Contributions and ideas are welcome!
