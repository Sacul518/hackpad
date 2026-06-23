"""Erkennt das verbundene Hackpad (CIRCUITPY-Laufwerk) plattformuebergreifend."""

import os
import sys
import glob


def host_os():
    """Gibt das OS des aktuellen Rechners zurueck: 'mac' | 'windows' | 'linux'."""
    if sys.platform.startswith("darwin"):
        return "mac"
    if sys.platform.startswith("win"):
        return "windows"
    return "linux"


def _candidates():
    plat = host_os()
    if plat == "mac":
        return ["/Volumes/CIRCUITPY"]
    if plat == "linux":
        user = os.environ.get("USER", "")
        paths = []
        paths += glob.glob("/media/%s/CIRCUITPY" % user)
        paths += glob.glob("/run/media/%s/CIRCUITPY" % user)
        paths += glob.glob("/media/CIRCUITPY")
        return paths
    # windows: Laufwerksbuchstaben durchgehen
    out = []
    for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
        root = "%s:\\" % letter
        if os.path.exists(root):
            out.append(root)
    return out


def _is_circuitpy(path):
    """Plausibel ein CIRCUITPY-Laufwerk? (Marker-Datei boot_out.txt)."""
    if not path or not os.path.isdir(path):
        return False
    # macOS/Linux: der Pfad heisst schon CIRCUITPY -> reicht.
    if os.path.basename(path.rstrip("/\\")).upper() == "CIRCUITPY":
        return True
    # Windows: Volume-Marker pruefen.
    return os.path.exists(os.path.join(path, "boot_out.txt"))


def find_circuitpy():
    """Gibt den Pfad zum verbundenen Hackpad zurueck oder None."""
    for path in _candidates():
        if _is_circuitpy(path):
            return path
    return None
