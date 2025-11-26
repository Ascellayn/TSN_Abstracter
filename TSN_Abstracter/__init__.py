"""
**TSN Abstracter (alias TSNA or "The Sirio Network Abstracter") is a Python Module designed to accomplish relatively common tasks.**  

It was created during Kosaka's v2.X Versions and as its "Dependencies.py" file kept being ported over to other Python projects, TSNA was created to avoid sloppily copy pasting reused code and simplify the process of writing code.  
You are entirely on your own for figuring out what TSNA does and what functions would be useful in your use case. TSNA was purposefully built to build programs for TSN, as such no feature requests will be accepted, unless they're contributing to the function of a TSN Service.  

#### NOTICE: TSNA is only expected to be imported using `from TSN_Abstracter import *;`
It in theory could work to just import exactly what you need, but this hasn't been tested extensively.

### Available Modules:
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

###### TSN Abstracter (TSNA) © 2025 by Ascellayn is licensed under TSN License 1.0 - Base
"""





import TSN_Abstracter.Config as Config;
import TSN_Abstracter.Log as Log;
import TSN_Abstracter.File as File;
import TSN_Abstracter.Misc as Misc;
import TSN_Abstracter.Safe as Safe;
import TSN_Abstracter.SNDL as SNDL;
import TSN_Abstracter.String as String;
import TSN_Abstracter.Time as Time;
__all__ = [
	"Config",
	"File",
	"Log",
	"Misc",
	"Safe",
	"SNDL",
	"String",
	"Time",
	"TSN_Abstracter"
];





class TSN_Abstracter:
	"""Class containing some information about TSN_Abstracter & Version Checking
	Yes this looks like a mess."""
	Version_Tuple: tuple[int, int, int] = (5,3,0);
	
	class Bad_Version(Exception):
		def __init__(self, Message: str, Quit_Program: bool):
			self.Message: str = Message;
			Log.Critical(self.Message);
			if (Quit_Program): exit();
		def __str__(self) -> str: return self.Message;

	class Outdated_Version(Bad_Version):
		def __init__(self, Asked: tuple[int, int, int], Quit_Program: bool):
			super().__init__(f"The program is asking us TSN_Abstracter {TSN_Abstracter.Version(Asked)} but TSNA {TSN_Abstracter.Version()} is outdated!", Quit_Program)

	class Breaking_Version(Bad_Version):
		def __init__(self, Asked: tuple[int, int, int], Quit_Program: bool):
			super().__init__(f"The program is asking us TSN_Abstracter {TSN_Abstracter.Version(Asked)} but TSNA {TSN_Abstracter.Version()} is too new!", Quit_Program)

	@staticmethod
	def Version(Version: tuple[int, int, int] | None = None) -> str:
		"""Returns a v.X.Y.Z string of the current TSN_Abstracter Version (or of a provided Version Tuple)"""
		if (Version == None): Version = TSN_Abstracter.Version_Tuple;
		return f"v{Version[0]}.{Version[1]}.{Version[2]}";

	@staticmethod
	def Require_Version(Minimum_Version: tuple[int, int, int], Quit_Program: bool = True) -> bool:
		"""Returns a boolean confirming if the TSN_Abstracter version provided by the Minimum_Version tuple is equal or above, if Quit_Program is True the program will quit after the exception."""
		if ((TSN_Abstracter.Version_Tuple[0] == Minimum_Version[0] and TSN_Abstracter.Version_Tuple[1] >= Minimum_Version[1])):
			if (TSN_Abstracter.Version_Tuple[1] == Minimum_Version[1]):
				if (TSN_Abstracter.Version_Tuple[2] >= Minimum_Version[2]): return True;
		elif (TSN_Abstracter.Version_Tuple[0] >= Minimum_Version[0]): raise TSN_Abstracter.Breaking_Version(Minimum_Version, Quit_Program);
		elif (Quit_Program): raise TSN_Abstracter.Outdated_Version(Minimum_Version, Quit_Program);
		else: Log.Warning(f"The program is asking us TSN_Abstracter {TSN_Abstracter.Version(Minimum_Version)} however we're using {TSN_Abstracter.Version()}!");
		return False;

