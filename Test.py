from TSN_Abstracter import *;
from TSN_Abstracter import TUI;
import random;



def Init() -> None:
	Entries: list[TUI.Menu.Entry] | tuple[TUI.Menu.Entry, ...] = (
		TUI.Menu.Entry(11, "0 Input Entry", "This is where the description on TSNA Menu Entries look like.", Value="Default Value"),
		TUI.Menu.Entry(0, "1 Test Entry Indented", "This is indented!.", 1),
		TUI.Menu.Entry(0, "2 Unavailable Entry", "This is unavailable.", 2, True),
		TUI.Menu.Entry(20, "", ""),
		TUI.Menu.Entry(20, "Text Header", ""),
		TUI.Menu.Entry(10, "3 Toggle Entry", "This is where the description on TSNA Menu Entries look like."),
		TUI.Menu.Entry(10, "4 Toggle Entry", "This is where the description on TSNA Menu Entries look like.", 1),
		TUI.Menu.Entry(20, "", ""),
		TUI.Menu.Entry(1, "Finalize Entry", "This is where the description on TSNA Menu Entries look like.")
	);

	TUI.Init();
	#Log.Stateless(f"{TUI.Input.Get()}"); exit();
	TUI.Menu.Interactive(Entries);
	while True:
		TUI.curses.update_lines_cols();
		TUI.Window.border();
		TUI.Window.hline(random.randint(1, TUI.curses.LINES - 2),random.randint(1, TUI.curses.COLS - 2), random.randint(32, 254), 1);
		TUI.Window.refresh();
		TUI.curses.beep();

if __name__ == "__main__":
	try: Init();
	except Exception as Except: TUI.Exit(); raise Exception;