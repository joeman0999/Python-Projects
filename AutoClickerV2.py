#!/usr/bin/env python3
import threading
import time
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional

import tkinter as tk
from tkinter import simpledialog, messagebox
from pynput.mouse import Controller as MouseController, Button as MouseButton, Listener as MouseListener
from pynput.keyboard import Controller as KeyController, Key, KeyCode, Listener as KeyListener

# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Action:
    """Represents one repeating action: either mouse or keyboard."""
    kind: str  # 'mouse' or 'keyboard'
    target: Union[MouseButton, Key, KeyCode]
    interval: float
    jitter: Tuple[float, float] = (0.0, 0.0)

    def next_delay(self) -> float:
        return self.interval + random.uniform(*self.jitter)

@dataclass
class TimedEvent:
    """A single user action event captured during recording."""
    timestamp: float
    kind: str       # 'mouse' or 'keyboard'
    target: Union[MouseButton, Key, KeyCode]

@dataclass
class Macro:
    """Sequence of timed events to replay."""
    events: List[TimedEvent] = field(default_factory=list)

    def play(self, mouse: MouseController, keyboard: KeyController) -> None:
        if not self.events:
            return
        start = self.events[0].timestamp
        for evt in self.events:
            delay = evt.timestamp - start
            time.sleep(delay)
            if evt.kind == 'mouse':
                mouse.click(evt.target)
            else:
                keyboard.press(evt.target)
                keyboard.release(evt.target)
            start = evt.timestamp

# ─────────────────────────────────────────────────────────────────────────────
class AutoClicker(threading.Thread):
    def __init__(self, actions: List[Action], macro: Optional[Macro] = None):
        super().__init__(daemon=True)
        self._actions = actions
        self._macro = macro
        self._running = threading.Event()
        self._stop = threading.Event()
        self._mouse = MouseController()
        self._keyboard = KeyController()

    def run(self) -> None:
        while not self._stop.is_set():
            if self._running.is_set():
                if self._macro:
                    self._macro.play(self._mouse, self._keyboard)
                    self._macro = None
                    self._running.clear()
                else:
                    for action in list(self._actions):
                        if action.kind == 'mouse':
                            self._mouse.click(action.target)
                        else:
                            self._keyboard.press(action.target)
                            self._keyboard.release(action.target)
                        time.sleep(action.next_delay())
            else:
                time.sleep(0.1)

    def start_clicking(self) -> None:
        self._running.set()

    def stop_clicking(self) -> None:
        self._running.clear()

    def exit(self) -> None:
        self._stop.set()
        self._running.clear()

    def add_action(self, action: Action) -> None:
        self._actions.append(action)

    def remove_action(self, index: int) -> None:
        if 0 <= index < len(self._actions):
            del self._actions[index]

    def load_macro(self, macro: Macro) -> None:
        self._macro = macro
        self.start_clicking()

# ─────────────────────────────────────────────────────────────────────────────
class Recorder:
    def __init__(self):
        self.events: List[TimedEvent] = []
        self._start_time: Optional[float] = None
        self._mouse_listener = MouseListener(on_click=self._on_click)
        self._key_listener = KeyListener(on_press=self._on_key)

    def _on_click(self, x, y, button, pressed):
        if pressed:
            now = time.time()
            if self._start_time is None:
                self._start_time = now
            self.events.append(TimedEvent(now - self._start_time, 'mouse', button))

    def _on_key(self, key):
        now = time.time()
        if self._start_time is None:
            self._start_time = now
        if isinstance(key, KeyCode) or isinstance(key, Key):
            self.events.append(TimedEvent(now - self._start_time, 'keyboard', key))

    def start(self) -> None:
        self.events.clear()
        self._start_time = None
        self._mouse_listener.start()
        self._key_listener.start()

    def stop(self) -> Macro:
        self._mouse_listener.stop()
        self._key_listener.stop()
        return Macro(self.events.copy())

# ─────────────────────────────────────────────────────────────────────────────
class ClickerGUI:
    def __init__(self, root: tk.Tk, clicker: AutoClicker, recorder: Recorder):
        self.root = root
        self.clicker = clicker
        self.recorder = recorder
        
        # Actions list
        self.actions_listbox = tk.Listbox(root, width=60)
        self.actions_listbox.pack(padx=10, pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Action", command=self.add_action).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Remove Action",command=self.remove_action).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Start",       command=clicker.start_clicking).grid(row=1,column=0, padx=5,pady=5)
        tk.Button(btn_frame, text="Stop",        command=clicker.stop_clicking).grid(row=1,column=1, padx=5,pady=5)
        tk.Button(btn_frame, text="Record",      command=self.start_record).grid(row=2,column=0, pady=5)
        tk.Button(btn_frame, text="Stop Record", command=self.stop_record).grid(row=2,column=1,pady=5)
        tk.Button(btn_frame, text="Exit",        command=self.on_exit).grid(row=3, column=0, columnspan=2, pady=5)

        self.refresh_actions()

    def refresh_actions(self) -> None:
        self.actions_listbox.delete(0, tk.END)
        for i, act in enumerate(self.clicker._actions):
            self.actions_listbox.insert(tk.END, f"[{i}] {act.kind:>8} {act.target!s:<10} interval={act.interval:.2f}±{act.jitter}")

    def add_action(self) -> None:
        kind = simpledialog.askstring("Action Kind", "Enter 'mouse' or 'keyboard':")
        if kind not in ('mouse', 'keyboard'):
            return messagebox.showerror("Error","Invalid kind—must be 'mouse' or 'keyboard'.")
        tgt = simpledialog.askstring("Target",
            "Mouse: 'left'/'right'; Keyboard: single char or special key name"
        )
        if not tgt:
            return
        if kind == 'mouse':
            try:
                btn = MouseButton[tgt.upper()]
            except KeyError:
                return messagebox.showerror("Error",f"Unknown mouse button '{tgt}'")
            target = btn
        else:
            if len(tgt) == 1:
                target = KeyCode(char=tgt)
            else:
                try:
                    target = getattr(Key, tgt.lower())
                except AttributeError:
                    return messagebox.showerror("Error",f"Unknown key '{tgt}'")
        interval = simpledialog.askfloat("Interval","Seconds between actions:",minvalue=0.0)
        jitter_low = simpledialog.askfloat("Jitter Min","Min jitter seconds:",minvalue=0.0,initialvalue=0.0)
        jitter_high = simpledialog.askfloat("Jitter Max","Max jitter seconds:",minvalue=jitter_low,initialvalue=0.0)
        action = Action(kind=kind, target=target, interval=interval, jitter=(jitter_low,jitter_high))
        self.clicker.add_action(action)
        self.refresh_actions()

    def remove_action(self) -> None:
        sel = self.actions_listbox.curselection()
        if sel:
            self.clicker.remove_action(sel[0])
            self.refresh_actions()

    def start_record(self) -> None:
        self.recorder.start()
        messagebox.showinfo("Recording","Recording user events...")

    def stop_record(self) -> None:
        macro = self.recorder.stop()
        self.clicker.load_macro(macro)
        messagebox.showinfo("Macro Loaded",f"Loaded {len(macro.events)} events")

    def on_exit(self) -> None:
        self.clicker.exit()
        self.root.quit()

# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    root = tk.Tk(); root.title("AutoClicker & Recorder")
    recorder = Recorder()
    clicker = AutoClicker(actions=[], macro=None)
    clicker.start()
    ClickerGUI(root, clicker, recorder)
    root.mainloop()
    clicker.join()

if __name__ == "__main__":
    main()
