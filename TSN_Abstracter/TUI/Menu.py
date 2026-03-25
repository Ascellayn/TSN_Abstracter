from .Globals import *;

from .Prompt import *;
from .Keybind import Keybinds;
from .Entry import Entry as __Entry, eType, Entries, Entries_To_Dict;

from . import Draw, Input;



__all__: list[str] = [
	"Menu"
];






def __ColorAttribute(Color: int) -> None: Window.attron(curses.color_pair(Color));



def Menu(Entries: Entries, Keybinds: Keybinds = [], Index: int = 0) -> Any:
	x: int; y: int = 2;


	# Init default value for supported types where a dev potentially forgot to set a default value.
	for Entry in Entries:
		if (Entry.Type == eType.Toggle):
			if (not Entry.Value): Entry.Value = False;
		if (Entry.Type == eType.Array):
			if (not Entry.Value): Entry.Value = Entry.Arguments[0];


	Fake_Indices: dict[str, int] = {};
	fakeIndex: int = 1;
	for tIndex, Entry in enumerate(Entries):
		Entry.Index = tIndex; # Ability to retrieve Index from Object to go back to previous option in previous menu if possible.

		# Get Fake Index for more accurate selection
		if (Entry.Type != eType.Text):
			Fake_Indices[str(tIndex)] = fakeIndex;
			fakeIndex += 1;

		# Set default values for Reset function
		if (Entry.Type in [eType.Toggle, eType.IOText, eType.Array]): # Toggle
			Entry.__ValueInitial = Entry.Value; # pyright: ignore[reportPrivateUsage]


	while True:
		Draw.Base();
		Draw.Base_Box();
		Max_Visible: int = curses.LINES - 6;


		# Failsafe when Entry Type is not selectable
		while (Entries[Index].Type == eType.Text): Index += 1;

		y = 2 + round(Max_Visible / 2) if ((len(Entries) - 1) >= Max_Visible and Index > round(Max_Visible / 2)) else 2 + Index;

		fakeIndex = Fake_Indices[str(Index)] if (str(Index) in Fake_Indices) else Index;


		# Used to automatically unavailable Finalizers if every other entry isn't filled.
		Missing_Entries: list[str | None] = [];
		for Entry in Entries:
			if (Entry.Type == eType.IOText and Entry.Value == "" and Entry.Required): Missing_Entries.append(Entry.ID);


		x = 3 + (2 * Entries[Index].Indentation);
		# Display entries
		Displayed: int = 0;
		for Number, Entry in enumerate(Entries):
			if (Max_Visible < len(Entries)):
				if (Displayed >= Max_Visible): break;
				if (Number + round(Max_Visible / 2) < Index): continue;
			eX: int = 6 + (2 * Entry.Indentation); eY = 2 + Displayed;

			if (Entry.Type == eType.Finalize and Entry.Required and len(Missing_Entries) > 0):
				Entry.Unavailable = True;
			elif (Entry.Type == eType.Finalize and Entry.Required):
				Entry.Unavailable = False;

			# Text Display
			Entry_Quirk: str = "";
			match (Entry.Type):
				case eType.Toggle: Entry_Quirk += "[X]" if (Entry.Value) else "[ ]";
				case eType.IOText: Entry_Quirk += f" - '{Entry.Value}'";
				case eType.Array:
					Values: str = "[";
					for Count, Possibility in enumerate(Entry.Arguments):
						if (Possibility == Entry.Value): Values += f"{'|' if (Count != 0) else ''} → {Possibility} ← ";
						else: Values += f"{'|' if (Count != 0) else ''} {Possibility} ";
					Values += "]";

					Entry_Quirk += f" - {Values}";

				case _: pass;

			Entry_Text: str = Entry.Name + " " + Entry_Quirk;
			if (Entry_Text != String.Abbreviate(Entry_Text, curses.COLS - eX - 1)):
				match (Entry.Type):
					case eType.Toggle: Entry_Text = String.Abbreviate(Entry_Text, curses.COLS - eX - 2 - len(Entry_Quirk)) + f" {Entry_Quirk}";
					case _: Entry_Text = String.Abbreviate(Entry_Text, curses.COLS - eX - 2);

			if (Entry.Unavailable): __ColorAttribute(SNDL.Color.Moon.Grey_TERM);
			if (Entry.Bold): Window.attron(curses.A_BOLD);
			Window.addstr(eY, eX, Entry_Text);
			Window.attrset(0);

			Displayed += 1;





		# Cursor Display
		if (Entries[Index].Indentation != -2): # Ignore on -2 Indent
			if (Entries[Index].Type != eType.Finalize): # No cursor on Finalize
				if (Entries[Index].Type != eType.Toggle): # Don't overwrite the toggle state
					Window.addch(y, x, "ø" if (Entries[Index].Unavailable) else ">");

		# Description
		Description: str = String.Abbreviate(f"[{String.Trailing_Zero(fakeIndex, len(str(len(Entries))))}] {Entries[Index].Description}", curses.COLS - 4);
		Window.addstr(curses.LINES - 2, 2, Description);

		# Low Res. Terms: Give scroll Hint
		if (Index != (len(Entries) - 1) and Max_Visible < len(Entries)):
			Remaining: int = len(Entries) - Index - round(Max_Visible / 2) + 1;
			if (Remaining > 0): # Rounding error correction band-aid fix
				Window.addstr(curses.LINES - 4, 2, String.Abbreviate(f" ... ({Remaining} more)", curses.COLS - 5));

		# Cursor & Refresh
		match (Entries[Index].Type):
			case eType.Finalize: Window.move(y, 2 + len(Entries[Index].Name));
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
						case eType.Text: Index += 1;
						case _: break;

			case curses.KEY_UP:
				Index -= 1;
				while (True): # Go Up one more if Unselectable Type
					if (Index <= -1): Index = len(Entries) - 1;
					match (Entries[Index].Type):
						case eType.Text: Index -= 1;
						case _: break;


			case 338: # PAGE DOWN:
				Index += Max_Visible;
				while (True): # Go Up one more if Unselectable Type
					if (Index > len(Entries) - 1): Index = len(Entries) - 1; curses.flash();
					match (Entries[Index].Type):
						case eType.Text: Index -= 1;
						case _: break;

			case 339: # PAGE UP:
				Index -= Max_Visible;
				while (True): # Go Up one more if Unselectable Type
					if (Index <= -1): Index = 0; curses.flash();
					match (Entries[Index].Type):
						case eType.Text: Index += 1;
						case _: break;



			case 27: curses.flash(); return None; # ESC


			# ARRAY ONLY INPUTS
			case curses.KEY_LEFT:
				if (Entries[Index].Type != eType.Array): continue;
				aIndex: int = Entries[Index].Arguments.index(Entries[Index].Value);
				if (aIndex == 0): Entries[Index].Value = Entries[Index].Arguments[len(Entries[Index].Arguments) - 1];
				else: Entries[Index].Value = Entries[Index].Arguments[aIndex - 1];

			case curses.KEY_RIGHT:
				if (Entries[Index].Type != eType.Array): continue;
				aIndex: int = Entries[Index].Arguments.index(Entries[Index].Value);
				if (aIndex == len(Entries[Index].Arguments) - 1): Entries[Index].Value = Entries[Index].Arguments[0];
				else: Entries[Index].Value = Entries[Index].Arguments[aIndex + 1];


			# MISC INPUTS
			case 104: # "h" - Help for Selected Entry
				Prompt(Entries[Index].Name, Entries[Index].Description, __Entry(eType.Array, Arguments=["Ok"]));


			case 72: # "H" - Help for Keybinds
				Description: str = f"""
TSN Abstracter Default Keybinds:\n
[h] - Show Entry Description\n
[H] - Show Available Keybinds\n
\n
[r] - Reset Selected Entry to Initial Value\n
[R] - Reset All Entry to their Initial Value\n
\n
{App.Name} Keybinds (for this Menu):\n
""";

				for Keybind in Keybinds:
					Description += f"[{chr(Keybind.Key)}] {Keybind.Name}\n";
				Description += "\n";

				Prompt("Keybinds Help", Description[:-1], __Entry(eType.Array, Arguments=["Ok"]), "Left");
				del Description;



			case 114: # "r" - Reset Selected Entry to initial value
				if (not Entries[Index].Type in [10, 11, 12]): continue;
				if (Entries[Index].Value == Entries[Index].__ValueInitial): continue; # pyright: ignore[reportPrivateUsage]

				Description: str = f"""
Are you sure you want to reset \"{Entries[Index].ID}\" to its initial value?\n\n
\"{Entries[Index].Value}\"\n
\n... will be reset to:\n\n
\"{Entries[Index].__ValueInitial}\"\n"""; # pyright: ignore[reportPrivateUsage]

				if ("Yes" == Prompt(
					"Reset Selected Entry to Initial Value", Description,
					__Entry(eType.Array, Arguments=["Yes", "No"], Value="No")
				)):
					Entries[Index].Value = Entries[Index].__ValueInitial; # pyright: ignore[reportPrivateUsage]
				del Description;


			case 82: # "R" - Reset Every Entry to their Initial Value
				if ("Yes" == Prompt(
					"Reset All Entries to their Initial Value", "Are you sure you want to reset every entries to their default values?",
					__Entry(eType.Array, Arguments=["Yes", "No"], Value="No")
				)):
					for Entry in Entries:
						if (not Entry.Type in [eType.Toggle, eType.IOText, eType.Array]): continue;
						Entry.Value = Entry.__ValueInitial; # pyright: ignore[reportPrivateUsage]






			case 10: # Enter - Execute Entry Features
				if (Entries[Index].Unavailable and Entries[Index].Type != eType.Finalize): curses.beep(); curses.flash(); continue;

				match (Entries[Index].Type):
					# Function Group
					case eType.Function: # Execute Function
						return Entries[Index].Function(*Entries[Index].Arguments);


					case eType.Finalize:
						if (Entries[Index].Unavailable):
							Description: str = f"You have not filled the following remaining {f'{len(Missing_Entries)} required entries' if (len(Missing_Entries) > 1) else 'required entry'}:\n";
							for Missed in Missing_Entries:
								Description += f"- {Missed if (Missed) else '<NO ENTRY ID>'}\n";
							Prompt("Missing Information", Description[:-1], __Entry(eType.Array, Value="Ok", Arguments=["Ok"]), "Left");
							del Description;
							continue;

						Data: str = "";
						for Key, Value in Entries_To_Dict(Entries).items(): # pyright: ignore[reportAssignmentType]
							Data += f"{Key}: {Value}\n";

						if ("Yes" == Prompt("Confirm Input", f"You will be saving the following settings:\n\n{Data[:-1]}", __Entry(eType.Array, Value="No", Arguments=["Yes", "No"]), "Left")):
							return Entries_To_Dict(Entries); # pyright: ignore[reportCallIssue]


					case eType.Return:
						return Entries[Index].Value;



					# Input Group
					case eType.Toggle:
						Entries[Index].Toggle(); continue;


					case eType.IOText:
						Entries[Index].Value = Input.Text(cast(str, Entries[Index].Value), *Entries[Index].Arguments); continue;


					case eType.Array: # Array Input
						Sub_Entries: list[__Entry] = [
							__Entry(eType.Text, Entries[Index].Name, Bold=True),
							__Entry(eType.Text, Entries[Index].Description),
							__Entry(eType.Text, "")
						];

						for Value in Entries[Index].Arguments: # pyright: ignore[reportAssignmentType]
							Sub_Entries.append(__Entry(eType.Return, Value, Value=Value));

						Entries[Index].Value = Menu(Sub_Entries, Index=Entries[Index].Arguments.index(Entries[Index].Value) + 3);
						del Sub_Entries; continue;



					# Display Group
					case eType.TextSelectable: curses.flash();


					case _: pass;
			# Keybinds Logic
			case _:
				for Keybind in Keybinds:
					if (Key == Keybind.Key):
						return Keybind.Function(Entries[Index], *Keybind.Arguments); # pyright: ignore[reportCallIssue]