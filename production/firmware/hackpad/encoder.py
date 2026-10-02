"""Quadratur-Encoder fuer die nicht benachbarten GPIOs des XIAO RP2040."""

import time

import keypad


class IncrementalEncoder:
    # D8=GPIO2 und D9=GPIO4: rotaryio verlangt auf dem RP2040 Nachbar-GPIOs.
    # keypad scannt im Hintergrund, auch waehrend ein Makro ausgefuehrt wird.
    _TRANSITIONS = (0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0)

    def __init__(self, pin_a, pin_b):
        self._keys = keypad.Keys(
            (pin_a, pin_b), value_when_pressed=False, pull=True,
            interval=0.001, max_events=256, debounce_threshold=1,
        )
        self._position = 0
        self._resync()

    def _resync(self):
        self._keys.reset()
        time.sleep(0.003)
        self._state = 3
        self._steps = 0
        event = self._keys.events.get()
        while event is not None:
            self._state = self._event_state(self._state, event)
            event = self._keys.events.get()

    @staticmethod
    def _event_state(state, event):
        mask = 1 << event.key_number
        if event.pressed:
            return state & ~mask
        return state | mask

    def _update(self, state):
        if state == self._state:
            return
        delta = self._TRANSITIONS[(self._state << 2) | state]
        self._state = state
        if delta == 0:
            self._steps = 0
            return
        self._steps += delta
        if self._steps >= 4:
            self._position += 1
            self._steps -= 4
        elif self._steps <= -4:
            self._position -= 1
            self._steps += 4

    @property
    def position(self):
        events = self._keys.events
        if events.overflowed:
            self._resync()
            return self._position
        state = self._state
        timestamp = None
        event = events.get()
        while event is not None:
            # Zwei im selben Scan geaenderte Kontakte haben keine bekannte
            # Reihenfolge; gemeinsam auswerten statt eine Richtung zu erfinden.
            if timestamp is not None and event.timestamp != timestamp:
                self._update(state)
            timestamp = event.timestamp
            state = self._event_state(state, event)
            event = events.get()
        self._update(state)
        return self._position

    def deinit(self):
        self._keys.deinit()
