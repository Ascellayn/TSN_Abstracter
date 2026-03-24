from .Globals import *;
from . import Draw, Entry, Input;



__all__: list[str] = [
	"Popup"
];





def Popup(Title: str, Description: str, Entry: Entry, Align: str = "Center") -> Any: # pyright: ignore[reportRedeclaration]
	""" Entry type must be Array """
	def _GetTextX(Text: str, Align: str) -> int:
		match Align:
			case "Center": return ULX - round((len(Text) - (LRX - ULX)) / 2);
			case "Left": return ULX + 2;
			case "Right": return LRX - len(Text);
			case _: raise ValueError(f"TSNA.TUI | Align property \"{Align}\" does not exist.")

	Title = " [" + Title + "] ";

	if (not Entry.Value): Entry.Value = Entry.Arguments[0];
	Index: int = Entry.Arguments.index(Entry.Value); iDescription: list[str] = Description.split("\n");
	Initial: str = cast(str, Entry.Value);

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


		Draw.Base(False if (iLINES == curses.LINES and iCOLS == curses.COLS) else True);
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