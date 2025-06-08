import TSN_Abstracter.Config as Config;
import TSN_Abstracter.File as File;
import datetime, inspect, logging, os, shutil, sys;

# My hope is that the "await" status system is so fucking bad that I'm NEVER EVER ALLOWED TO TOUCH PYTHON CODE IN MY ENTIRE LIFE EVER AGAIN
Last_Awaited = False;
Last_Text = "";

Default_Path = os.getcwd(); # Move this later to File.*

""" Note: All the ANSI Colors and everything here are purposeful shit because they're compatible with Discord's ANSI ones. (of which they are shit)
In the future if I have time I will add more colors which would better fit SNDL's Colors. """
class TF():
	# Text Format
	Normal = "\u001b[0m";
	Bold = "\u001b[1m";
	Underline = "\u001b[4m";

class FC():
	# Foreground Color
	Red = "\u001b[31m";
	Yellow = "\u001b[33m";
	Green = "\u001b[32m";
	Cyan = "\u001b[36m";
	Blue = "\u001b[34m";
	Magenta = "\u001b[35m";
	Grey = "\u001b[30m";
	White = "\u001b[37m";

class BC():
	# Background Color
	Orange = "\u001b[41m";
	Indigo = "\u001b[45m";
	Firefly_Dark_Blue = "\u001b[40m";
	Marble_Blue = "\u001b[42m";
	Greyish_Turquoise = "\u001b[43m";
	Grey = "\u001b[44m";
	Light_Grey = "\u001b[46m";
	White = "\u001b[47m";

class Awaited_Log:
	""" Object used to update the "status" of the log specified. Prevents conflicts across threads at the inconvenience of using this object to correctly render logs.  
	Call the following methods to replace "..." to:  
	.OK() -> "[OK]"  
	.ERROR(Exception) -> "[ERROR] \n\t EXCEPTION: {Exception}"  
	Status_Update(Status) -> "{Status}"
	"""
	def __init__(self, Level: int, Caller: str, Text: str) -> None:
		self.Level = Level;
		self.Text = Text;
		self.Caller = Caller;
	
	def __str__(self) -> str:
		return f"{self.Level}: {self.Caller}() - {self.Text}";

	def Status_Update(self, Status: str) -> None:
		"""
		Replaces the last 3 characters (which are assumed to be "...", done automatically) with {Text}. Used to show progress with statuses such as "[OK]".  
		This functions handles also making changes to the Log file, although the assumed "..." will NOT be removed.
		"""
		global Last_Awaited;
		if (Last_Awaited and Last_Text == self.Text):
			print(f"\033[3D {Status}");
			if (Config.Logging["File"] and (self.Level >= Config.Logging["File_Level"])):
				Logger = logging.getLogger("TSN");
				Logger.handlers.clear();
				Logger.addHandler(logging.FileHandler(filename=f"logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log"))
				Logger.log(msg=f" {Status}", level=self.Level)
		else:
			Log(self.Text.replace("...", f" {Status}"), self.Level, self.Caller);
		Last_Awaited = False;

	def OK(self) -> None:
		""" [OK] Status Update shortcut"""
		self.Status_Update(f"{FC.Green}[OK]{TF.Normal}");

	def ERROR(self, Except: Exception) -> None:
		""" [ERROR] Status Update shortcut"""
		self.Status_Update(f"{FC.Red}[ERROR]{TF.Normal}\n{BC.Indigo}{FC.White}\t{TF.Underline}EXCEPTION:{TF.Normal}{BC.Indigo}{FC.White} {Except}{TF.Normal}");

class Empty_Log:
	""" Version of Awaited_Log that contains nothing, used to prevent exceptions when the users' code expects Awaited_Log but the log level is too low  
	Contains the same methods as Awaited_Log but they all do absolutely nothing. """
	def __init__(self) -> None:
		return;

	def __str__(self) -> str:
		return f"Empty";

	def Status_Update(self, Status: str) -> None:
		return;

	def OK(self) -> None:
		return;
	def ERROR(self, Except: Exception) -> None:
		return;

# Simplified logging functions
def Debug(Text: str) -> Awaited_Log:
	""" Debug Log """
	return Log(Text, 10);

def Info(Text: str) -> Awaited_Log:
	""" Info Log """
	return Log(Text, 20);

def Warning(Text: str) -> Awaited_Log:
	""" Warning Log """
	return Log(Text, 30);

def Error(Text: str) -> Awaited_Log:
	""" Error Log """
	return Log(Text, 40);

def Critical(Text: str) -> Awaited_Log:
	""" Critical Log """
	return Log(Text, 50);

def Log_Path() -> str:
	f"{Default_Path}/logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log";

def Log(Text: str, Level: int = 0, Caller: str = "") -> Awaited_Log | Empty_Log:
	""" Logs a specified message manually. Writes the log to a file and displays it to the console.

	Arguments:
		Text: String corresponding to the message to Log
		Level: Integer corresponding to how severe the message is.
	TODO:
		- Add config to prevent generation of logs
		- Make Logger Global so we don't have to redeclare EVERY TIME this shit
	"""
	if (Level < Config.Logging["Print_Level"] and Level < Config.Logging["File_Level"]):
		return Empty_Log(); # Stop execution if the log isn't gonna display anywhere

	# We edit these global variables so that using Status_Update() is much less painful on the "user" side.
	global Last_Awaited, Last_Text;

	# Check if the Logs folder doesn't exist, create it if it isn't. Assuming it is allowed to do so.
	if (Config.Logging["File"]):
		File.Path_Require("logs");
	
	# Configure Logger
	Logger = logging.getLogger("TSN");
	Logger.setLevel(Level);

	# Handlers
	Handlers = [];
	Logger.handlers.clear(); # Clearing handlers otherwise the fucking conditions compared to the config never work?????

	if (Level >= Config.Logging["Print_Level"]): # If this is a debug message, don't display to the console.
		Handlers.append(logging.StreamHandler(stream=sys.stdout));
	if (Config.Logging["File"] and (Level >= Config.Logging["File_Level"])):
		Handlers.append(logging.FileHandler(filename=Log_Path()));
	
	# Get function name that called the logger
	if (Caller == ""):
		Caller = Get_Caller(3);
	
	# Detects if the logged text is going to await a status update and changes the terminator accordingly, includes prefix.
	Prefix = "\n" if (Last_Awaited) else "";
	Terminator = "\n";
	Return = False;
	if (Text != None): # Avoids Exception if Text is None which actually can happen due to coding errors on whichever script is using this module
		if ("..." == Text[-3:]):
			Terminator = "";
			Last_Awaited = True;
			Last_Text = Text;
			Return = True;
		else:
			Last_Awaited = False;


	match Level:
		case 50: Level_Color = FC.Magenta; # Critical 
		case 40: Level_Color = FC.Red; # Error 
		case 30: Level_Color = FC.Yellow; # Warning
		case 20: Level_Color = FC.Blue; # Information
		case 10: Level_Color = FC.Cyan; # Debug
		case _: Level_Color = FC.White;

	Format = logging.Formatter(
		fmt = f"{Prefix}{FC.Grey}[%(asctime)s]{TF.Normal} - {TF.Bold}{Level_Color}%(levelname)s{TF.Normal}: %(message)s", 
		datefmt = "%Y/%m/%d - %H:%M:%S"
	);

	for Handler in Handlers:
		Handler.terminator = Terminator;
		Handler.setFormatter(Format);
		Logger.addHandler(Handler);

	Logger.log(Level, f"{TF.Underline}{FC.Grey}{Caller}(){TF.Normal} - {Text}");
	if (Return):
		return Awaited_Log(Level, Caller, Text);
	else:
		return Empty_Log();

# Logging Dependencies
def Get_Caller(Depth: int = 2) -> str:
	 """ Gives the name of the function who called the function where this function is executed OR the filename where the function was executed if the function returned is "<module>".

	 Arguments:
		Depth: Integer representing how far we go back to get the function name. By default it is 2.
	 Returns:
		String with the name of the function or module name.
	 """
	 Function = inspect.getouterframes(inspect.currentframe())[Depth][3];
	 if (Function == "<module>"):
		 Function = __name__;
	 return Function;

# Miscellaneous Logging
def Carriage(Text: str) -> None:
	"""
	Prints using "\r" while also completely clearing the line to be sure there won't be artifacts from the previous text.
	"""
	global Last_Awaited;
	Last_Awaited = False;
	print(" "*shutil.get_terminal_size()[0], end="\r");
	print(Text, end="\r");

def Clear() -> None:
	"""
	Simply empties the entire console's text.
	"""
	print(f"\033[2J");

def Delete() -> None:
	"""
	COMPLETELY Empties the latest Log File.
	"""
	Clear();
	Critical("=== DELETING THE LOG FILE! ===");
	File.Write(f"logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log", "");