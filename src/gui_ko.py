# src/gui_ko.py - Korean Edition Entrypoint
import sys
from pathlib import Path

_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from src import gui

def main():
    app = gui.DiscordCheckerGui(default_lang="ko")
    app.mainloop()

if __name__ == "__main__":
    main()
