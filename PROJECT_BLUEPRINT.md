# PROJECT_BLUEPRINT.md (v2.1)

### Project Name

ha-virtual-devices

### Problem Statement

Complex physical devices (like multi-step dimmers controlled by simple switches) are impossible to integrate cleanly into standard automations, requiring brittle, untestable workarounds. Furthermore, logic for managing media playback (like contextual playlists) is often scattered across dozens of helpers and scripts, making it unmanageable for non-technical users.

### Target User Persona

A technically proficient Home Assistant user who wants to abstract away the complexity of non-standard hardware and complex scripting into simple, standard, UI-configurable virtual devices.

---

### V1 MVP: The Virtual Step-Dimmer

1.  **Config Flow:** The integration must provide a UI in Home Assistant to create a new "Virtual Step-Dimmer Light". The user will select the physical `switch` entity, the `sensor` entity for power monitoring, and define the brightness levels for each "step".
2.  **Virtual `light` Entity:** The integration will create a new `light` entity in Home Assistant that behaves like a standard dimmable light, with an on/off state and a brightness slider.
3.  **Stateful Logic & Control:** When the brightness of the virtual light is changed, the integration's internal logic will execute the necessary sequence of `switch.toggle` commands to reach the desired step. It will use the power sensor to verify the current state and reconcile any discrepancies.
4.  **Verifiable Logic:** The core state machine and control logic must be covered by a `pytest` suite that runs independently of Home Assistant.

---

### V2 Feature: Virtual Music Context

1.  **Context Options Flow:** An **Options Flow** will be added to the integration to serve as the "Music Context Editor." This UI must be accessible to non-admin family members.
2.  **Editor UI:** The UI will allow users to **Create**, **Delete**, and **Edit** contexts (e.g., "Morning," "Party," "Seasonal").
3.  **Playlist Picker UI:** The "Edit" screen will dynamically fetch the `items` from `sensor.sonos_favorites` (showing friendly names) and present them in a UI that allows adding them to a context list.
4.  **Weighting:** The UI will support weighting by allowing a user to add the same favorite to a context _multiple times_.
5.  **Playback Service:** The integration will register a new service, `virtual_devices.play_context`, which accepts one or more context names and handles the weighted, "don't-repeat" random playback logic.

---

### Future Virtual Devices (V3+ Parking Lot)

- **Room Scene Controller:** The higher-level concept of a "Room" entity that manages scenes and multiple lights.
- **The Hallway Switch:** A stateful toggle to solve the original hallway problem.
- **"Better Radio" / Room Awareness:** Auto-pausing music, mixing podcasts, etc. This is explicitly out of scope until V2 is stable.

### Proposed Tech Stack

- **Platform:** Home Assistant Custom Integration.
- **Distribution:** HACS (Home Assistant Community Store).
- **Language:** Python 3.13
- **Development Environment:** VS Code Dev Container using `ghcr.io/home-assistant/devcontainer:addons`.
- **Framework:** We will re-purpose the `appdaemon-aegis` repository under the new name `ha-virtual-devices`.
- **Testing:** `pytest`.
