# gui_ko.py - Korean Edition Entrypoint
import gui

def main():
    app = gui.DiscordCheckerGui(default_lang="ko")
    app.mainloop()

if __name__ == "__main__":
    main()
