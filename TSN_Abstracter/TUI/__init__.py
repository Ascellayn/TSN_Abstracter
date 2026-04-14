""" ### Terminal User Interface Framework for TSNA-Based Applications  
*THIS MODULE IS __NOT__ AUTOMATICALLY IMPORTED BY TSN ABSTRACTER!*  
Prior knowledge of how `curses` functions is heavily recommended.  

<br>

The TSNA TUI Framework is heavily based on "Entries", these entries range from simple Text display in most notably `TUI.Menu` or as full on interactive elements (Checkboxes, Text, Selection Array, ...)  
Most of your efforts will be spent using `TUI.Menu`, `TUI.Prompt` and `TUI.Entry` naturally.  

Running `TUI.Init()` is required before running any functions from this module. The inverse (`TUI.Exit()`) can be used to stop the TUI Mode which is required in order to avoid severe text display issues.  
**Notice**: The TSNA `Log.*` functions are naturally heavily broken by the enabling of the TUI Mode.  

A `Window` object is provided by `TUI/Globals.py` if you are in need of doing more advanced things.

"""

from .Entry import *;
from .Keybind import *;

from .Menu import *;
from .Prompt import *;

from .Globals import *;
from . import Draw, Input;





__all__ = [
	"Window", "curses",
	"Draw", "Input",
	"Entry", "Entries", "eType", "Entries_To_Dict"
];


