""" ***Implemented in __TSNA `v7.0.0`__***  

Custom actions triggered by pressing a Key for `TUI.Menu`
"""
from .Globals import *;








@dataclass
class Keybind:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	A Keybind object to be passed in `TUI.Menu`  
	**[!]** When a Keybind is called, its first argument is __ALWAYS__ the selected entry from `TUI.Menu` **[!]**

	Arguments:
		Key (int): An integer representation of a key to press to trigger `Function`.
		Name (str): A description of the Keybind to be shown by pressing `H`.
		Function (Callable): The function to run when the Keybind is triggered.
		Arguments (list[Any] | tuple[Any, ...]): The arguments to pass in `Function`.
	"""
	def __init__(self,
			KEY: int,
			NAME: str,
			FUNC: Callable[[], Any] | Callable[[Any], Any],
			ARGS: list[Any] | tuple[Any, ...] = (),
		) -> None:
		self.Key: int = KEY;
		self.Name: str = NAME;
		self.Func: Callable[[], Any] | Callable[[Any], Any] = FUNC;
		self.Args: list[Any] | tuple[Any, ...] = tuple(ARGS);

type Keybinds = list[Keybind] | tuple[Keybind, ...];










__all__: list[str] = [
	"Keybind",
	"Keybinds"
];