""" ***Implemented in __TSNA `v7.0.0`__***  

User Input functions for the TUI Framework 

### Examples
>>> from TSN_Abstracter import *;
>>> from TSN_Abstracter import TUI;
>>> TUI.init();
>>> TUI.Get();
[*User presses a Key*]
129 # The integer representation of which key was pressed.
"""
from .Globals import *;
from . import Draw;


import time;





Key_Held: int = -1;








def Get(HZ: int = 1000) -> int:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Blocking Input Catcher
	"""
	global Key_Held;
	while True:
		CHAR: int = Window.getch();
		if (CHAR != -1 and Key_Held != CHAR): Key_Held = CHAR; return CHAR;
		Key_Held = -1;
		time.sleep((1000 / HZ) / 1000);





def Text(Value: str = "", Allowed: str = r".", Limitation: tuple[int, int, int] | None = None) -> str:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	allowed represents regex, if regex fails then character is not inputted, value is default 
	limitation is x_min, x_max, Y
	"""
	initial: str = Value;
	cursor: int = 0;

	if (not Limitation):
		x_min: int = 2;
		x_max: int = curses.COLS - 2;
		y: int = curses.LINES - 2;
	else:
		x_min: int = Limitation[0];
		x_max: int = Limitation[1];
		y: int = Limitation[2];

	x: int = x_min + (len(Value) - 1);


	while True:
		# Empty Description Field
		Window.addstr(y, x_min - 1, " " * (x_max - x_min + 2));

		if (len(Value) > (x_max - x_min)):
			Window.addstr(y, x_min - 1,
				(Value[
					max(len(Value) - (x_max - x_min) + cursor, 0):
				])[:(x_max - x_min)]
			);
		else: Window.addstr(y, x_min - 1, Value[:(x_max - x_min)]);

		Draw.frame(False);
		Window.move(y, min(x + cursor, x_max));
		Key = Get();
		match (Key): # We use ints here because the predefined numbers by curses don't work for some reason.
			case 10: return Value; # Enter
			case 27: curses.flash(); return initial; # ESC

			case curses.KEY_LEFT:
				if ((len(Value) + (cursor - 1)) != -1): cursor -= 1;
				else: curses.flash(); curses.beep();
			case curses.KEY_RIGHT:
				if ((cursor + 1) != 1): cursor += 1;
				else: curses.flash(); curses.beep();

			case 263: # Delete
				if ((len(Value) + cursor) == 0): curses.flash(); curses.beep(); continue;

				x -= 1;
				if (cursor == 0): Value = Value[:-1];
				else: Value = Value[:cursor -1] + Value[cursor:];


			case _: # Actual input
				if (not re.match(Allowed, chr(Key))): curses.flash(); curses.beep(); continue;

				if (cursor == 0): Value += chr(Key);
				else: Value = Value[:cursor] + chr(Key) + Value[cursor:];
				x += 1;

		Window.refresh();










__all__: list[str] = [
	"Get",
	"Text"
];