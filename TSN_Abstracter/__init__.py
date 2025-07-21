from TSN_Abstracter.Config import *;
from TSN_Abstracter.Cryptography import *;
from TSN_Abstracter.Log import *;
from TSN_Abstracter.File import *;
from TSN_Abstracter.Misc import *;
from TSN_Abstracter.Safe import *;
from TSN_Abstracter.SNDL import *;
from TSN_Abstracter.String import *;
from TSN_Abstracter.Time import *;

__all__ = [
	"Config",
	"Cryptography",
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
	Version_Tuple: tuple[int] = (2,0,0);
	
	class Bad_Version(Exception):
		def __init__(self, Message: str, Quit_Program: bool):
			self.Message: str = Message;
			Log.Critical(self.Message);
			if (Quit_Program): exit();
		def __str__(self) -> str: return self.Message;

	class Outdated_Version(Bad_Version):
		def __init__(self, Asked: tuple[int], Quit_Program: bool):
			super().__init__(f"The program is asking us TSN_Abstracter {TSN_Abstracter.Version(Asked)} but TSNA {TSN_Abstracter.Version()} is outdated!", Quit_Program)

	class Breaking_Version(Bad_Version):
		def __init__(self, Asked: tuple[int], Quit_Program: bool):
			super().__init__(f"The program is asking us TSN_Abstracter {TSN_Abstracter.Version(Asked)} but TSNA {TSN_Abstracter.Version()} is too new!", Quit_Program)

	def Version(Version: tuple[int] | None = None) -> str:
		"""Returns a v.X.Y.Z string of the current TSN_Abstracter Version (or of a provided Version Tuple)"""
		if (Version == None): Version = TSN_Abstracter.Version_Tuple;
		return f"v{Version[0]}.{Version[1]}.{Version[2]}";
	
	def Require_Version(Minimum_Version: tuple[int], Quit_Program: bool = True) -> bool:
		"""Returns a boolean confirming if the TSN_Abstracter version provided by the Minimum_Version tuple is equal or above, if Quit_Program is True the program will quit after the exception."""
		if ((TSN_Abstracter.Version_Tuple[0] == Minimum_Version[0] and TSN_Abstracter.Version_Tuple[1] >= Minimum_Version[1])): return True;
		elif (TSN_Abstracter.Version_Tuple[0] >= Minimum_Version[0]): raise TSN_Abstracter.Breaking_Version(Minimum_Version, Quit_Program);
		elif (Quit_Program): raise TSN_Abstracter.Outdated_Version(Minimum_Version, Quit_Program);
		else: Log.Warning(f"The program is asking us TSN_Abstracter {TSN_Abstracter.Version(Minimum_Version)} however we're using {TSN_Abstracter.Version()}!");