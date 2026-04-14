""" Module in charge of being able to display Popups and get data from the user. """
from .Globals import *;
from . import Draw, Input;
from .Entry import Entry as __Entry, eType;





def Prompt(Title: str, Description: str, Entry: __Entry = __Entry(12, Arguments=["OK"]), Align: str = "Center") -> Any: # pyright: ignore[reportRedeclaration]
	""" Displays a floating popup at the center of the screen, asking the user to make a choice.

	Arguments:
		Title (str*): The text to show at the top of the Prompt Frame.
		Description (str*): The text to show inside the Prompt Frame before the Entry.
		Entry (Entry): **[!] MUST BE EITHER AN `IOText (11)` OR `Array (12)` ENTRY [!]** - The Entry with the options available to choose from or to type in.
		Align (str = "Center"): The text alignment. Can be either "Center", "Left" or "Right".
	"""
	def _GetTextX(Text: str, Align: str) -> int:
		match Align:
			case "Center": return ULX - round((len(Text) - (LRX - ULX)) / 2);
			case "Left": return ULX + 2;
			case "Right": return LRX - len(Text);
			case _: raise ValueError(f"TSNA.TUI | Align property \"{Align}\" does not exist.")

	if (Entry.Type not in [eType.Array, eType.IOText]):
		Log.Critical(f"Entry Type of ID {Entry.Type} is unsupported by TUI.Prompt");
		return;



	Title = " [" + Title + "] ";
	iDescription: list[str] = Description.split("\n");

	iLINES: int = curses.LINES; iCOLS: int = curses.COLS;

	if (Entry.Type == eType.Array):
		if (not Entry.Value): Entry.Value = Entry.Arguments[0];
		Index: int = Entry.Arguments.index(Entry.Value); 
		Initial: str = cast(str, Entry.Value);


	# Input Handling for Array
	while True:
		# Get Selection, only really applicable for Array Types but still helps for IOText
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


		if (Entry.Type == eType.IOText):
			return Input.Text(cast(str, Entry.Value), cast(str, Entry.Arguments[0]), Limitation=(ULX + 2, LRX - 1, LRY - 1));


		Window.addstr(LRY - 1, LRX - 1 - len(Values), Values); # Selection
		Key: int = Input.Get();
		match (Key):
			case curses.KEY_LEFT:
				if (Index == 0): Index = len(Entry.Arguments) - 1; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
				else: Index -= 1; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point

			case curses.KEY_RIGHT:
				if (Index == (len(Entry.Arguments) - 1)): Index = 0; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
				else: Index += 1; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
			case 27: curses.flash(); return Initial; # ESC # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point
			case 10: return Entry.Value; # Enter
			case _: pass;

		Entry.Value = Entry.Arguments[Index]; # pyright: ignore[reportPossiblyUnboundVariable] // Literally impossible to be unbound at this point





__all__: list[str] = [
	"Prompt"
];