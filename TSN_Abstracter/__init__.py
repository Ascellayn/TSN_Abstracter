"""
**TSN Abstracter (alias TSNA or "The Sirio Network Abstracter") is a Python Module designed to accomplish relatively common tasks.**  

It was created during Kosaka's v2.X Versions and as its "Dependencies.py" file kept being ported over to other Python projects, TSNA was created to avoid sloppily copy pasting reused code and simplify the process of writing code.  
You are entirely on your own for figuring out what TSNA does and what functions would be useful in your use case. TSNA was purposefully built to build programs for TSN, as such no feature requests will be accepted, unless they're contributing to the function of a TSN Service.  

#### NOTICE: TSNA is only expected to be imported with `from TSN_Abstracter import *;` first.
You can then import additional modules such as the TUI one with `from TSN_Abstracter import TUI;`.  
We do not recommend importing TSNA in another way.

### Available Modules:
- App  
- Config  
- Cryptography [NOT IMPORTED BY DEFAULT]  
	- TSNA Dependencies:  
		- Log
	- Python Dependencies:  
		- hashlib
- Log  
	- TSNA Dependencies:  
		- Config
		- File
		- TSNDL
		- String
		- Time

	- Python Dependencies:  
		- datetime
		- inspect
		- logging
		- shutil
		- sys
- File  
	- TSNA Dependencies:  
		- Log
		- String
	- Python Dependencies:  
		- pathlib
		- os
		- lzma
		- json
- Misc  
	- Python Dependencies:  
		- multiprocessing
		- threading
- Safe  
- TSNDL  
	- TSNA Dependencies:  
		- Config
- TUI [NOT IMPORTED BY DEFAULT]  
	- Python Dependencies:  
		- curses
	- TSNA Dependencies:  
		- App
		- Config
		- Log
		- String
		- TSNDL
		- TSN_Abstracter
- String
- Time
	- TSNA Dependencies:  
		- String
	- Python Dependencies:  
		- datetime
		- time

###### TSN Abstracter (TSNA) © 2025-2026 by Ascellayn / The Sirio Network is licensed under TSN License 2.1 - Base
"""
from . import Config;
from . import App;
from . import Deco;
from . import Log;
from . import File;
from . import Misc;
from . import Safe;
from . import TSNDL;
from . import String;
from . import Time;


from typing import Any, Literal, Optional, NotRequired, TypedDict, assert_type, cast;
from collections.abc import Callable;





unix_t = Time.unix_t;








class TSNA:
	"""Class containing some information about TSN_Abstracter & Version Checking
	Yes this looks like a mess."""
	VERSION: tuple[int, int, int] = (7,0,0);





	class __VersionBad(Exception):
		def __init__(self, Message: str, QUIT: bool):
			self.Message: str = Message;
			Log.Critical(self.Message);
			if (QUIT): exit();
		def __str__(self) -> str: return self.Message;

	class __Outdated(__VersionBad):
		def __init__(self, Asked: tuple[int, int, int], QUIT: bool):
			super().__init__(f"{App.Codename} is asking for TSN Abstracter {TSNA.version(Asked)} but TSNA {TSNA.version()} is outdated!", QUIT);

	class __Breaking(__VersionBad):
		def __init__(self, Asked: tuple[int, int, int], QUIT: bool):
			super().__init__(f"{App.Codename} is asking for TSN Abstracter {TSNA.version(Asked)} but TSNA {TSNA.version()} is too new!", QUIT);





	@staticmethod
	def version(VERSION: tuple[int, int, int] | None = None) -> str:
		""" Returns a v.X.Y.Z string of the current TSN Abstracter Version (or of a provided Version Tuple) """
		return f"v{".".join(String.ify_Array(TSNA.VERSION if (not VERSION) else VERSION))}";



	@staticmethod
	def require(MINIMUM: tuple[int, int, int], QUIT: bool = True) -> bool:
		"""Returns a boolean confirming if the TSN_Abstracter version provided by the MINIMUM tuple is equal or above, if QUIT is True the program will quit after the exception."""
		try:
			if ((TSNA.VERSION[0] == MINIMUM[0] and TSNA.VERSION[1] >= MINIMUM[1])):
				if (TSNA.VERSION[1] == MINIMUM[1]):
					if (TSNA.VERSION[2] >= MINIMUM[2]): return True;
			elif (TSNA.VERSION[0] >= MINIMUM[0]): raise TSNA.__Breaking(MINIMUM, QUIT);
			elif (QUIT): raise TSNA.__Outdated(MINIMUM, QUIT);
			else: Log.Warning(f"{App.Codename} is asking for TSN Abstracter {TSNA.version(MINIMUM)} however we're using {TSNA.version()}!");
		except TSNA.__Breaking, TSNA.__Outdated:
			Log.Stateless(f"You may ignore this error, however we do not guarantee that the program will function correctly.\nPress any key to continue.");
			input();
		return False;





	@staticmethod
	def denyImport() -> None:
		"""If your TSNA-Based Application does not support being imported as a Python Module run this when `(__name__ != "__main__")`, this will quit the application with exit code 126."""
		Log.Critical(f"{App.Name} does not support being imported as a Python Module. Exiting!"); exit(126);



	@staticmethod
	def init(Clear_Console: bool = False) -> None:
		"""When your TSNA-Based Application runs, use this command to print basic information about your Application. (When `(__name__ == "__main__")`)  
		Provides a single argument to specify if we should clear the console on the App's successful launch."""
		TSNA.require(App.TSNA, False);
		if (Clear_Console): Log.Clear();
		Log.Stateless(f"{App.Name} {App.Branch} {App.version()} © ({App.Year}) - {", ".join(App.Author)} | {App.License}\n{App.Description}");










__all__ = [
	"App", "Deco", "Config", "File", "Log", "Misc", "Safe", "TSNDL", "String", "Time",
	"TSNA",
	"Any", "Literal", "Optional", "NotRequired", "TypedDict", "Callable",
	"unix_t",
	"assert_type", "cast"
];