"""Laden/Speichern der config.json (lokal + aufs Hackpad)."""

import json
import os

CONFIG_NAME = "config.json"

# Lokale Arbeitskopie neben der App.
_LOCAL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "last_config.json")


def default_config():
    return {
        "version": 1,
        "active_profile": 0,
        "profiles": [_empty_profile("Profil 1")],
    }


def _empty_profile(name, target_os="mac"):
    return {
        "name": name,
        "target_os": target_os,
        "keys": [{"label": "", "action": None} for _ in range(9)],
    }


def empty_profile(name, target_os="mac"):
    return _empty_profile(name, target_os)


def load_local():
    """Letzte lokale Arbeitskopie laden, sonst Default."""
    try:
        with open(_LOCAL, "r") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default_config()


def load_from(path):
    with open(os.path.join(path, CONFIG_NAME), "r") as f:
        return json.load(f)


def _write(path, config):
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


def save_local(config):
    _write(_LOCAL, config)


def save_to_device(config, device_path):
    """Schreibt config.json aufs Hackpad UND speichert lokal. device_path=None
    -> nur lokal."""
    save_local(config)
    if device_path:
        _write(os.path.join(device_path, CONFIG_NAME), config)
        return True
    return False
