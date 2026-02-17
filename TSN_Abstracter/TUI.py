from . import App, Config, Log, SNDL, String; # pyright: ignore[reportUnusedImport] | SNDL is used inside an eval
from . import TSN_Abstracter;
from dataclasses import dataclass;
from collections.abc import Callable;
import curses, curses.textpad;
import enum, re, typing;


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

			Menu.Base(False);
			Window.move(y, min(x + Cursor, curses.COLS - 2));
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
			Return = 2;

			# INPUT GROUP - 1X
			Toggle = 10;
			IOText = 11;
			Array = 12;

			# DISPLAY GROUP - 2X
			Text = 20;



		def __init__(self,
				Type: int,
				Name: str = "Unnamed Entry",
				Description: str = "This entry does not have any description.",
				ID: str | None = None,

				Indentation: int = 0, Unavailable: bool = False, Bold: bool = False,

				Function: Callable[[], typing.Any] | Callable[[typing.Any], typing.Any] = Log.Clear,
				Arguments: list[typing.Any] | tuple[typing.Any, ...] = (),
				Value: str | bool = "",
			) -> None:
			self.Type: int = Type;

			self.Name: str = Name;
			self.Description: str = Description;
			self.ID: str | None = ID;

			self.Indentation: int = Indentation;
			self.Unavailable: bool = Unavailable;
			self.Bold = Bold;

			self.Function: Callable[[], typing.Any] | Callable[[typing.Any], typing.Any] = Function;
			self.Arguments: list[typing.Any] | tuple[typing.Any, ...] = tuple(Arguments);
			self.Value: str | bool = Value;

			self.__ValueInitial: typing.Any = None;

			match self.Type:
				case 1: self.Indentation = self.Indentation - 2;
				case 20: self.Indentation = self.Indentation - 2;
				case _: pass;



		def Toggle(self) -> bool:
			self.Value = False if (self.Value) else True;
			return self.Value;



	@dataclass
	class Keybind:
		def __init__(self,
				Key: int,
				Name: str,
				Function: Callable[[], typing.Any] | Callable[[typing.Any], typing.Any],
				Arguments: list[typing.Any] | tuple[typing.Any, ...] = (),
			) -> None:
			self.Key: int = Key;
			self.Name: str = Name;
			self.Function: Callable[[], typing.Any] | Callable[[typing.Any], typing.Any] = Function;
			self.Arguments: list[typing.Any] | tuple[typing.Any, ...] = tuple(Arguments);

	type Entries = list[Entry] | tuple[Entry, ...];
	type Keybinds = list[Keybind] | tuple[Keybind, ...];





	@staticmethod
	def Entries_To_Dict(Entries: Entries) -> dict[str, typing.Any]:
		Data: dict[str, typing.Any] = {};
		for Entry in Entries:
			if (Entry.ID): Data[Entry.ID] = Entry.Value;
	
		return Data;










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
	def Popup(Title: str, Description: str, Entry: Entry, Align: str = "Center") -> typing.Any: # pyright: ignore[reportRedeclaration]
		""" Entry type must be Array """
		def _GetTextX(Text: str, Align: str) -> int:
			match Align:
				case "Center": return ULX - round((len(Text) - (LRX - ULX)) / 2);
				case "Left": return ULX + 2;
				case "Right": return LRX - len(Text);
				case _: raise ValueError(f"TSNA.TUI | Align property \"{Align}\" does not exist.")

		if (not Entry.Value): Entry.Value = Entry.Arguments[0];
		Index: int = Entry.Arguments.index(Entry.Value); iDescription: list[str] = Description.split("\n");
		Initial: str = typing.cast(str, Entry.Value);

		iLINES: int = curses.LINES; iCOLS: int = curses.COLS;
		while True:
			# Get Selection
			Values: str = "[";
			for Count, Possibility in enumerate(Entry.Arguments):
				if (Possibility == Entry.Value): Values += f"{'|' if (Count != 0) else ''} → {Possibility} ← ";
				else: Values += f"{'|' if (Count != 0) else ''} {Possibility} ";
			Values += "]";

			# Failsafe if Description is too long, creates automatic spacing
			Description: list[str] = [];
			for Line in iDescription:
				if (len(Line) > curses.COLS - 8):
					for Splitted in String.Split_Length(Line, curses.COLS - 8):
						Description.append(Splitted);
				else: Description.append(Line);


			# Drawing Textbox
			Horizontal: int = max(len(Title), *[len(x) for x in Description], len(Values)) + 3;
			Vertical: int = 4 + len(Description);

			ULX: int = round(((curses.COLS - Horizontal) / 2));
			ULY: int = round(((curses.LINES - Vertical) / 2));
			LRY: int = round(((curses.LINES - Vertical) / 2)) + Vertical;
			LRX: int = round(((curses.COLS - Horizontal) / 2)) + Horizontal;


			Menu.Base(False if (iLINES == curses.LINES and iCOLS == curses.COLS) else True);
			for Y in range(ULY + 1, LRY):
				Window.addstr(Y, ULX + 1, " " * (LRX - ULX - 1));
			curses.textpad.rectangle(Window, ULY, ULX, LRY, LRX);

			Window.addstr(ULY, _GetTextX(Title, "Center"), Title, curses.A_BOLD); # Title

			dY: int = ULY + 2; # Description
			for Line in Description:
				Window.addstr(dY, _GetTextX(Line, Align), Line);
				dY += 1;

			Window.addstr(LRY - 1, LRX - 1 - len(Values), Values); # Selection

			# Input Handling
			Key: int = Input.Get();
			match (Key):
				case curses.KEY_LEFT:
					if (Index == 0): Index = len(Entry.Arguments) - 1;
					else: Index -= 1;

				case curses.KEY_RIGHT:
					if (Index == (len(Entry.Arguments) - 1)): Index = 0;
					else: Index += 1;
				case 27: curses.flash(); return Initial; # ESC
				case 10: return Entry.Value; # Enter
				case _: pass;

			Entry.Value = Entry.Arguments[Index];







	@staticmethod
	def Interactive(Entries: Entries, Keybinds: Keybinds = []) -> typing.Any:
		x: int; y: int = 2;
		Index: int = 0;


		# Init default value for supported types where a dev potentially forgot to set a default value.
		for Entry in Entries:
			if (Entry.Type == 10): # Toggle
				if (not Entry.Value): Entry.Value = False;
			if (Entry.Type == 12): # Array:
				if (not Entry.Value): Entry.Value = Entry.Arguments[0];

		# Set default values for Reset function
		for Entry in Entries:
			if (Entry.Type in [10, 11, 12]): # Toggle
				Entry.__ValueInitial = Entry.Value; # pyright: ignore[reportPrivateUsage]



		while True:
			Menu.Base();
			Max_Visible: int = curses.LINES - 6;

			# Failsafe when Entry Type is not selectable
			while (Entries[Index].Type == 20):
				Index += 1;

			if ((len(Entries) - 1) >= Max_Visible and Index > round(Max_Visible / 2)): y = 2 + round(Max_Visible / 2);
			else: y = 2 + Index;

			x = 3 + (2 * Entries[Index].Indentation);

			# Display entries
			Displayed: int = 0;
			for Number, Entry in enumerate(Entries):
				if (Max_Visible < len(Entries)):
					if (Displayed >= Max_Visible): break;
					if (Number + round(Max_Visible / 2) < Index): continue;
				eX: int = 6 + (2 * Entry.Indentation); eY = 2 + Displayed;

				# Text Display
				if (Entry.Unavailable): _ColorAttribute(SNDL.Color.Moon.Grey_TERM);
				if (Entry.Bold): Window.attron(curses.A_BOLD);
				Window.insstr(eY, eX, Entry.Name);
				Window.attrset(0);


				# Type Quirks
				match (Entry.Type):
					case 10: Window.addstr(eY, 2 + (2 * Entry.Indentation), "[X]" if (Entry.Value) else "[ ]");
					case 11: Window.insstr(eY, eX + len(Entry.Name), f" - '{Entry.Value}'");
					case 12: # Arrays
						Values: str = "[";
						for Count, Possibility in enumerate(Entry.Arguments):
							if (Possibility == Entry.Value): Values += f"{'|' if (Count != 0) else ''} → {Possibility} ← ";
							else: Values += f"{'|' if (Count != 0) else ''} {Possibility} ";
						Values += "]";

						Window.insstr(eY, eX + len(Entry.Name), f" - {Values}");

					case _: pass;
				Displayed += 1;



			# Cursor Display
			if (Entries[Index].Indentation != -2): # Ignore on -2 Indent
				if (Entries[Index].Type != 1): # No cursor on Finalize
					if (Entries[Index].Type != 10): # Don't overwrite the toggle state
						Window.addch(y, x, "ø" if (Entries[Index].Unavailable) else ">");

			# Description
			Description: str = f"[{String.Trailing_Zero(Index, len(str(len(Entries))))}] {Entries[Index].Description}";
			if (len(Description) >= curses.COLS - 4): Description = Description[:curses.COLS - 9] + "(...)";
			Window.addstr(curses.LINES - 2, 2, Description);

			# Low Res. Terms: Give scroll Hint
			if (Index != (len(Entries) - 1) and Max_Visible < len(Entries)):
				Remaining: int = len(Entries) - Index - round(Max_Visible / 2) + 1;
				if (Remaining > 0): # Rounding error correction band-aid fix
					Window.insstr(curses.LINES - 4, 2, f" ... ({Remaining} more)");

			# Cursor & Refresh
			match (Entries[Index].Type):
				case 1: Window.move(y, 2 + len(Entries[Index].Name));
				case _:
					if (Entries[Index].Indentation == -2): Window.move(y, 2 + len(Entries[Index].Name));
					else: Window.move(y, 3 + (2 * Entries[Index].Indentation));
			Window.refresh();





			# Input Logic
			Key: int = Input.Get();
			match (Key):
				case curses.KEY_DOWN:
					Index += 1;
					while (True): # Go Up one more if Unselectable Type
						if (Index > len(Entries) - 1): Index = 0;
						match (Entries[Index].Type):
							case 20: Index += 1;
							case _: break;

				case curses.KEY_UP:
					Index -= 1;
					while (True): # Go Up one more if Unselectable Type
						if (Index == -1): Index = len(Entries) - 1;
						match (Entries[Index].Type):
							case 20: Index -= 1;
							case _: break;

				case 27: curses.flash(); return None; # ESC


				# ARRAY ONLY INPUTS
				case curses.KEY_LEFT:
					if (Entries[Index].Type != 12): continue;
					aIndex: int = Entries[Index].Arguments.index(Entries[Index].Value);
					if (aIndex == 0): Entries[Index].Value = Entries[Index].Arguments[len(Entries[Index].Arguments) - 1];
					else: Entries[Index].Value = Entries[Index].Arguments[aIndex - 1];

				case curses.KEY_RIGHT:
					if (Entries[Index].Type != 12): continue;
					aIndex: int = Entries[Index].Arguments.index(Entries[Index].Value);
					if (aIndex == len(Entries[Index].Arguments) - 1): Entries[Index].Value = Entries[Index].Arguments[0];
					else: Entries[Index].Value = Entries[Index].Arguments[aIndex + 1];


				# MISC INPUTS
				case 104: # "h" - Help for Selected Entry
					Menu.Popup(Entries[Index].Name, Entries[Index].Description, Menu.Entry(12, Arguments=["Ok"]));


				case 72: # "H" - Help for Keybinds
					Description: str = f"\
TSN Abstracter Default Keybinds:\n\
[h] - Show Entry Description\n\
[H] - Show Available Keybinds\n\
\n\
[r] - Reset Selected Entry to Initial Value\n\
[R] - Reset All Entry to their Initial Value\n\
\n\
{App.Name} Keybinds (for this Menu):\n\
";

					for Keybind in Keybinds:
						Description += f"[{chr(Keybind.Key)}] {Keybind.Name}\n";
					Description += "\n";

					Menu.Popup("Keybinds Help", Description[:-1], Menu.Entry(12, Arguments=["Ok"]), "Left");
					del Description;



				case 114: # "r" - Reset Selected Entry to initial value
					if (not Entries[Index].Type in [10, 11, 12]): continue;
					if (Entries[Index].Value == Entries[Index].__ValueInitial): continue; # pyright: ignore[reportPrivateUsage]

					Description: str = f"\
Are you sure you want to reset \"{Entries[Index].ID}\" to its initial value?\n\n\
\"{Entries[Index].Value}\"\n\
\n... will be reset to:\n\n\
\"{Entries[Index].__ValueInitial}\"\n"; # pyright: ignore[reportPrivateUsage]

					if ("Yes" == Menu.Popup(
						"Reset Selected Entry to Initial Value", Description,
						Menu.Entry(12, Arguments=["Yes", "No"], Value="No")
					)):
						Entries[Index].Value = Entries[Index].__ValueInitial; # pyright: ignore[reportPrivateUsage]
					del Description;


				case 82: # "R" - Reset Every Entry to their Initial Value
					if ("Yes" == Menu.Popup(
						"Reset All Entries to their Initial Value", "Are you sure you want to reset every entries to their default values?",
						Menu.Entry(12, Arguments=["Yes", "No"], Value="No")
					)):
						for Entry in Entries:
							if (not Entry.Type in [10, 11, 12]): continue;
							Entry.Value = Entry.__ValueInitial; # pyright: ignore[reportPrivateUsage]






				case 10: # Enter - Execute Entry Features
					if (Entries[Index].Unavailable): curses.beep(); curses.flash(); continue;

					match (Entries[Index].Type):
						# Function Group
						case 0: # Execute Function
							return Entries[Index].Function(*Entries[Index].Arguments);


						case 1: # Finalize
							Data: str = "";
							for Key, Value in Menu.Entries_To_Dict(Entries).items(): # pyright: ignore[reportAssignmentType]
								Data += f"{Key}: {Value}\n";

							if ("Yes" == Menu.Popup("Confirm Input", f"You will be saving the following settings:\n\n{Data[:-1]}", Menu.Entry(12, Value="No", Arguments=["Yes", "No"]), "Left")):
								return Menu.Entries_To_Dict(Entries); # pyright: ignore[reportCallIssue]


						case 2: # Hard Return
							return Entries[Index].Value;



						# Input Group
						case 10: # Toggle
							Entries[Index].Toggle(); continue;


						case 11: # Text Input
							Entries[Index].Value = Input.Text(typing.cast(str, Entries[Index].Value), *Entries[Index].Arguments); continue;


						case 12: # Array Input
							Sub_Entries: list[Menu.Entry] = [
								Menu.Entry(20, Entries[Index].Name, Bold=True),
								Menu.Entry(20, Entries[Index].Description),
								Menu.Entry(20, "")
							];

							for Value in Entries[Index].Arguments: # pyright: ignore[reportAssignmentType]
								Sub_Entries.append(Menu.Entry(2, Value, Value=Value));

							Entries[Index].Value = Menu.Interactive(Sub_Entries);
							del Sub_Entries; continue;



						case _: pass;
				# Keybinds Logic
				case _:
					for Keybind in Keybinds:
						if (Key == Keybind.Key):
							return Keybind.Function(Entries[Index], *Keybind.Arguments); # pyright: ignore[reportCallIssue]