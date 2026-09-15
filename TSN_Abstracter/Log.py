""" ***Implemented in __TSNA `v7.0.0`__***  

This module from TSN Abstracter contains TSNA's logger and its associated derivative functions related to printing stuff on the screen.

## Examples
>>> from TSN_Abstracter import Log;
>>> def MyFunction() -> None: Log.info(f"Hello World!");
>>> MyFunction();
[2007/04/23 - 17:00:00] - Info: MyFunction → Hello World!
"""
from . import App, Config, File, TSNDL, String, Time;
import datetime, inspect, logging, shutil, sys, traceback;








# Configure Loggers
CONSOLE: logging.Logger = logging.getLogger("TSN-Console"); CONSOLE.addHandler(logging.StreamHandler(stream=sys.stdout));
FILE: logging.Logger = logging.getLogger("TSN-File");



# My hope is that the "await" status system is so fucking bad that I'm NEVER EVER ALLOWED TO TOUCH PYTHON CODE IN MY ENTIRE LIFE EVER AGAIN
	# v7.0.0: god damn it the awaited status system is kinda good... look what you've done past me, how dare you
Statuses: dict[str, list[Status]] = {};
Status_Console: str | None = None;
Status_File: str | None = None;








def __updateFile() -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Internal Logging Function used to re-add the File Handler when the TSNA Configuration updates.  
	This is unfortunately required in other to deal with the log file not properly updating when the date changes.
	"""
	global FILE;
	if (Config.Logger.File and not Config.Logger.Disable):
		FILE.handlers = [logging.FileHandler(filename=path())];
		File.Path.require(Config.Logger.File_Folder);
	else: FILE.handlers = [];








# Logging Dependencies
def path() -> str:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Get the path to where all the Log Files are located. 
	
	Returns:
		str: A relative path to the Log Files Folder.
	"""
	# Check if the Logs folder doesn't exist, create it if it isn't, only if File Logging is enabled.
	if (Config.Logger.File): File.Path.require(Config.Logger.File_Folder);
	return f"{File.DIRECTORY}/{Config.Logger.File_Folder}/{datetime.datetime.now().strftime("%Y-%m_%d")}.log";



def gable(LEVEL: int) -> bool:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Returns if a Log can be display anywhere according to its importance level and TSNA's Config.

	Arguments:
		Level (int): Integer corresponding to how severe the message is.

	Returns:
		bool: Whenever the Log Level and TSNA's Config can allow Logging to either the Console or File.
	"""
	if (
		Config.Logger.Disable
		or
		(LEVEL < Config.Logger.Print_Level and LEVEL < Config.Logger.File_Level)
	): return False;
	return True;



def caller(Depth: int = 2) -> str:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Gives the name of the function who called the function where this function is executed OR the Application Codename if the caller is found to be the root module.

	Arguments:
		Depth (int = 2): How far we go back to get the function name.

	Returns:
		str: The name of the function or module name.
	"""
	caller: str = inspect.getouterframes(inspect.currentframe())[Depth][3];
	return App.Codename if (caller == "<module>") else caller;










# Miscellaneous Logging
def clear() -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Clear the console's text without needing to call OS specific commands.

	### Examples
	>>> Log.clear();
	# The console would then be effectively cleared.
	"""
	print(String.ASCII.Clear_Screen);



def delete() -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	COMPLETELY empties the latest Log File. To be used only during the development & debugging process!

	### Examples
	>>> Log.delete();
	# [Console gets cleared]
	[2007/04/23 - 17:00:00] - CRITICAL: TSN_Abstracter.log() → === DELETING THE LOG FILE! ===
	# [Latest Log File emptied]
	"""
	clear();
	crit("=== DELETING THE LOG FILE! ===");
	File.write(path(), "");




def carriage(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Print a message that can be overwritten thanks to carriage returns.

	Arguments:
		Text (str): The message you wish to display and be able to overwrite using the same function.

	Examples:
		>>> for i in range(10): Log.carriage(i);
		# Every number would be displayed, but obviously they would get overwritten every time this function is run.
	"""
	global Last_Awaited; Last_Awaited = False;

	print(" "*shutil.get_terminal_size()[0], end="\r");
	print(TEXT, end="\r");










# Log Status System
class Status:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	The Awaited Log System permits TSNA Programs to update the status of Log Entries dynamically.  
	They're used primarily for confirming the end of loading something.  

	Awaited Logs are automatically created when Log Entries end with "...", changing the status of the log will replace said ellipsis with the new status.
	"""
	def __init__(self, LEVEL: int, CALLER: str, TEXT: str) -> None:
		self.Level: int = LEVEL;
		self.CALLER: str = CALLER;
		self.TEXT = TEXT[:-3] if (TEXT[-4:] == " ...") else TEXT[:-3] + " ";



	def __str__(self) -> str: return f"{self.Level}: {self.CALLER}() - {self.TEXT}";
	def __repr__(self) -> str: return self.__str__();





	def update(self, STATUS: str, LEVEL: int) -> None:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Replace the "..." part of the Awaited Log with the status of your choosing.

		Arguments:
			Status (str): The custom status to replace the ellipsis with.
			Level (int): The logging level of the Status Update itself.

		Examples:
			>>> Log.info("Cooking Ascellayn...");
			[2016/05/20 - 17:00:00] - Info: Arellayn → Cooking Ascellayn...
			>>> Log.Status.update("[COOKED]", 25);
			[2016/05/20 - 17:00:00] - Info: Arellayn → Cooking Ascellayn [COOKED]
		"""
		global Statuses, Status_Console, Status_File;
		do_return: bool = True;

		if (Config.Logger.Awaited_Status):
			if (LEVEL > self.Level and not gable(self.Level)):
				self.Level = LEVEL;
				do_return = False;
		# Displays Awaited Status Changes when they're higher than the initial log

		if (gable(LEVEL)):
			# Update Console Log Entry
			if (self.Level >= Config.Logger.Print_Level):
				if (Status_Console == self.CALLER):
					if (do_return): CONSOLE.log(self.Level, String.ASCII.Line.Return + self.TEXT + STATUS);
					else: CONSOLE.log(self.Level, self.TEXT + STATUS);

					Status_Console = None;
				else: CONSOLE.log(self.Level, self.TEXT + STATUS);

			# Update File Log Entry
			__updateFile();
			if (Config.Logger.File and (self.Level >= Config.Logger.File_Level)):

				# Check if we can easily overwrite the last line
				if (Status_File == self.CALLER and do_return):
					# warn: This is slow, should come up with a better solution in the future
					Lines: list[str] = open(path(), "r").readlines();
					Lines[-1] = String.ASCII.clearFormatting(f"{self.TEXT}{STATUS}\n");
					open(path(), "w").writelines(Lines);

					Status_File = None;
				else: FILE.log(self.Level, String.ASCII.clearFormatting(self.TEXT + STATUS));



	def ok(self, STATUS: str | None = None) -> None:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		>>> Log.Status.ok();
		[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [OK] """
		self.update(f"{TSNDL.Color.log("Green")}[OK{f": {STATUS}" if (STATUS) else ""}]{String.ASCII.Text.Reset}", self.Level);



	def alert(self, STATUS: str | None = None) -> None:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		>>> Log.Status.warn("2 Modules Skipped");
		[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [WARNING: 2 Modules Skipped] """
		self.update(f"{TSNDL.Color.log("Yellow")}[WARNING{f": {STATUS}" if (STATUS) else ""}]{String.ASCII.Text.Reset}", 30);



	def bad(self, STATUS: str | None = None) -> None:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		>>> Log.Status.error("1 Outdated Module");
		[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [ERROR: 1 Outdated Module] """
		self.update(f"{TSNDL.Color.log("Red")}[ERROR{f": {STATUS}" if (STATUS) else ""}]{String.ASCII.Text.Reset}", 40);



	def exception(self, EXCEPTION: Exception, RAISE: bool = False, TRACEBACK: bool = True) -> None:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		>>> Log.Status.exception(Except);
		[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [EXCEPTION]
		Cannot divide by zero.
		"""
		self.update(f"{TSNDL.Color.log("Orange")}[EXCEPTION]{String.ASCII.Text.Reset}\n{String.ASCII.Shortcut.BSOD}{EXCEPTION}{'\n'.join(traceback.format_exception(EXCEPTION)) if (TRACEBACK) else ""}{String.ASCII.Text.Reset}", 50);
		if (RAISE): raise EXCEPTION;





class StatusDummy(Status):
	""" ***Implemented in __TSNA `v7.0.0`__***  

	An Awaited Log that doesn't do anything, to be used when the Caller doesn't correspond to the awaited one.
	"""
	def __init__(self): return;
	def __str__(self): return "";
	def update(self, STATUS: str, LEVEL: int): return;
	def ok(self, STATUS: str | None = None): return;
	def alert(self, STATUS: str | None = None): return;
	def bad(self, STATUS: str | None = None): return;
	def exception(self, EXCEPTION: Exception, RAISE: bool = False, TRACEBACK: bool = True): return;





def status(CALLER: str = caller()) -> Status | StatusDummy:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Get the latest Awaited Log, you may specify a Custom Caller if you wish to handle the Log of another function.  
	Using this function is generally not recommended if you're going to run the usual `.ok()`, `.alert()`, `.bad()` or `.exception()` methods, as doing so here is slower. Only use this function if you know what you're doing.
	
	Arguments:
		CALLER (str = caller()): A custom name for the caller.

	Returns:
		Status/StatusDummy: The corresponding Log Object or a Dummy one if it wasn't found.

	"""
	global Statuses;

	if (CALLER in Statuses.keys()):
		status: Status = Statuses[CALLER].pop();
		if (len(Statuses[CALLER]) == 0): del Statuses[CALLER];
		return status;
	return StatusDummy();



def ok(TEXT: str | None = None, CALLER: str = caller()) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	More optimized shortcut for `Log.status().ok()`.  
	***This functions does nothing if no status logs could be found.***

	Arguments:
		TEXT (str | None = None): Extra text to add after `OK`, pre-appends `: `.
		CALLER (str = caller()): Which function has an active Status Log, can be set to something customized.


	>>> Log.Status.ok();
	[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [OK]
	"""
	statuses: list[Status] | None = Statuses.get(CALLER);
	if (not statuses): return;
	Statuses[CALLER].pop().ok(TEXT);



def alert(TEXT: str | None = None, CALLER: str = caller()) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	More optimized shortcut for `Log.status().alert()`.  
	***This functions does nothing if no status logs could be found.***

	Arguments:
		TEXT (str | None = None): Extra text to add after `WARNING`, pre-appends `: `.
		CALLER (str = caller()): Which function has an active Status Log, can be set to something customized.


	>>> Log.Status.error("1 Outdated Module");
	[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [ERROR: 1 Outdated Module]
	"""
	statuses: list[Status] | None = Statuses.get(CALLER);
	if (not statuses): return;
	Statuses[CALLER].pop().alert(TEXT);



def bad(TEXT: str | None = None, CALLER: str = caller()) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	More optimized shortcut for `Log.status().bad()`.  
	***This functions does nothing if no status logs could be found.***

	Arguments:
		TEXT (str | None = None): Extra text to add after `ERROR`, pre-appends `: `.
		CALLER (str = caller()): Which function has an active Status Log, can be set to something customized.


	>>> Log.Status.warn("2 Modules Skipped");
	[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [WARNING: 2 Modules Skipped]
	"""
	statuses: list[Status] | None = Statuses.get(CALLER);
	if (not statuses): return;
	Statuses[CALLER].pop().bad(TEXT);



def exception(
		EXCEPTION: Exception,
		RAISE: bool = False,
		TRACEBACK: bool = True,
		CALLER: str = caller()
	) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	More optimized shortcut for `Log.status().exception()`.  
	***This functions does nothing if no status logs could be found.***

	Arguments:
		EXCEPTION (Exception): The caught exception to log.
		RAISE (bool = False): Whenever to throw the exception again.
		TRACEBACK (bool = True): Whenever to show a more detailed error on why the exception happened.
		CALLER (str = caller()): Which function has an active Status Log, can be set to something customized.


	>>> Log.Status.exception(Except);
	[2016/05/20 - 17:00:00] - Info: setup_hook → Loading Kosaka [EXCEPTION]
	Cannot divide by zero.
	"""
	statuses: list[Status] | None = Statuses.get(CALLER);
	if (not statuses): return;
	Statuses[CALLER].pop().exception(EXCEPTION, RAISE, TRACEBACK);








# Simplified logging functions
def debugTSN(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a debug message for **Libraries** *(Level: 5)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.debugTSN(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - TSN_Debug: MyFunction → Hello World!
	"""
	log(TEXT, 5);



def debug(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a debug message for **TSNA Programs** *(Level: 10)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.debug(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Debug: MyFunction → Hello World!
	"""
	log(TEXT, 10);



def text(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a message. No extra fancy bells or whistles. *(Level: 15)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.Text(f"Hello World!");
		>>> MyFunction();
		Hello World!
	"""
	log(TEXT, 15);



def stateless(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a message with only the time if it's enabled *(Level: 20)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.stateless(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Hello World!
	"""
	log(TEXT, 20);



def info(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a standard informal message *(Level: 25)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.info(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Info: MyFunction → Hello World!
	"""
	log(TEXT, 25);



def warn(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a standard warning message *(Level: 30)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.warn(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Warning: MyFunction → Hello World!
	"""
	log(TEXT, 30);



def error(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a standard error message *(Level: 40)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.error(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Error: MyFunction → Hello World!
	"""
	log(TEXT, 40);



def crit(TEXT: str) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a standard critical message *(Level: 50)*.

	Arguments:
		Text (str): The string to be displayed in the Log.

	Examples:
		>>> def MyFunction() -> None: Log.crit(f"Hello World!");
		>>> MyFunction();
		[2007/04/23 - 17:00:00] - Critical: MyFunction → Hello World!
	"""
	log(TEXT, 50);





# The actual logging function
def log(TEXT: str, LEVEL: int = 0, CALLER: str = caller(3)) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Log a message depending on its Level, logging the Caller and Time if it was enabled or is possible into the Python Console or a File according to the TSNA Config.
	#### **DO NOT USE THIS FUNCTION DIRECTLY, USE THE FUNCTIONS SUCH AS Log.info()!**  

	Arguments:
		Text (str): String corresponding to the message to Log.
		Level (int = 0): Integer corresponding to how severe the message is.
		Caller (str = caller(3)): Enforce the displayed function that called the Logger, if left empty, automatically figure out who called the Logger.
	
	Examples:
		>>> Log.log("Hug a Mika a day, keeps your sanity away~", 30, "Ascellayn");
		[2007/04/23 - 17:00:00] - Warning: Ascellayn → Hug a Mika a day, keeps your sanity away~
	"""
	global Statuses, Status_Console, Status_File, FILE; # Awaiting Log System Bullshit & Janky bug fix for date issues
	if (not gable(LEVEL) and not Config.Logger.Awaited_Status): return;



	Level_Color: str; Level_String: str;
	match LEVEL:
		case 50: Level_Color = TSNDL.Color.log("Purple"); Level_String = String.ASCII.Text.Blink + "Critical" + String.ASCII.Text.Blink_OFF;
		case 40: Level_Color = TSNDL.Color.log("Red"); Level_String = String.ASCII.Text.Blink + "Error" + String.ASCII.Text.Blink_OFF;
		case 30: Level_Color = TSNDL.Color.log("Yellow"); Level_String = "Warning";
		case 25: Level_Color = TSNDL.Color.log("Blue"); Level_String = "Info";
		case 20: Level_Color = TSNDL.Color.log("White"); Level_String = "Stateless";
		case 15: Level_Color = TSNDL.Color.log("White"); Level_String = "Text";
		case 10: Level_Color = TSNDL.Color.log("Cyan"); Level_String = "Debug";
		case 5: Level_Color = TSNDL.Color.log("Green"); Level_String = "TSN_Debug";
		case _: Level_Color = TSNDL.Color.log("White"); Level_String = "Unknown";
	CONSOLE.setLevel(LEVEL); FILE.setLevel(LEVEL);

	# Detects if the logged text is going to await a status update and changes the terminator accordingly, includes prefix.
	if (TEXT.endswith("...")):
		if (LEVEL >= Config.Logger.Print_Level): Status_Console = CALLER;
		if (LEVEL >= Config.Logger.File_Level): Status_File = CALLER;



	# Log Message Formatting
	log_text: str = "";
	if (LEVEL != 15):
		str_date, str_time = Time.dateStrings(Time.Unix.now());

		if (Config.Logger.Display_Date): log_text += f"{TSNDL.Color.log("Grey")}[{str_date} - {str_time}]{String.ASCII.Text.Reset} - "; # Date

		if (LEVEL != 20): # Check for Stateless before adding Caller
			log_text += f"{String.ASCII.Text.Bold}{Level_Color}{Level_String}{String.ASCII.Text.Reset}: "; # Log Level
			if (Config.Logger.Display_Caller): log_text += f"{String.ASCII.Text.Underline}{TSNDL.Color.log("Grey")}{CALLER}{String.ASCII.Text.Reset} → ";

	log_text += TEXT; # Finally add the actual message we want to Log.



	# Verify for both the Console and File if the Level is high enough before logging. Also refuses to log if the TUI is currently enabled.
	if (LEVEL >= Config.Logger.Print_Level and not Config.System.TUI_Enabled): CONSOLE.log(LEVEL, log_text);

	__updateFile();
	if (Config.Logger.File and (LEVEL >= Config.Logger.File_Level)):
		FILE.log(LEVEL, String.ASCII.clearFormatting(log_text));



	if (CALLER not in Statuses.keys()): Statuses[CALLER] = [];
	Statuses[CALLER].append(Status(LEVEL, CALLER, log_text));