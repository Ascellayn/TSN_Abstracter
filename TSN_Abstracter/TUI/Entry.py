from .Globals import *;

type Entries = list[Entry] | tuple[Entry, ...];
__all__: list[str] = [
	"eType",
	"Entry",
	"Entries",
	"Entries_To_Dict"
];

class eType():
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
		self.Value = False if (self.Value) else True;
		return self.Value;





def Entries_To_Dict(Entries: Entries) -> dict[str, Any]:
	Data: dict[str, Any] = {};
	for Entry in Entries:
		if (Entry.ID): Data[Entry.ID] = Entry.Value;

	return Data;