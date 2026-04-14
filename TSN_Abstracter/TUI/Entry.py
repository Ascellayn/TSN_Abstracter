from .Globals import *;





class eType():
	""" A class containing every single type of Entries currently implemented in the TUI Framework.  
	INTs are used instead of strings to specify Entry Types for performance/memory reasons, it's also much faster to type.  
	Using raw integers is still preferred over typing `TUI.eType.Function.value`, mostly because it's painfully long to write than just `0`."""
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
	TextSelectable = 21;





def _NULL() -> None: pass;
@dataclass
class Entry:
	""" An Entry Object is a displayable `TUI.Menu` object that holds functions to execute along with arguments and a whole lot of other parameters.

	Arguments:
		Type (int*): The Type of the Entry.
		Name (str): The (selectable) text to display.
		Description (str): The text to display in most notably the Description Box of `TUI.Menu`.
		ID (str | None = None): An ID to specify to more easily fetch data from.
		Indentation (int = 0): How far away from the left the Entry is displayed.
		Unavailable (bool = False): Whenever the Entry is actionable.
		Required (bool = False): Whenever the Entry must have a non-None value in order for a given `TUI.Menu`'s `TUI.Entry(1) (Finalize)` to function.
		Bold (bool = False): Make the displayed `Name` bold.
		Function (Callable): A function to run when actioned. Unused depending on the Entry Type.
		Arguments (list[Any] | tuple[Any, ...] = ()): Arguments to pass through the function. **[!]** Behavior changes depending on the Entry Type, see Entry Type section. **[!]**
		Value (str | bool = ""): The default value of the Entry.

	# Entry Types
	Generic Entry Types that are intended to exit `TUI.Menu`, primarily running functions in the end.
	## FUNCTION GROUP
	### Function (0)
	This type when actioned inside a Menu simply runs `Function(*Arguments)`.
	### Finalize (1)
	This type when actioned inside a Menu returns the `TUI.Entries_To_Dict()` of every Entries sent to `TUI.Menu`.
	### Return (2)
	This type when actioned inside a Menu returns `Value`.

	## INPUT GROUP
	Generic Entry Types that handle user input.
	### Toggle (10)
	This type when actioned inside a Menu toggles its `Value` between `True` and `False`, specially displays a checkbox.
	### IOText (11)
	This type when actioned inside a Menu runs `TUI.Text`, specially displays the current set text.  
	**The `Arguments` value behaves differently here**, it must be a __singular string__ representing the regex pattern of what is valid to enter.
	### Array (12)
	This type when actioned inside a Menu runs a sub-`TUI.Menu` with a list of the available elements to select, specially displays the selectable elements.  
	Using the Left and Right arrow keys lets you quickly select one of the available options.
	**The `Arguments` value behaves differently here**, it is an __array__ containing the available options to select from.

	## TEXT GROUP
	Generic Entry Types that are only used to display things.
	### Text (20)
	Only used to display text, this Entry is automatically skipped and cannot be selected.  
	### TextSelectable (21)
	Standard `Text` Entry Type, but can be selected instead of being skipped over.  
	"""
	def __init__(self,
			Type: int,
			Name: str = "Unnamed Entry",
			Description: str = "This entry does not have any description.",
			ID: str | None = None,

			Indentation: int = 0,
			Unavailable: bool = False,
			Required: bool = False,
			Bold: bool = False,

			Function: Callable[[], Any] | Callable[[Any], Any] = _NULL,
			Arguments: list[Any] | tuple[Any, ...] = (),
			Value: str | bool = "",
		) -> None:
		self.Type: int = Type;

		self.Name: str = Name;
		self.Description: str = Description;
		self.ID: str | None = ID;

		self.Indentation: int = Indentation;
		self.Unavailable: bool = Unavailable;
		self.Required: bool = Required;
		self.Bold = Bold;


		self.Function: Callable[[], Any] | Callable[[Any], Any] = Function;
		self.Arguments: list[Any] | tuple[Any, ...] = tuple(Arguments);
		self.Value: str | bool = Value;

		self.__ValueInitial: Any = None;

		match self.Type:
			case eType.Finalize: self.Indentation = self.Indentation - 2;
			case eType.Text: self.Indentation = self.Indentation - 2;
			case _: pass;

		self.Index: int = 0;



	def Toggle(self) -> bool:
		""" Toggle between `True` and `False`, to be used with a Toggle Entry (`10`).  
		Also returns the new state of `self.Value`."""
		self.Value = False if (self.Value) else True;
		return self.Value;
type Entries = list[Entry] | tuple[Entry, ...];





def Entries_To_Dict(Entries: Entries) -> dict[str, Any]:
	""" Takes in a list of Entry Objects and dumps their `.Value` with the key `.ID` when it is defined into a dictionary.

	Arguments:
		Entries (Entries*): The list of Entry Objects.

	Returns:
		dict[str, Any]: The returned Dictionary containing the data extracted from each Entry with an `ID`.

	Examples:
		>>> TUI.Entries_To_Dict([
			TUI.Entry(10, ID="Hello", Value="There"),
			TUI.Entry(20, "This is some random thing"),
		]);
		{
			"Hello": "There"
		}
	"""
	Data: dict[str, Any] = {};
	for Entry in Entries:
		if (Entry.ID): Data[Entry.ID] = Entry.Value;

	return Data;





__all__: list[str] = [
	"eType",
	"Entry",
	"Entries",
	"Entries_To_Dict"
];