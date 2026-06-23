"""Konfigurator-GUI (CustomTkinter) -- Layout nach Lucas' PDF.

Links:  OLED-Vorschau, 3x3-Tastenraster (1-9) + Encoder-Info, Profil-Selektor.
Rechts: gewaehlte Taste, Ziel-OS, Editor mit Tabs (Kombi / Text & Script / Media).
Oben:   Verbunden-Indikator, Host-OS, Software-Version.
Unten:  "Aufs Hackpad speichern".
"""

import customtkinter as ctk

from . import config_io, device, osmap, keynames
from . import script_parser as sp

APP_VERSION = "0.1"

ACCENT = "#2563eb"
OK_GREEN = "#16a34a"
OFF_GRAY = "#6b7280"

# Tastatur-Layout fuer den Kombi-Tab (Anzeige-Text, kanonischer Name).
_NUMS = [(str(i), str(i)) for i in range(1, 10)] + [("0", "0")]
_ROW1 = list("QWERTYUIOP")
_ROW2 = list("ASDFGHJKL")
_ROW3 = list("ZXCVBNM")
_SPECIAL = [
    ("Enter", "ENTER"), ("Tab", "TAB"), ("Esc", "ESCAPE"),
    ("Space", "SPACEBAR"), ("Backsp", "BACKSPACE"), ("Del", "DELETE"),
    ("<-", "LEFT_ARROW"), ("->", "RIGHT_ARROW"),
    ("Up", "UP_ARROW"), ("Down", "DOWN_ARROW"),
]
_MODS = [("GUI"), ("CONTROL"), ("ALT"), ("SHIFT")]
_MEDIA = [
    ("Play/Pause", "PLAY_PAUSE"), ("Vol +", "VOLUME_UP"), ("Vol -", "VOLUME_DOWN"),
    ("Mute", "MUTE"), ("Next", "NEXT_TRACK"), ("Prev", "PREV_TRACK"),
    ("Stop", "STOP"),
]


class HackpadApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Hackpad Konfigurator")
        self.geometry("1140x720")
        self.minsize(1000, 640)

        self.config_data = config_io.load_local()
        self.profile_idx = 0
        self.key_idx = 0
        self.device_path = None

        # Kombi-Editor-Status
        self.sel_mods = set()
        self.sel_main = None
        self._mod_buttons = {}
        self._mainkey_buttons = {}
        self.media_choice = None
        self._media_buttons = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_topbar()
        self._build_main()
        self._build_bottom()

        self._refresh_profiles()
        self._select_key(0)
        self._poll_connection()

    # ===================================================================
    # Top bar
    # ===================================================================
    def _build_topbar(self):
        bar = ctk.CTkFrame(self, height=48, corner_radius=0)
        bar.grid(row=0, column=0, sticky="ew")
        self.conn_dot = ctk.CTkLabel(bar, text="●", text_color=OFF_GRAY,
                                     font=("", 18))
        self.conn_dot.pack(side="left", padx=(14, 4), pady=8)
        self.conn_label = ctk.CTkLabel(bar, text="Hackpad getrennt")
        self.conn_label.pack(side="left", pady=8)

        ctk.CTkLabel(bar, text="Hackpad Konfigurator",
                     font=("", 16, "bold")).pack(side="left", padx=24)

        ctk.CTkLabel(bar, text="v%s" % APP_VERSION,
                     text_color=OFF_GRAY).pack(side="right", padx=14)
        self.host_label = ctk.CTkLabel(
            bar, text="Dieser PC: %s" % device.host_os(), text_color=OFF_GRAY)
        self.host_label.pack(side="right", padx=8)

    # ===================================================================
    # Main: left (device) + right (editor)
    # ===================================================================
    def _build_main(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        main.grid_columnconfigure(0, weight=0)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)
        self._build_left(main)
        self._build_right(main)

    def _build_left(self, parent):
        left = ctk.CTkFrame(parent, width=320)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        left.grid_propagate(False)

        # OLED-Vorschau
        oled = ctk.CTkFrame(left, fg_color="#0b0f1a", corner_radius=8,
                            height=70, border_width=2, border_color="#1e293b")
        oled.pack(fill="x", padx=14, pady=(14, 10))
        oled.pack_propagate(False)
        self.oled_title = ctk.CTkLabel(oled, text="Hackpad",
                                       text_color="#38bdf8",
                                       font=("Courier", 13, "bold"))
        self.oled_title.pack(anchor="w", padx=10, pady=(8, 0))
        self.oled_line = ctk.CTkLabel(oled, text="> Profil 1",
                                      text_color="#7dd3fc",
                                      font=("Courier", 12))
        self.oled_line.pack(anchor="w", padx=10)

        # 3x3-Tastenraster
        grid = ctk.CTkFrame(left, fg_color="transparent")
        grid.pack(padx=14, pady=6)
        self.key_buttons = []
        for i in range(9):
            r, c = divmod(i, 3)
            b = ctk.CTkButton(grid, text=str(i + 1), width=84, height=64,
                              command=lambda i=i: self._select_key(i))
            b.grid(row=r, column=c, padx=4, pady=4)
            self.key_buttons.append(b)

        # Encoder-Info
        ctk.CTkLabel(left, text="○ RE  =  Profil wechseln",
                     text_color=OFF_GRAY).pack(pady=(2, 8))

        # Profil-Selektor
        ctk.CTkLabel(left, text="Profile", anchor="w",
                     font=("", 13, "bold")).pack(fill="x", padx=14)
        self.profile_bar = ctk.CTkFrame(left, fg_color="transparent")
        self.profile_bar.pack(fill="x", padx=14, pady=(2, 6))

        rename = ctk.CTkFrame(left, fg_color="transparent")
        rename.pack(fill="x", padx=14, pady=(0, 6))
        self.name_entry = ctk.CTkEntry(rename, placeholder_text="Profilname")
        self.name_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(rename, text="OK", width=40,
                      command=self._rename_profile).pack(side="left", padx=(6, 0))

        self.os_menu = ctk.CTkOptionMenu(
            left, values=list(osmap.OSES), command=self._on_os_change)
        self.os_menu.pack(fill="x", padx=14, pady=(0, 12))

    def _build_right(self, parent):
        right = ctk.CTkFrame(parent)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        self.key_header = ctk.CTkLabel(right, text="Taste 1",
                                       font=("", 18, "bold"))
        self.key_header.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 0))

        labelrow = ctk.CTkFrame(right, fg_color="transparent")
        labelrow.grid(row=1, column=0, sticky="ew", padx=16, pady=8)
        ctk.CTkLabel(labelrow, text="Bezeichnung (OLED/App):").pack(side="left")
        self.label_entry = ctk.CTkEntry(labelrow, width=200)
        self.label_entry.pack(side="left", padx=8)

        self.tabs = ctk.CTkTabview(right)
        self.tabs.grid(row=2, column=0, sticky="nsew", padx=16, pady=8)
        self.tabs.add("Kombi")
        self.tabs.add("Text & Script")
        self.tabs.add("Media")
        self._build_tab_kombi(self.tabs.tab("Kombi"))
        self._build_tab_script(self.tabs.tab("Text & Script"))
        self._build_tab_media(self.tabs.tab("Media"))

        apply_row = ctk.CTkFrame(right, fg_color="transparent")
        apply_row.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        ctk.CTkButton(apply_row, text="Auf Taste übernehmen",
                      fg_color=ACCENT, command=self._apply_action).pack(side="left")
        self.editor_status = ctk.CTkLabel(apply_row, text="", text_color=OFF_GRAY)
        self.editor_status.pack(side="left", padx=12)

    # -- Kombi-Tab -------------------------------------------------------
    def _build_tab_kombi(self, tab):
        ctk.CTkLabel(tab, text="Modifier + eine Taste wählen:").pack(
            anchor="w", pady=(6, 4))
        modrow = ctk.CTkFrame(tab, fg_color="transparent")
        modrow.pack(anchor="w")
        for mod in _MODS:
            b = ctk.CTkButton(modrow, text=mod, width=80,
                              fg_color="gray30",
                              command=lambda m=mod: self._toggle_mod(m))
            b.pack(side="left", padx=3)
            self._mod_buttons[mod] = b

        kb = ctk.CTkScrollableFrame(tab, height=230)
        kb.pack(fill="both", expand=True, pady=8)
        self._add_key_row(kb, [(n, n) for n in [str(i) for i in range(1, 10)] + ["0"]])
        self._add_key_row(kb, [(c, c) for c in _ROW1])
        self._add_key_row(kb, [(c, c) for c in _ROW2])
        self._add_key_row(kb, [(c, c) for c in _ROW3])
        self._add_key_row(kb, _SPECIAL)
        self._add_key_row(kb, [("F%d" % i, "F%d" % i) for i in range(1, 13)])

        self.combo_preview = ctk.CTkLabel(tab, text="Kombi: (leer)",
                                          text_color="#7dd3fc")
        self.combo_preview.pack(anchor="w", pady=4)

    def _add_key_row(self, parent, items):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", pady=2)
        for text, name in items:
            b = ctk.CTkButton(row, text=text, width=46, height=30,
                              fg_color="gray25",
                              command=lambda n=name: self._set_main(n))
            b.pack(side="left", padx=2)
            self._mainkey_buttons[name] = b

    def _toggle_mod(self, mod):
        if mod in self.sel_mods:
            self.sel_mods.discard(mod)
            self._mod_buttons[mod].configure(fg_color="gray30")
        else:
            self.sel_mods.add(mod)
            self._mod_buttons[mod].configure(fg_color=ACCENT)
        self._update_combo_preview()

    def _set_main(self, name):
        if self.sel_main and self.sel_main in self._mainkey_buttons:
            self._mainkey_buttons[self.sel_main].configure(fg_color="gray25")
        if self.sel_main == name:           # nochmal klicken = abwaehlen
            self.sel_main = None
        else:
            self.sel_main = name
            self._mainkey_buttons[name].configure(fg_color=ACCENT)
        self._update_combo_preview()

    def _current_combo_keys(self):
        order = ["GUI", "CONTROL", "ALT", "SHIFT"]
        keys = [m for m in order if m in self.sel_mods]
        if self.sel_main:
            keys.append(self.sel_main)
        return keys

    def _update_combo_preview(self):
        keys = self._current_combo_keys()
        if not keys:
            self.combo_preview.configure(text="Kombi: (leer)")
            return
        os_name = self.os_menu.get()
        shown = [osmap.modifier_label(k, os_name) for k in keys]
        self.combo_preview.configure(text="Kombi: " + " + ".join(shown))

    # -- Text & Script-Tab ----------------------------------------------
    def _build_tab_script(self, tab):
        ctk.CTkLabel(
            tab,
            text='Syntax:  (Return) (Cmd+C)  |  "schnell tippen"  |  \'einfügen\'',
            text_color=OFF_GRAY, anchor="w").pack(fill="x", pady=(6, 2))
        self.script_box = ctk.CTkTextbox(tab, height=160)
        self.script_box.pack(fill="both", expand=True)
        self.script_box.bind("<KeyRelease>", lambda e: self._preview_script())
        self.script_preview = ctk.CTkLabel(tab, text="", text_color="#7dd3fc",
                                           anchor="w", justify="left",
                                           wraplength=560)
        self.script_preview.pack(fill="x", pady=4)

    def _preview_script(self):
        text = self.script_box.get("1.0", "end").strip()
        if not text:
            self.script_preview.configure(text="", text_color="#7dd3fc")
            return
        try:
            action = sp.parse(text)
            self.script_preview.configure(text="OK ✓", text_color=OK_GREEN)
            return action
        except sp.ParseError as e:
            self.script_preview.configure(text="Fehler: %s" % e,
                                          text_color="#f87171")
            return None

    # -- Media-Tab -------------------------------------------------------
    def _build_tab_media(self, tab):
        ctk.CTkLabel(tab, text="Media-/Lautstärke-Taste:").pack(
            anchor="w", pady=(6, 6))
        grid = ctk.CTkFrame(tab, fg_color="transparent")
        grid.pack(anchor="w")
        for idx, (text, code) in enumerate(_MEDIA):
            r, c = divmod(idx, 4)
            b = ctk.CTkButton(grid, text=text, width=110, fg_color="gray25",
                              command=lambda code=code: self._set_media(code))
            b.grid(row=r, column=c, padx=4, pady=4)
            self._media_buttons[code] = b

    def _set_media(self, code):
        for c, b in self._media_buttons.items():
            b.configure(fg_color=ACCENT if c == code else "gray25")
        self.media_choice = code

    # ===================================================================
    # Bottom
    # ===================================================================
    def _build_bottom(self):
        bar = ctk.CTkFrame(self, height=52, corner_radius=0)
        bar.grid(row=2, column=0, sticky="ew")
        ctk.CTkButton(bar, text="↓  Aufs Hackpad speichern",
                      fg_color=OK_GREEN, hover_color="#15803d", height=34,
                      command=self._save).pack(side="left", padx=14, pady=8)
        self.save_status = ctk.CTkLabel(bar, text="", text_color=OFF_GRAY)
        self.save_status.pack(side="left", padx=8)

    # ===================================================================
    # Profile / Tasten
    # ===================================================================
    @property
    def profile(self):
        return self.config_data["profiles"][self.profile_idx]

    def _refresh_profiles(self):
        for w in self.profile_bar.winfo_children():
            w.destroy()
        for i, p in enumerate(self.config_data["profiles"]):
            sel = i == self.profile_idx
            b = ctk.CTkButton(
                self.profile_bar, text=p["name"], width=70, height=28,
                fg_color=ACCENT if sel else "gray30",
                command=lambda i=i: self._select_profile(i))
            b.pack(side="left", padx=2)
        ctk.CTkButton(self.profile_bar, text="+", width=34, height=28,
                      fg_color="gray20",
                      command=self._add_profile).pack(side="left", padx=2)
        # Name + OS-Felder fuellen
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, self.profile["name"])
        self.os_menu.set(self.profile.get("target_os", "mac"))
        self._refresh_keys()
        self._update_oled()

    def _refresh_keys(self):
        default = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        for i, b in enumerate(self.key_buttons):
            key = self.profile["keys"][i]
            label = key.get("label") or str(i + 1)
            sel = i == self.key_idx
            b.configure(text=label, fg_color=ACCENT if sel else default,
                        border_width=2 if sel else 0,
                        border_color="#93c5fd")

    def _update_oled(self):
        total = len(self.config_data["profiles"])
        self.oled_title.configure(text="Hackpad")
        self.oled_line.configure(
            text="> %s  (%d/%d)" % (self.profile["name"],
                                    self.profile_idx + 1, total))

    def _select_profile(self, i):
        self.profile_idx = i
        self._refresh_profiles()
        self._select_key(self.key_idx)

    def _add_profile(self):
        name = "Profil %d" % (len(self.config_data["profiles"]) + 1)
        self.config_data["profiles"].append(
            config_io.empty_profile(name, self.os_menu.get()))
        self._select_profile(len(self.config_data["profiles"]) - 1)

    def _rename_profile(self):
        name = self.name_entry.get().strip()
        if name:
            self.profile["name"] = name
            self._refresh_profiles()

    def _on_os_change(self, value):
        self.profile["target_os"] = value
        self._update_combo_preview()

    def _select_key(self, i):
        self.key_idx = i
        self.key_header.configure(text="Taste %d" % (i + 1))
        self._refresh_keys()
        self._load_key_into_editor()

    # ===================================================================
    # Editor laden / anwenden
    # ===================================================================
    def _clear_editor(self):
        self.sel_mods.clear()
        for b in self._mod_buttons.values():
            b.configure(fg_color="gray30")
        if self.sel_main and self.sel_main in self._mainkey_buttons:
            self._mainkey_buttons[self.sel_main].configure(fg_color="gray25")
        self.sel_main = None
        self._update_combo_preview()
        self.script_box.delete("1.0", "end")
        self._preview_script()
        for b in self._media_buttons.values():
            b.configure(fg_color="gray25")
        self.media_choice = None
        self.editor_status.configure(text="")

    def _load_key_into_editor(self):
        self._clear_editor()
        key = self.profile["keys"][self.key_idx]
        self.label_entry.delete(0, "end")
        self.label_entry.insert(0, key.get("label", ""))
        action = key.get("action")
        if not action:
            self.tabs.set("Kombi")
            return
        kind = action.get("type")
        if kind in ("combo", "key"):
            keys = action.get("keys", [action.get("key")]) if kind == "combo" \
                else [action.get("key")]
            for k in keys:
                if k in ("GUI", "CONTROL", "ALT", "SHIFT"):
                    self._toggle_mod(k)
                elif k:
                    self._set_main(k)
            self.tabs.set("Kombi")
        elif kind == "media":
            self._set_media(action.get("code"))
            self.tabs.set("Media")
        else:  # string / sequence
            self.script_box.insert("1.0", _action_to_script(action))
            self._preview_script()
            self.tabs.set("Text & Script")

    def _apply_action(self):
        tab = self.tabs.get()
        action = None
        if tab == "Kombi":
            keys = self._current_combo_keys()
            if keys:
                action = {"type": "combo", "keys": keys} if len(keys) > 1 \
                    else {"type": "key", "key": keys[0]}
        elif tab == "Media":
            if self.media_choice:
                action = {"type": "media", "code": self.media_choice}
        else:
            action = self._preview_script()
            if action is None and self.script_box.get("1.0", "end").strip():
                self.editor_status.configure(text="Script-Fehler — nicht "
                                                  "übernommen",
                                             text_color="#f87171")
                return
        key = self.profile["keys"][self.key_idx]
        key["label"] = self.label_entry.get().strip()
        key["action"] = action
        self._refresh_keys()
        self.editor_status.configure(
            text="✓ Taste %d gespeichert" % (self.key_idx + 1),
            text_color=OK_GREEN)

    # ===================================================================
    # Speichern + Verbindung
    # ===================================================================
    def _save(self):
        self.config_data["active_profile"] = self.profile_idx
        try:
            wrote = config_io.save_to_device(self.config_data, self.device_path)
        except OSError as e:
            self.save_status.configure(text="Fehler: %s" % e,
                                       text_color="#f87171")
            return
        if wrote:
            self.save_status.configure(
                text="✓ Auf Hackpad geschrieben (lädt automatisch neu)",
                text_color=OK_GREEN)
        else:
            self.save_status.configure(
                text="Lokal gespeichert (kein Hackpad verbunden)",
                text_color=OFF_GRAY)

    def _poll_connection(self):
        path = device.find_circuitpy()
        if path != self.device_path:
            self.device_path = path
            if path:
                self.conn_dot.configure(text_color=OK_GREEN)
                self.conn_label.configure(text="Hackpad verbunden")
            else:
                self.conn_dot.configure(text_color=OFF_GRAY)
                self.conn_label.configure(text="Hackpad getrennt")
        self.after(2000, self._poll_connection)


def _action_to_script(action):
    """Aktion -> Script-Text (best effort), zum Wieder-Bearbeiten."""
    kind = action.get("type")
    if kind == "string":
        return '"%s"' % action.get("text", "")
    if kind == "key":
        return "(%s)" % action.get("key", "")
    if kind == "combo":
        return "(%s)" % "+".join(action.get("keys", []))
    if kind == "sequence":
        return " ".join(_action_to_script(s) for s in action.get("steps", []))
    return ""


def run():
    HackpadApp().mainloop()
