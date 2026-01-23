"""
**TSN Abstracter (alias TSNA or "The Sirio Network Abstracter") is a Python Module designed to accomplish relatively common tasks.**  

It was created during Kosaka's v2.X Versions and as its "Dependencies.py" file kept being ported over to other Python projects, TSNA was created to avoid sloppily copy pasting reused code and simplify the process of writing code.  
You are entirely on your own for figuring out what TSNA does and what functions would be useful in your use case. TSNA was purposefully built to build programs for TSN, as such no feature requests will be accepted, unless they're contributing to the function of a TSN Service.  

#### NOTICE: TSNA is only expected to be  import fromed TSN_Abstracter from  import *;` theory could work to just from  import exactly need, but this hasn't been tested extensively.

### Available Modules:
- App  
- Config  
- Cryptography  
	- TSNA Dependencies:  
		- Log
	- Python Dependencies:  
		- hashlib
- Log  
	- TSNA Dependencies:  
		- Config
		- File
		- SNDL
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
- SNDL  
	- TSNA Dependencies:  
		- Config
- String
- Time
	- TSNA Dependencies:  
		- String
	- Python Dependencies:  
		- datetime
		- time

###### TSN Abstracter (TSNA) © 2025-2026 by Ascellayn / The Sirio Network is licensed under TSN License 2.1 - Base
"""





from . import App;
from . import Config;
from . import Log;
from . import File;
from . import Misc;
from . import Safe;
from . import SNDL;
from . import String;
from . import Time;
from typing import Any, TypedDict;





class TSN_Abstracter:
	"""Class containing some information about TSN_Abstracter & Version Checking
	Yes this looks like a mess."""
	Version_Tuple: tuple[int, int, int] = (6,0,0);



	class Bad_Version(Exception):
		def __init__(self, Message: str, Quit_Program: bool):
			self.Message: str = Message;
			Log.Critical(self.Message);
			if (Quit_Program): exit();
		def __str__(self) -> str: return self.Message;

	class Outdated_Version(Bad_Version):
		def __init__(self, Asked: tuple[int, int, int], Quit_Program: bool):
			super().__init__(f"{App.Codename} is asking for TSN Abstracter {TSN_Abstracter.Version(Asked)} but TSNA {TSN_Abstracter.Version()} is outdated!", Quit_Program)

	class Breaking_Version(Bad_Version):
		def __init__(self, Asked: tuple[int, int, int], Quit_Program: bool):
			super().__init__(f"{App.Codename} is asking for TSN Abstracter {TSN_Abstracter.Version(Asked)} but TSNA {TSN_Abstracter.Version()} is too new!", Quit_Program)



	@staticmethod
	def Version(Version: tuple[int, int, int] | None = None) -> str:
		"""Returns a v.X.Y.Z string of the current TSN_Abstracter Version (or of a provided Version Tuple)"""
		if (Version == None): Version = TSN_Abstracter.Version_Tuple;
		return f"v{".".join(str(INT) for INT in Version)}";


	@staticmethod
	def Require_Version(Minimum_Version: tuple[int, int, int], Quit_Program: bool = True) -> bool:
		"""Returns a boolean confirming if the TSN_Abstracter version provided by the Minimum_Version tuple is equal or above, if Quit_Program is True the program will quit after the exception."""
		if ((TSN_Abstracter.Version_Tuple[0] == Minimum_Version[0] and TSN_Abstracter.Version_Tuple[1] >= Minimum_Version[1])):
			if (TSN_Abstracter.Version_Tuple[1] == Minimum_Version[1]):
				if (TSN_Abstracter.Version_Tuple[2] >= Minimum_Version[2]): return True;
		elif (TSN_Abstracter.Version_Tuple[0] >= Minimum_Version[0]): raise TSN_Abstracter.Breaking_Version(Minimum_Version, Quit_Program);
		elif (Quit_Program): raise TSN_Abstracter.Outdated_Version(Minimum_Version, Quit_Program);
		else: Log.Warning(f"{App.Codename} is asking for TSN Abstracter {TSN_Abstracter.Version(Minimum_Version)} however we're using {TSN_Abstracter.Version()}!");
		return False;



	@staticmethod
	def Import_Unsupported() -> None:
		"""If your TSNA-Based Application does not support being imported as a Python Module run this when `(__name__ != "__main__")`, this will quit the application with exit code 126."""
		Log.Critical(f"{App.Name} does not support being imported as a Python Module. Exiting!"); exit(126);



	@staticmethod
	def App_Version() -> str:
		"""Returns a readable string of the TSNA-Based Application Version."""
		return f"v{App.Version_Prefix}{".".join(str(INT) for INT in App.Version)}{App.Version_Prefix}";


	@staticmethod
	def App_Init(Clear_Console: bool = False) -> None:
		"""When your TSNA-Based Application runs, use this command to print basic information about your Application. (When `(__name__ == "__main__")`)  
		Provides a single argument to specify if we should clear the console on the App's successful launch."""
		TSN_Abstracter.Require_Version(App.TSNA);
		if (Clear_Console): Log.Clear();
		Log.Stateless(f"{App.Name} {App.Branch} {TSN_Abstracter.App_Version()} © ({App.License_Year}) - {", ".join(App.Author)} | {App.License}\n{App.Description}");


	@staticmethod
	def App_Info() -> dict[str, Any]:
		"""Retrieve the Application's full information inside a Dictionary. Intended to be used when your TSNA-Based Application is imported as a Python Module."""
		return {
			"Name": App.Name, "Description": App.Description,
			"Author": App.Author, "Contributors": App.Contributors,
			"License": App.License, "License_Year": App.License_Year,
			"Codename": App.Codename, "Branch": App.Branch, "Version": App.Version,
			"TSNA": App.TSNA
		};









__all__ = [
	"App",
	"Config",
	"File",
	"Log",
	"Misc",
	"Safe",
	"SNDL",
	"String",
	"Time",
	"TSN_Abstracter",
	"Any", "TypedDict"
];