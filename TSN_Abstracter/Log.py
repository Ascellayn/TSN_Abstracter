"""
This module from TSN Abstracter contains various random functions that currently do not deserve their own dedicated TSNA Module.

## Examples
>>> from TSN_Abstracter import Log;
>>> def MyFunction() -> None: Log.Info(f"Hello World!");
>>> MyFunction();
[2007/04/23 - 17:00:00] - Info: MyFunction → Hello World!
"""
from . import Config;
from . import File;
from . import SNDL;
from . import String;
from . import Time;
import datetime, inspect, logging, shutil, sys;





def Log_Path() -> str:
	""" Get the path to where all the Log Files are located. 
	
	Returns:
		str: A relative path to the Log Files Folder.
	"""
	# Check if the Logs folder doesn't exist, create it if it isn't, only if File Logging is enabled.
	if (Config.Logger.File): File.Path_Require(Config.Logger.File_Folder);
	return f"{File.Main_Directory}/{Config.Logger.File_Folder}/{datetime.datetime.now().strftime("%Y-%m_%d")}.log";

# Configure Loggers
Logger_Console = logging.getLogger("TSN-Console"); Logger_Console.addHandler(logging.StreamHandler(stream=sys.stdout));
Logger_File = logging.getLogger("TSN-File");



def Verify_Config() -> None:
	""" Internal Logging Function used to re-add the File Handler when the TSNA Configuration updates. """
	global Logger_File;
	if (Config.Logger.File and not Config.Logger.Disable):
		Logger_File.handlers = [logging.FileHandler(filename=Log_Path())];
		File.Path_Require(Config.Logger.File_Folder);
	else: Logger_File.handlers = []





# Logging Dependencies
def Can_Log(Level: int) -> bool:
	""" Returns if a Log can be display anywhere according to its importance level and TSNA's Config.

	Arguments:
		Level (int*): Integer corresponding to how severe the message is.

	Returns:
		bool: Whenever the Log Level and TSNA's Config can allow Logging to either the Console or File.
	"""
	if (
		Config.Logger.Disable
		or
		(Level < Config.Logger.Print_Level and Level < Config.Logger.File_Level)
	): return False;
	return True;



def Get_Caller(Depth: int = 2) -> str:
	""" Gives the name of the function who called the function where this function is executed OR the filename where the function was executed if the function returned is "module".

	Arguments:
		Depth (int = 2): How far we go back to get the function name.

	Returns:
		str: The name of the function or module name.
	"""
	Function = inspect.getouterframes(inspect.currentframe())[Depth][3];
	if (Function == "<module>"):
		Function = __name__;
	return Function;





# Awaited Logging System
class Awaited_Log:
	""" The Awaited Log System permits TSNA Programs to update the status of Log Entries dynamically.  
	They're used primarily for confirming the end of loading something.  

	Awaited Logs are automatically created when Log Entries end with "...", changing the status of the log will replace said ellipsis with the new status.
	"""
	def __init__(self, Level: int, Caller: str, Text: str) -> None:
		self.Level = Level;
		self.Caller = Caller;

		if (Text[-4:] == " ..."): self.Text = Text[:-3];
		else: self.Text = Text[:-3] + " ";

	def __str__(self) -> str:
		return f"{self.Level}: {self.Caller}() - {self.Text}";

	def Status_Update(self, Status: str) -> None:
		""" Replace the "..." part of the Awaited Log with the status of your choosing.

		Arguments:
			Status (str*): The custom status to replace the ellipsis with.

		Examples:
			>>> Log.Info("Cooking Ascellayn...");
			[2016/05/20 - 17:00:00] - Info: Arellayn → Cooking Ascellayn...
			>>> Log.Awaited.Status_Update("[COOKED]");
			[2016/05/20 - 17:00:00] - Info: Arellayn → Cooking Ascellayn [COOKED]
		"""
		global Awaited_Logs, Awaited_Console, Awaited_File;
	
		if (Can_Log(self.Level)):
			# Update Console Log Entry
			if (self.Level >= Config.Logger.Print_Level):
				if (Awaited_Console == self.Caller):
					Logger_Console.log(self.Level, String.ASCII.Line.Return + self.Text + Status);

					Awaited_Console = None;
				else: Logger_Console.log(self.Level, self.Text + Status);

			# Update File Log Entry
			Verify_Config();
			if (Config.Logger.File and (self.Level >= Config.Logger.File_Level)):

				# Check if we can easily overwrite the last line
				if (Awaited_File == self.Caller):
					# WARNING: This is slow, should come up with a better solution in the future
					Lines: list[str] = open(Log_Path(), "r").readlines();
					Lines[-1] = String.Clear_ASCII_Formatting(self.Text + Status + "\n");
					open(Log_Path(), "w").writelines(Lines);

					Awaited_File = None;
				else: Logger_File.log(self.Level, String.Clear_ASCII_Formatting(self.Text + Status));


		del Awaited_Logs[self.Caller];

	def OK(self, Status: str | None = None) -> None:
		""" >>> Log.Awaited.OK();
		[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [OK] """
		self.Status_Update(f"{SNDL.Log_Color("Green")}[OK{f": {Status}" if (Status) else ""}]{String.ASCII.Text.Reset}");

	def ERROR(self, Error: str) -> None:
		""" >>> Log.Awaited.ERROR();
		[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [ERROR] """
		self.Status_Update(f"{SNDL.Log_Color("Red")}[ERROR]{String.ASCII.Text.Reset}\n{String.ASCII.Shortcut.BSOD}{Error}{String.ASCII.Text.Reset}");

	def EXCEPTION(self, Except: Exception, Raise: bool = False) -> None:
		""" >>> Log.Awaited.EXCEPTION(Except);
		[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [EXCEPTION]
		Cannot divide by zero.
		"""
		self.Status_Update(f"{SNDL.Log_Color("Orange")}[EXCEPTION]{String.ASCII.Text.Reset}\n{String.ASCII.Shortcut.BSOD}{Except}{String.ASCII.Text.Reset}");
		if (Raise): raise Except;


class Awaited_Dummy(Awaited_Log):
	""" An Awaited Log that doesn't do anything, to be used when the Caller doesn't correspond to the awaited one. """
	def __init__(self): return;
	def __str__(self): return "";
	def Status_Update(self, Status: str): return;
	def OK(self, Status: str | None = None): return;
	def ERROR(self, Error: str): return;
	def EXCEPTION(self, Except: Exception, Raise: bool = False): return;

def Awaited(Custom_Caller: str | None = None) -> Awaited_Log | Awaited_Dummy:
	""" Get the latest Awaited Log, you may specify a Custom Caller if you wish to handle the Log of another function.
	
	Arguments:
		Custom_Caller (str | None = None): The name of the caller.

	Returns:
		Awaited_Log/Awaited_Dummy: The corresponding Log Object or a Dummy one if it wasn't found.

	"""
	Caller: str = Get_Caller() if (not Custom_Caller) else Custom_Caller;
	if (Caller in Awaited_Logs.keys()):
		return Awaited_Logs[Caller];
	return Awaited_Dummy();


# My hope is that the "await" status system is so fucking bad that I'm NEVER EVER ALLOWED TO TOUCH PYTHON CODE IN MY ENTIRE LIFE EVER AGAIN
Awaited_Logs: dict[str, Awaited_Log] = {};
Awaited_Console: str | None = None;
Awaited_File: str | None = None;



# Simplified logging functions
def TSN_Debug(Text: str) -> None:
	""" Log a debug message for **Libraries** *(Level: 10)*.

	Arguments:
		Text (str*): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.TSN_Debug(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - TSN_Debug: MyFunction → Hello World!
	"""
	Log(Text, 10);

def Debug(Text: str) -> None:
	""" Log a debug message for **TSNA Programs** *(Level: 15)*.

	Arguments:
		Text (str*): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.Debug(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Debug: MyFunction → Hello World!
	"""
	Log(Text, 15);

def Stateless(Text: str) -> None:
	""" Log a message with only the time if it's enabled *(Level: 20)*.

	Arguments:
		Text (str*): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.Stateless(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Hello World!
	"""
	Log(Text, 20);

def Info(Text: str) -> None:
	""" Log a standard informal message *(Level: 25)*.

	Arguments:
		Text (str*): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.Info(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Info: MyFunction → Hello World!
	"""
	Log(Text, 25);

def Warning(Text: str) -> None:
	""" Log a standard warning message *(Level: 30)*.

	Arguments:
		Text (str*): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.Warning(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Warning: MyFunction → Hello World!
	"""
	Log(Text, 30);

def Error(Text: str) -> None:
	""" Log a standard error message *(Level: 40)*.

	Arguments:
		Text (str*): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.Error(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Error: MyFunction → Hello World!
	"""
	Log(Text, 40);

def Critical(Text: str) -> None:
	""" Log a standard critical message *(Level: 50)*.

	Arguments:
		Text (str*): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.Critical(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Critical: MyFunction → Hello World!
	"""
	Log(Text, 50);





# The actual logging function
def Log(Text: str, Level: int = 0, Caller: str = "") -> None:
	""" Log a message depending on its Level, logging the Caller and Time if it was enabled or is possible into the Python Console or a File according to the TSNA Config.
	#### **DO NOT USE THIS FUNCTION DIRECTLY, USE THE FUNCTIONS SUCH AS Log.Info()!**  

	Arguments:
		Text (str*): String corresponding to the message to Log.
		Level (int = 0): Integer corresponding to how severe the message is.
		Caller (str = ""): Enforce the displayed function that called the Logger, if left empty, automatically figure out who called the Logger.
	
	Examples:
		>>> Log.Log("Hug a Mika a day, keeps your sanity away~", 30, "Ascellayn");
		[2007/04/23 - 17:00:00] - Warning: Ascellayn → Hug a Mika a day, keeps your sanity away~
	"""
	global Awaited_Logs, Awaited_Console, Awaited_File, Logger_File # Awaiting Log System Bullshit & Janky bug fix for date issues
	if (not Can_Log(Level)): return;



	match Level:
		case 50: Level_Color = SNDL.Log_Color("Purple"); Level_String = String.ASCII.Text.Blink + "Critical" + String.ASCII.Text.Blink_OFF;
		case 40: Level_Color = SNDL.Log_Color("Red"); Level_String = String.ASCII.Text.Blink + "Error" + String.ASCII.Text.Blink_OFF;
		case 30: Level_Color = SNDL.Log_Color("Yellow"); Level_String = "Warning";
		case 25: Level_Color = SNDL.Log_Color("Blue"); Level_String = "Info";
		case 20: Level_Color = SNDL.Log_Color("White"); Level_String = "Stateless";
		case 15: Level_Color = SNDL.Log_Color("Cyan"); Level_String = "Debug";
		case 10: Level_Color = SNDL.Log_Color("Green"); Level_String = "TSN_Debug";
		case _: Level_Color = SNDL.Log_Color("White"); Level_String = "Unknown";
	Logger_Console.setLevel(Level); Logger_File.setLevel(Level);

	# Get function name that called the logger
	if (Caller == ""): Caller = Get_Caller(3);
	
	# Detects if the logged text is going to await a status update and changes the terminator accordingly, includes prefix.
	if (len(Text) >= 3): # Avoids Exception if Text is too short
		if ("..." == Text[-3:]):
			if (Level >= Config.Logger.Print_Level): Awaited_Console = Caller;
			if (Level >= Config.Logger.File_Level): Awaited_File = Caller;



	# Log Message Formatting
	Date_Str, Time_Str = Time.Get_DateStrings(Time.Get_Unix());
	Logged_Text: str = ""; # Prefix if previous log was Awaited

	if (Config.Logger.Display_Date): Logged_Text += f"{SNDL.Log_Color("Grey")}[{Date_Str} - {Time_Str}]{String.ASCII.Text.Reset} - "; # Date

	if (Level != 20): # Check for Stateless before adding Caller
		Logged_Text += f"{String.ASCII.Text.Bold}{Level_Color}{Level_String}{String.ASCII.Text.Reset}: "; # Log Level
		if (Config.Logger.Display_Caller): Logged_Text += f"{String.ASCII.Text.Underline}{SNDL.Log_Color("Grey")}{Caller}{String.ASCII.Text.Reset} → ";

	Logged_Text += Text; # Finally add the actual message we want to Log.



	# Verify for both the Console and File if the Level is high enough before logging.
	if (Level >= Config.Logger.Print_Level): Logger_Console.log(Level, Logged_Text);

	Verify_Config();
	if (Config.Logger.File and (Level >= Config.Logger.File_Level)):
		Logger_File.log(Level, String.Clear_ASCII_Formatting(Logged_Text));



	if (Awaited_Console or Awaited_File): Awaited_Logs[Caller] = Awaited_Log(Level, Caller, Logged_Text);





# Miscellaneous Logging
def Carriage(Text: str) -> None:
	""" Print a message that can be overwritten thanks to carriage returns.

	Arguments:
		Text (str*): The message you wish to display and be able to overwrite using the same function.

	Examples:
		>>> for i in range(10): Log.Carriage(i);
		# Every number would be displayed, but obviously they would get overwritten every time this function is run.
	"""
	global Last_Awaited; Last_Awaited = False;

	print(" "*shutil.get_terminal_size()[0], end="\r");
	print(Text, end="\r");

def Clear() -> None:
	""" Clear the console's text without needing to call OS specific commands.

	### Examples
	>>> Log.Clear();
	# The console would then be effectively cleared.
	"""
	print(String.ASCII.Clear_Screen);

def Delete() -> None:
	""" COMPLETELY empties the latest Log File. To be used only during the development & debugging process!

	### Examples
	>>> Log.Delete();
	# [Console gets cleared]
	[2007/04/23 - 17:00:00] - CRITICAL: TSN_Abstracter.Log() → === DELETING THE LOG FILE! ===
	# [Latest Log File emptied]
	"""
	Clear();
	Critical("=== DELETING THE LOG FILE! ===");
	File.Write(Log_Path(), "");