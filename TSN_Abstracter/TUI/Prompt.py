""" ***Implemented in __TSNA `v7.0.0`__***  

Module in charge of being able to display Popups and get data from the user.
"""
from .Globals import *;
from . import Draw, Input;

from .Entry import Entry;
from . import FUNCTION, FINALIZE, RETURN, CHECKBOX, INPUT, CHOICE, TEXT, TEXT_SELECTABLE;
class T:
	FUNCTION = FUNCTION;
	FINALIZE = FINALIZE;
	RETURN = RETURN;
	CHECKBOX = CHECKBOX;
	INPUT = INPUT;
	CHOICE = CHOICE;
	TEXT = TEXT;
	TEXT_SELECTABLE = TEXT_SELECTABLE;
# THIS IS FUCKING AWFUL AND NEEDS TO BE CHANGED!! SEPARATE THE TYPES INTO ANOTHER PYTHON MODULE FUCK IT
# IF THIS MAKES RELEASE V7 IM GOING TO STRANGLE MY PAST SELF








def prompt(Title: str, Description: str, Entry: Entry = Entry(12, ARGS=["OK"]), Align: str = "Center") -> Any: # pyright: ignore[reportRedeclaration]
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Displays a floating popup at the center of the screen, asking the user to make a choice.

	Arguments:
		Title (str): The text to show at the top of the Prompt Frame.
		Description (str): The text to show inside the Prompt Frame before the Entry.
		Entry (Entry): **[!] MUST BE EITHER AN `IOText (11)` OR `Array (12)` ENTRY [!]** - The Entry with the options available to choose from or to type in.
		Align (str = "Center"): The text alignment. Can be either "Center", "Left" or "Right".
	"""
	def __getTextX(Text: str, Align: str) -> int:
		match Align:
			case "Center": return ULX - round((len(Text) - (LRX - ULX)) / 2);
			case "Left": return ULX + 2;
			case "Right": return LRX - len(Text);
			case _: raise ValueError(f"TSNA.TUI | Align property \"{Align}\" does not exist.");

	if (Entry.Type not in [T.CHOICE, T.INPUT]):
		Log.crit(f"Entry Type of ID {Entry.Type} is unsupported by TUI.Prompt");
		return;


	Title = " [" + Title + "] ";
	iDescription: list[str] = Description.split("\n");

	iLINES: int = curses.LINES; iCOLS: int = curses.COLS;

	if (Entry.Type == T.CHOICE):
		if (not Entry.Value): Entry.Value = Entry.Args[0];
		Index: int = Entry.Args.index(Entry.Value); 
		Initial: str = cast(str, Entry.Value);


	# Input Handling for Array
	while True:
		# Get Selection, only really applicable for Array Types but still helps for IOText
		Values: str = "[";
		for i, possibility in enumerate(Entry.Args):
			if (possibility == Entry.Value): Values += f"{'|' if (i != 0) else ''} → {possibility} ← ";
			else: Values += f"{'|' if (i != 0) else ''} {possibility} ";
		Values += "]";

		# Failsafe if Description is too long, creates automatic spacing
		Description: list[str] = [];
		for line in iDescription:
			if (len(line) > curses.COLS - 8):
				for splitted in String.lengthSplit(line, curses.COLS - 8):
					Description.append(splitted);
			else: Description.append(line);


		# Drawing Textbox
		Horizontal: int = max(len(Title), *[len(x) for x in Description], len(Values)) + 3;
		Vertical: int = 4 + len(Description);

		ULX: int = round(((curses.COLS - Horizontal) / 2));
		ULY: int = round(((curses.LINES - Vertical) / 2));
		LRY: int = round(((curses.LINES - Vertical) / 2)) + Vertical;
		LRX: int = round(((curses.COLS - Horizontal) / 2)) + Horizontal;


		Draw.frame(False if (iLINES == curses.LINES and iCOLS == curses.COLS) else True);
		for y in range(ULY + 1, LRY): Window.addstr(y, ULX + 1, " " * (LRX - ULX - 1));
		curses.textpad.rectangle(Window, ULY, ULX, LRY, LRX);

		Window.addstr(ULY, __getTextX(Title, "Center"), Title, curses.A_BOLD); # Title

		dY: int = ULY + 2; # Description
		for line in Description:
			Window.addstr(dY, __getTextX(line, Align), line);
			dY += 1;


		if (Entry.Type == T.INPUT):
			return Input.Text(cast(str, Entry.Value), cast(str, Entry.Args[0]), Limitation=(ULX + 2, LRX - 1, LRY - 1));


		Window.addstr(LRY - 1, LRX - 1 - len(Values), Values); # Selection
		Key: int = Input.Get();
		match (Key):
			case curses.KEY_LEFT:
				if (Index == 0): Index = len(Entry.Args) - 1; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
				else: Index -= 1; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point

			case curses.KEY_RIGHT:
				if (Index == (len(Entry.Args) - 1)): Index = 0; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
				else: Index += 1; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
			case 27: curses.flash(); return Initial; # ESC # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
			case 10: return Entry.Value; # Enter
			case _: pass;

		Entry.Value = Entry.Args[Index]; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point










__all__: list[str] = [
	"prompt"
];