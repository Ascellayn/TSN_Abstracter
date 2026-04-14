""" Custom actions triggered by pressing a Key for `TUI.Menu` """
from .Globals import *;



__all__: list[str] = [
	"Keybind",
	"Keybinds"
];





@dataclass
class Keybind:
	""" A Keybind object to be passed in `TUI.Menu`  
	**[!]** When a Keybind is called, its first argument is __ALWAYS__ the selected entry from `TUI.Menu` **[!]**

	Arguments:
		Key (int*): An integer representation of a key to press to trigger `Function`.
		Name (str*): A description of the Keybind to be shown by pressing `H`.
		Function (Callable*): The function to run when the Keybind is triggered.
		Arguments (list[Any] | tuple[Any, ...]): The arguments to pass in `Function`.
	"""
	def __init__(self,
			Key: int,
			Name: str,
			Function: Callable[[], Any] | Callable[[Any], Any],
			Arguments: list[Any] | tuple[Any, ...] = (),
		) -> None:
		self.Key: int = Key;
		self.Name: str = Name;
		self.Function: Callable[[], Any] | Callable[[Any], Any] = Function;
		self.Arguments: list[Any] | tuple[Any, ...] = tuple(Arguments);

type Keybinds = list[Keybind] | tuple[Keybind, ...];