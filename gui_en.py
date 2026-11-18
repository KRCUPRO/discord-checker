# gui_en.py - English Edition Entrypoint
import gui

def main():
    app = gui.DiscordCheckerGui(default_lang="en")
    app.mainloop()

if __name__ == "__main__":
    main()
