"""Encoder-Signalfolgen pruefen; ersetzt keinen Test mit dem echten Drehknopf."""

from collections import deque
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class EventQueue:
    def __init__(self):
        self.items = deque()
        self.overflowed = False

    def get(self):
        return self.items.popleft() if self.items else None


class Keys:
    initial_state = 3

    def __init__(self, pins, **kwargs):
        self.events = EventQueue()
        self.deinitialized = False

    def reset(self):
        self.events.items.clear()
        self.events.overflowed = False
        for bit in range(2):
            if not self.initial_state & (1 << bit):
                self.events.items.append(SimpleNamespace(
                    key_number=bit, pressed=True, timestamp=0))

    def deinit(self):
        self.deinitialized = True


spec = importlib.util.spec_from_file_location(
    "encoder", ROOT / "firmware/hackpad/encoder.py")
encoder_module = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"keypad": SimpleNamespace(Keys=Keys)}):
    spec.loader.exec_module(encoder_module)


class EncoderTests(unittest.TestCase):
    def setUp(self):
        Keys.initial_state = 3
        self.sleep = patch.object(encoder_module.time, "sleep", return_value=None)
        self.sleep.start()
        self.addCleanup(self.sleep.stop)
        self.encoder = encoder_module.IncrementalEncoder("D8", "D9")
        self.state = 3
        self.timestamp = 0

    def feed(self, states):
        for state in states:
            self.timestamp += 1
            for bit in range(2):
                if (state ^ self.state) & (1 << bit):
                    self.encoder._keys.events.items.append(SimpleNamespace(
                        key_number=bit, pressed=not bool(state & (1 << bit)),
                        timestamp=self.timestamp))
            self.state = state
        return self.encoder.position

    def test_idle(self):
        self.assertEqual(self.feed([]), 0)
        self.assertEqual(self.feed([3, 3]), 0)

    def test_both_directions(self):
        self.assertEqual(self.feed([1, 0, 2, 3]), 1)
        self.assertEqual(self.feed([2, 0, 1, 3]), 0)
        self.assertEqual(self.feed([2, 0, 1, 3]), -1)

    def test_partial_rotation(self):
        self.assertEqual(self.feed([1, 0, 2]), 0)
        self.assertEqual(self.feed([3]), 1)

    def test_contact_bounce(self):
        self.assertEqual(self.feed([1, 3, 1, 0, 1, 0, 2, 3, 2, 3]), 1)

    def test_reverse_mid_step(self):
        self.assertEqual(self.feed([1, 0, 1, 3]), 0)
        self.assertEqual(self.feed([2, 0, 1, 3]), -1)

    def test_simultaneous_changes(self):
        self.assertEqual(self.feed([0, 3, 0, 3]), 0)
        self.assertEqual(self.feed([1, 0, 2, 3]), 1)

    def test_missing_transition_discards_partial_step(self):
        self.assertEqual(self.feed([1, 2, 3]), 0)
        self.assertEqual(self.feed([1, 0, 2, 3]), 1)

    def test_startup_all_contact_states(self):
        cycle = [3, 1, 0, 2]
        for index, state in enumerate(cycle):
            with self.subTest(state=state):
                Keys.initial_state = state
                self.encoder = encoder_module.IncrementalEncoder("D8", "D9")
                self.state = state
                self.assertEqual(self.encoder.position, 0)
                states = [cycle[(index + n) % 4] for n in range(1, 5)]
                self.assertEqual(self.feed(states), 1)

    def test_overflow_resynchronizes_without_phantom_rotation(self):
        self.assertEqual(self.feed([1, 0, 2, 3]), 1)
        self.feed([1])
        Keys.initial_state = 0
        self.encoder._keys.events.overflowed = True
        self.assertEqual(self.encoder.position, 1)
        self.state = 0
        self.assertEqual(self.feed([2, 3, 1, 0]), 2)

    def test_queued_rotation(self):
        self.assertEqual(self.feed([1, 0, 2, 3] * 50), 50)
        self.assertEqual(self.feed([2, 0, 1, 3] * 50), 0)

    def test_release_pins(self):
        self.encoder.deinit()
        self.assertTrue(self.encoder._keys.deinitialized)

    def test_production_matches_source(self):
        for name in ("code.py", "hackpad/encoder.py"):
            self.assertEqual((ROOT / "firmware" / name).read_bytes(),
                             (ROOT / "production/firmware" / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
