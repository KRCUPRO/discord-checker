# src/ui/tooltip.py
import tkinter as tk
from typing import Union, Callable
import customtkinter as ctk

class CTkToolTip:
    """
    Lightweight, elegant hover tooltip for CustomTkinter & Tkinter widgets.
    Supports dynamic text functions for multilingual instant updates.
    """
    def __init__(self, widget: tk.Widget, text: Union[str, Callable[[], str]], delay_ms: int = 250):
        self.widget = widget
        self.text_provider = text
        self.delay_ms = delay_ms
        self._tip_window: tk.Toplevel = None
        self._after_id = None

        self.widget.bind("<Enter>", self._on_enter, add="+")
        self.widget.bind("<Leave>", self._on_leave, add="+")
        self.widget.bind("<ButtonPress>", self._on_leave, add="+")

    def _get_text(self) -> str:
        if callable(self.text_provider):
            return self.text_provider()
        return str(self.text_provider)

    def _on_enter(self, event=None):
        self._cancel_scheduled()
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _on_leave(self, event=None):
        self._cancel_scheduled()
        self._hide()

    def _cancel_scheduled(self):
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self):
        tip_text = self._get_text()
        if not tip_text:
            return

        if self._tip_window or not self.widget.winfo_exists():
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self._tip_window = tk.Toplevel(self.widget)
        self._tip_window.wm_overrideredirect(True)
        self._tip_window.wm_attributes("-topmost", True)

        # Container frame with subtle border
        frame = tk.Frame(
            self._tip_window,
            background="#1e1e24",
            highlightbackground="#4a4a58",
            highlightcolor="#4a4a58",
            highlightthickness=1,
            padx=8,
            pady=6
        )
        frame.pack()

        label = tk.Label(
            frame,
            text=tip_text,
            justify="left",
            background="#1e1e24",
            foreground="#e6e6e6",
            font=("Segoe UI", 9),
            wraplength=340
        )
        label.pack()

        # Keep on screen bounds
        self._tip_window.update_idletasks()
        w = self._tip_window.winfo_width()
        h = self._tip_window.winfo_height()
        screen_w = self._tip_window.winfo_screenwidth()
        screen_h = self._tip_window.winfo_screenheight()

        if x + w > screen_w - 10:
            x = screen_w - w - 10
        if y + h > screen_h - 10:
            y = self.widget.winfo_rooty() - h - 5

        self._tip_window.wm_geometry(f"+{x}+{y}")

    def _hide(self):
        if self._tip_window:
            try:
                self._tip_window.destroy()
            except Exception:
                pass
            self._tip_window = None


def create_help_badge(parent, tooltip_text: Union[str, Callable[[], str]], on_click: Callable = None) -> ctk.CTkButton:
    """
    Creates a small, elegant [?] circular button with tooltip support.
    """
    badge = ctk.CTkButton(
        parent,
        text="?",
        width=18,
        height=18,
        corner_radius=9,
        font=ctk.CTkFont(size=10, weight="bold"),
        fg_color="#2b2b36",
        hover_color="#3e3e50",
        text_color="#00c8ff",
        command=on_click
    )
    CTkToolTip(badge, tooltip_text, delay_ms=150)
    return badge
