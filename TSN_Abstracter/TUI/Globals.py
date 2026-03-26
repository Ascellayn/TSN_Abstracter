from .. import App, Config, Log, String, TSNDL, TSN_Abstracter; # pyright: ignore[reportUnusedImport]

import curses, curses.textpad, enum, re; # pyright: ignore[reportUnusedImport]

from dataclasses import dataclass; # pyright: ignore[reportUnusedImport]
from typing import Any, Callable, cast; # pyright: ignore[reportUnusedImport]



Window: curses.window = curses.initscr();





def Init() -> None:
	Window.move(0,0);
	Window.erase();
	Window.refresh();
	Window.keypad(True);
	Window.nodelay(True);
	curses.noecho();
	curses.cbreak();
	curses.start_color();
	curses.use_default_colors();

	# A quick and dirty way to initialize every single SNC Color for curses
	_Colors: list[str] = ["Black", "Grey", "White", "Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "Pink"];
	_Schemes: list[str] = ["Abyss", "Night", "Moon", "Sky", "Day", "Sun"];
	for sIndex, Scheme in enumerate(_Schemes):
		for cIndex, Color in enumerate(_Colors):
			Number: int = (sIndex * 20) + cIndex;
			curses.init_color(Number, *[round(x*(1000/255)) for x in eval(f"TSNDL.Color.{Scheme}.{Color}")]);
			curses.init_pair(Number, Number, -1);

	Config.System.TUI_Enabled = True;



def Exit() -> None:
	Window.move(0,0);
	Window.clear();
	Window.refresh();
	curses.echo();
	curses.nocbreak();
	Window.keypad(False);
	Window.nodelay(False);
	curses.endwin();
	curses.reset_shell_mode();

	Config.System.TUI_Enabled = False;

Exit(); # Creating the window object somewhat runs a partial Init which screws up everything, so we run an exit.