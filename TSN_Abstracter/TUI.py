from . import App, Log, SNDL, String; # pyright: ignore[reportUnusedImport] | SNDL is used inside an eval
from . import TSN_Abstracter;
from dataclasses import dataclass;
from collections.abc import Callable;
import curses, enum, re, typing;


Window: curses.window = curses.initscr();
Key_Held: int = -1;







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
			curses.init_color(Number, *[round(x*(1000/255)) for x in eval(f"SNDL.Color.{Scheme}.{Color}")]);
			curses.init_pair(Number, Number, -1);


def Exit() -> None:
	Window.move(0,0);
	Window.clear();
	Window.refresh();
	curses.echo();
	curses.nocbreak();
	Window.keypad(False);
	Window.nodelay(False);
	curses.endwin();






def _ColorAttribute(Color: int) -> None: Window.attron(curses.color_pair(Color));









class Input:
	@staticmethod
	def Get() -> int:
		""" Blocking Input Catcher"""
		global Key_Held;
		while True:
			CHAR = Window.getch();
			if (CHAR != -1 and Key_Held != CHAR): Key_Held = CHAR; return CHAR;
			Key_Held = -1;


	@staticmethod
	def Text(Value: str = "", Allowed: str = r".") -> str:
		""" allowed represents regex, if regex fails then character is not inputted, value is default """
		Initial: str = Value;
		x: int = 2 + (len(Value) - 1); y: int = curses.LINES - 2; Cursor: int = 0;

		while True:
			Menu.Base(False);

			# Empty Description Field
			Window.insstr(y, 0, " " * curses.COLS);
			Window.hline(y - 1, 1, curses.ACS_HLINE, curses.COLS -2);

			Window.insstr(y, 1, Value);
			Window.move(y, x + Cursor);

			Key = Input.Get();
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










class Menu:
	@dataclass
	class Entry:
		class Action(enum.Enum):
			# FUNCTION GROUP - 0X
			Function = 0;
			Finalize = 1;

			# INPUT GROUP - 1X
			Toggle = 10;
			IOText = 11;

			# DISPLAY GROUP - 2X
			Title = 20;



		def __init__(self,
				Type: int,
				Name: str = "Unnamed Entry",
				Description: str = "This entry does not have any description.",
				Indentation: int = 0, Unavailable: bool = False,
				Function: Callable[[], typing.Any] | Callable[[typing.Any], typing.Any] = Log.Clear,
				Arguments: list[typing.Any] | tuple[typing.Any, ...] = (),
				Toggled: bool = False, Value: str = ""
			) -> None:
			self.Type: int = Type;

			self.Name: str = Name;
			self.Description: str = Description;
			self.Indentation: int = Indentation;
			self.Unavailable: bool = Unavailable;

			self.Function: Callable[[], typing.Any] | Callable[[typing.Any], typing.Any] = Function;
			self.Arguments: list[typing.Any] | tuple[typing.Any, ...] = tuple(Arguments);
			self.Toggled: bool = Toggled;
			self.Value: str = Value;

			match self.Type:
				case 1: self.Indentation = self.Indentation - 2;
				case 20: self.Indentation = self.Indentation - 2;
				case _: pass;



		def Toggle(self) -> bool:
			self.Toggled = False if (self.Toggled) else True;
			return self.Toggled;





	@staticmethod
	def Base(Clear: bool = True) -> None:
		curses.update_lines_cols();
		if (curses.LINES < 6): Exit(); Log.Critical("Terminal size is way too small! TSN Abstracter's TUI Menu requires a terminal that's at the very least 6 lines long."); exit(78);
		if (Clear): Window.clear();
		Window.border();
		Window.insstr(0, 2, f" {App.Name} - {TSN_Abstracter.App_Version()} ", curses.A_BOLD);

		Window.hline(curses.LINES - 3, 1, curses.ACS_HLINE, curses.COLS -2);
		Window.addch(curses.LINES - 3, 0, curses.ACS_SSSB);
		Window.addch(curses.LINES - 3, curses.COLS -1, curses.ACS_SBSS);



	@staticmethod
	def Interactive(Entries: list[Entry] | tuple[Entry, ...]) -> typing.Any:
		x: int; y: int = 2;
		Index: int = 0;
		while True:
			Menu.Base();
			Max_Visible: int = curses.LINES - 5;
			x = 3 + (2 * Entries[Index].Indentation);

			# Display entries
			Displayed: int = 0;
			for Number, Entry in enumerate(Entries):
				if (Max_Visible < len(Entries)):
					if (Displayed >= Max_Visible): break;
					if (Number < Index): continue;
				eX: int = 6 + (2 * Entry.Indentation); eY = 2 + Displayed;

				# Text Display
				if (Entry.Unavailable): _ColorAttribute(SNDL.Color.Moon.Grey_TERM);
				if (Entry.Type == 20): Window.attron(curses.A_BOLD);
				Window.insstr(eY, eX, Entry.Name);
				Window.attrset(0);


				# Type Quirks
				match (Entry.Type):
					case 10: Window.addstr(eY, 2 + (2 * Entry.Indentation), "[X]" if (Entry.Toggled) else "[ ]");
					case 11: Window.insstr(eY, eX + len(Entry.Name), f" - '{Entry.Value}'");
					case _: pass;
				Displayed += 1;



			# Cursor Display
			if (Entries[Index].Type != 1): # No cursor on Finalize
				if (Entries[Index].Type != 10): # Don't overwrite the toggle state
					Window.addch(y, x, "ø" if (Entries[Index].Unavailable) else ">");

			# Description
			Window.insstr(curses.LINES - 2, 2, f"[{String.Trailing_Zero(Index, len(str(len(Entries))))}] {Entries[Index].Description}");
			Window.addch(curses.LINES - 2, curses.COLS -1, curses.ACS_VLINE);
			# insstr breaks the final character so we add it back

			# Cursor & Refresh
			match (Entries[Index].Type):
				case 1: Window.move(y, 2 + len(Entries[Index].Name));
				case _: Window.move(y, 3 + (2 * Entries[Index].Indentation));
			Window.refresh();



			# Input Logic
			Key: int = Input.Get();
			match (Key):
				case curses.KEY_DOWN:
					Index += 1; Repeat: int = 1;
					while (Index != 0 and Index != len(Entries)):
						match (Entries[Index].Type):
							case 20: Index += 1; Repeat += 1;
							case _: break;

					if (Index == len(Entries)): y = 2; Index = 0; continue;
					elif ((y == curses.LINES - 5)): y = 2; continue;

					y += 1 * Repeat;


				case curses.KEY_UP:
					Index -= 1; Repeat: int = 1;
					while (Index != 0 and Index != len(Entries)):
						match (Entries[Index].Type):
							case 20: Index -= 1; Repeat += 1;
							case _: break;

					if (y == 2 and Index == -1): y = min(Displayed + 1, len(Entries) + 1, curses.LINES - 4); Index = len(Entries) - 1; continue;
					elif (y == 2): y = min(len(Entries) + 1, curses.LINES - 5); continue;

					y -= 1 * Repeat;



				case 27: curses.flash(); return ""; # ESC
				case 10: # Enter
					if (Entries[Index].Unavailable): curses.beep(); curses.flash(); continue;

					match (Entries[Index].Type):
						case 1: return Entries[Index].Function(Entries); # pyright: ignore[reportCallIssue]

						case 10: Entries[Index].Toggle(); continue;
						case 11: Entries[Index].Value = Input.Text(Entries[Index].Value, *Entries[Index].Arguments); continue;
						case _: pass;

					return Entries[Index].Function(*Entries[Index].Arguments);
				case _: pass;