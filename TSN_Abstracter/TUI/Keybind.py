from .Globals import *;



__all__: list[str] = [
	"Keybind",
	"Keybinds"
];





@dataclass
class Keybind:
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