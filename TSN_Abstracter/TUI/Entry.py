from .Globals import *;





# FUNCTION GROUP - 0X
FUNCTION = 0;
FINALIZE = 1;
RETURN = 2;

# INPUT GROUP - 1X
CHECKBOX = 10;
INPUT = 11;
CHOICE = 12;

# DISPLAY GROUP - 2X
TEXT = 20;
TEXT_SELECTABLE = 21;








def _NULL(*args: Any, **kwargs: Any) -> None: pass;
@dataclass
class Entry:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	An Entry Object is a displayable `TUI.Menu` object that holds functions to execute along with arguments and a whole lot of other parameters.

	ARGS:
		Type (int): The Type of the Entry.
		Name (str): The (selectable) text to display.
		Description (str): The text to display in most notably the Description Box of `TUI.Menu`.
		ID (str | None = None): An ID to specify to more easily fetch data from.
		Indentation (int = 0): How far away from the left the Entry is displayed.
		Unavailable (bool = False): Whenever the Entry is actionable.
		Required (bool = False): Whenever the Entry must have a non-None value in order for a given `TUI.Menu`'s `TUI.Entry(1) (Finalize)` to function.
		Bold (bool = False): Make the displayed `Name` bold.
		FUNC (Callable): A function to run when actioned. Unused depending on the Entry Type.
		ARGS (list[Any] | tuple[Any, ...] = ()): ARGS to pass through the function. **[!]** Behavior changes depending on the Entry Type, see Entry Type section. **[!]**
		VALUE (str | bool = ""): The default value of the Entry.

	# Entry Types
	Generic Entry Types that are intended to exit `TUI.Menu`, primarily running functions in the end.
	## FUNCTION GROUP
	### FUNCTION (0)
	This type when actioned inside a Menu simply runs `FUNC(*ARGS)`.
	### FINALIZE (1)
	This type when actioned inside a Menu returns the `TUI.entryJSON()` of every Entries sent to `TUI.Menu`.
	### RETURN (2)
	This type when actioned inside a Menu returns `VALUE`.

	## INPUT GROUP
	Generic Entry Types that handle user input.
	### CHECKBOX (10)
	This type when actioned inside a Menu toggles its `VALUE` between `True` and `False`, specially displays a checkbox.
	### INPUT (11)
	This type when actioned inside a Menu runs `TUI.Text`, specially displays the current set text.  
	**The `ARGS` value behaves differently here**, it must be a __singular string__ representing the regex pattern of what is valid to enter.
	### CHOICE (12)
	This type when actioned inside a Menu runs a sub-`TUI.Menu` with a list of the available elements to select, specially displays the selectable elements.  
	Using the Left and Right arrow keys lets you quickly select one of the available options.
	**The `ARGS` value behaves differently here**, it is an __array__ containing the available options to select from.

	## TEXT GROUP
	Generic Entry Types that are only used to display things.
	### TEXT (20)
	Only used to display text, this Entry is automatically skipped and cannot be selected.  
	### TEXT_SELECTABLE (21)
	Standard `Text` Entry Type, but can be selected instead of being skipped over.  
	"""
	def __init__(self,
			TYPE: int,
			NAME: str = "Unnamed Entry",
			DESCRIPTION: str = "This entry does not have any description.",
			ID: str | None = None,

			INDENTATION: int = 0,
			UNAVAILABLE: bool = False,
			REQUIRED: bool = False,
			BOLD: bool = False,
				*,
			FUNC: Callable[..., Any] = _NULL,
			ARGS: list[Any] | tuple[Any, ...] = (),
			VALUE: str | bool = "",
		) -> None:
		self.Type: int = TYPE;

		self.Name: str = NAME;
		self.Description: str = DESCRIPTION;
		self.ID: str | None = ID;

		self.Indentation: int = INDENTATION;
		self.Unavailable: bool = UNAVAILABLE;
		self.Required: bool = REQUIRED;
		self.Bold = BOLD;


		self.Func: Callable[..., Any] = FUNC;
		self.Args: list[Any] | tuple[Any, ...] = tuple(ARGS);
		self.Value: str | bool = VALUE;

		self.__ValueInitial: Any = None;

		match self.Type:
			case 1: self.Indentation = self.Indentation - 2; # Finalize
			case 20: self.Indentation = self.Indentation - 2; # Text
			case _: pass;

		self.Index: int = 0;



	def toggle(self) -> bool:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Toggle between `True` and `False`, to be used with a Toggle Entry (`10`).  
		Also returns the new state of `self.VALUE`."""
		self.Value = False if (self.Value) else True;
		return self.Value;



type Entries = list[Entry] | tuple[Entry, ...];





def entryJSON(Entries: Entries) -> dict[str, Any]:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Takes in a list of Entry Objects and dumps their `.Value` with the key `.ID` when it is defined into a dictionary.

	ARGS:
		Entries (Entries): The list of Entry Objects.

	Returns:
		dict[str, Any]: The returned Dictionary containing the data extracted from each Entry with an `ID`.

	Examples:
		>>> TUI.entryJSON([
			TUI.Entry(10, ID="Hello", VALUE="There"),
			TUI.Entry(20, "This is some random thing"),
		]);
		{
			"Hello": "There"
		}
	"""
	Data: dict[str, Any] = {};
	for e in Entries:
		if (e.ID): Data[e.ID] = e.Value;

	return Data;










__all__: list[str] = [
	"FUNCTION", "FINALIZE", "RETURN", "CHECKBOX", "INPUT", "CHOICE", "TEXT", "TEXT_SELECTABLE",
	"Entry", "Entries", "entryJSON"
];