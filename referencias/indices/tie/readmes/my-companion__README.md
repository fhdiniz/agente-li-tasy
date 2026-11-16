# My Companion TIE integrations

## Table of Content
- [Import Files](#import-files)
  - [Conditions](#conditions)
- [Send terms of use](#send-terms-of-use)
  - [Conditions](#conditions-1)
- [Update terms of use](#update-terms-of-use)
  - [Conditions](#conditions-2)

## Import Files

Allows the My Companion application to import teleconsultation files of the chat into Tasy application.

#### Conditions

- Should have GED_ATENDIMENTO repository configured into Tasy in "System Management / Parameters tab / File storage tab / File repository item".
- Should have "Schedule parameters" of "Core Tables Settings" module configured for teleconsultation.

---

## Send terms of use

Allows Tasy application to send and update terms of use of teleconsultation application.

#### Conditions

- Should have "Teleconsultation terms" records in "Web Suite Management / configuration menu / privacy tab" for terms of use and privacy notice.
- Should have "Schedule parameters" of "Core Tables Settings" module configured for teleconsultation.

---

## Update terms of use

Allows Tasy application checks whether new patients (only external access) have accepted the terms of use/privacy notice.

#### Conditions

- Should have "Teleconsultation terms" records in "Web Suite Management / configuration menu / privacy tab" for terms of use and privacy notice.
- Should have "Schedule parameters" of "Core Tables Settings" module configured for teleconsultation.
