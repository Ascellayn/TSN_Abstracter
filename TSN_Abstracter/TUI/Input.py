from .Globals import *;
from . import Draw;



__all__: list[str] = [
	"Get",
	"Text"
];



Key_Held: int = -1;






def Get() -> int:
	""" Blocking Input Catcher"""
	global Key_Held;
	while True:
		CHAR = Window.getch();
		if (CHAR != -1 and Key_Held != CHAR): Key_Held = CHAR; return CHAR;
		Key_Held = -1;





def Text(Value: str = "", Allowed: str = r".") -> str:
	""" allowed represents regex, if regex fails then character is not inputted, value is default """
	Initial: str = Value;
	x: int = 2 + (len(Value) - 1); y: int = curses.LINES - 2; Cursor: int = 0;

	while True:
		# Empty Description Field
		Window.addstr(y, 0, " " * curses.COLS);
		Window.hline(y - 1, 1, curses.ACS_HLINE, curses.COLS - 2);

		if (len(Value) > curses.COLS - 3):
			Window.addstr(y, 1,
				Value[
					max(len(Value) - (curses.COLS - 3) + Cursor, 0):
				]
			);
		else: Window.addstr(y, 1, Value);

		Draw.Base(False);
		Draw.Base_Box();
		Window.move(y, min(x + Cursor, curses.COLS - 2));
		Key = Get();
		match (Key): # We use ints here because the predefined numbers by curses don't work for some reason.
			case 10: return Value; # Enter
			case 27: curses.flash(); return Initial; # ESC

			case curses.KEY_LEFT:
				if ((len(Value) + (Cursor - 1)) != -1): Cursor -= 1;
				else: curses.flash(); curses.beep();
			case curses.KEY_RIGHT:
				if ((Cursor + 1) != 1): Cursor += 1;
				else: curses.flash(); curses.beep();

			case 263: # Delete
				if (len(Value) == 0): curses.flash(); curses.beep(); continue;

				x -= 1;
				if (Cursor == 0): Value = Value[:-1];
				else: Value = Value[:Cursor -1] + Value[Cursor:];


			case _: # Actual input
				if (not re.match(Allowed, chr(Key))): curses.flash(); curses.beep(); continue;

				if (Cursor == 0): Value += chr(Key);
				else: Value = Value[:Cursor] + chr(Key) + Value[Cursor:];
				x += 1;

		Window.refresh();