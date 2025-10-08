# PROJECT_BLUEPRINT.md (v2.0)

### Project Name
ha-virtual-devices

### Problem Statement
Complex physical devices (like multi-step dimmers controlled by simple switches) are impossible to integrate cleanly into standard automations, requiring brittle, untestable workarounds.

### Target User Persona
A technically proficient Home Assistant user who wants to abstract away the complexity of non-standard hardware into simple, standard virtual devices.

### Core MVP Feature Set (The Virtual Step-Dimmer)
1.  **Config Flow:** The integration must provide a UI in Home Assistant to create a new "Virtual Step-Dimmer Light". The user will select the physical `switch` entity, the `sensor` entity for power monitoring, and define the brightness levels for each "step".
2.  **Virtual `light` Entity:** The integration will create a new `light` entity in Home Assistant that behaves like a standard dimmable light, with an on/off state and a brightness slider.
3.  **Stateful Logic & Control:** When the brightness of the virtual light is changed, the integration's internal logic will execute the necessary sequence of `switch.toggle` commands to reach the desired step. It will use the power sensor to verify the current state and reconcile any discrepancies.
4.  **Verifiable Logic:** The core state machine and control logic must be covered by a `pytest` suite that runs independently of Home Assistant.

### "Out of Scope" for MVP (The V2 Parking Lot)
* **Room Scene Controller:** The higher-level concept of a "Room" entity that manages scenes and multiple lights is the clear goal for V2, once the foundational device abstraction is complete.
* The Hallway Switch.

### Proposed Tech Stack
* **Platform:** Home Assistant Custom Integration.
* **Distribution:** HACS (Home Assistant Community Store).
* **Language:** Python 3.12.
* **Framework:** We will re-purpose the `appdaemon-aegis` repository under the new name `ha-virtual-devices`.
* **Testing:** `pytest`.
