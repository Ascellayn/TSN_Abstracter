import TSN_Abstracter.Config as Config;
import TSN_Abstracter.File as File;
import TSN_Abstracter.Time as Time;
import datetime, inspect, logging, os, re, shutil, sys;

# My hope is that the "await" status system is so fucking bad that I'm NEVER EVER ALLOWED TO TOUCH PYTHON CODE IN MY ENTIRE LIFE EVER AGAIN
Awaited_Logs: dict = {};
Await_Next: bool = False;

def Log_Path() -> str: return f"{File.Working_Directory}/logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log";

# Configure Loggers
Logger_Console = logging.getLogger("TSN-Console"); Logger_Console.addHandler(logging.StreamHandler(stream=sys.stdout));
Logger_File = logging.getLogger("TSN-File"); Logger_File.addHandler(logging.FileHandler(filename=Log_Path()));


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

def Clear_TextFormatting(Text: str) -> str:
	""" This function takes in a String and then clears out all the special Text formatting according to the TF/FC/BC objects. Used for making Log files look cleaner. """
	return re.sub(r"\u001b\[\d*m", "", Text);

def Can_Log(Level: int) -> bool:
	if (Config.Logger.Disable): return False;
	if (Level < Config.Logger.Print_Level and Level < Config.Logger.File_Level): return False; # Stop execution if the log isn't gonna display anywhere
	return True;





""" Note: All the ANSI Colors and everything here are purposeful shit because they're compatible with Discord's ANSI ones. (of which they are shit)
In the future if I have time I will add more colors which would better fit SNDL's Colors. """
class TF:
	"""Text Format"""
	Normal = "\u001b[0m";
	Bold = "\u001b[1m";
	Underline = "\u001b[4m";
	Return_Line = "\x1b[1A\x1b[2K" * 2;

class FC:
	"""Foreground Color"""
	Red = "\u001b[31m";
	Yellow = "\u001b[33m";
	Green = "\u001b[32m";
	Cyan = "\u001b[36m";
	Blue = "\u001b[34m";
	Magenta = "\u001b[35m";
	Grey = "\u001b[30m";
	White = "\u001b[37m";

class BC:
	"""Background Color"""
	Orange = "\u001b[41m";
	Indigo = "\u001b[45m";
	Firefly_Dark_Blue = "\u001b[40m";
	Marble_Blue = "\u001b[42m";
	Greyish_Turquoise = "\u001b[43m";
	Grey = "\u001b[44m";
	Light_Grey = "\u001b[46m";
	White = "\u001b[47m";





# Awaited Logging System
class Awaited_Log:
	"""
	Object used to update the "status" of the log specified. Prevents conflicts across threads at the inconvenience of using this object to correctly render logs.  
	Call the following methods to replace "..." to:  
	.OK() -> "[OK]"  
	.ERROR(Error) -> "[ERROR] \n{Error}"  
	.EXCEPTION(Except) -> "[EXCEPTION] \n{Except}"  
	Status_Update(Status) -> "{Status}"
	"""
	def __init__(self, Level: int, Caller: str, Text: str) -> None:
		self.Level = Level;
		self.Caller = Caller;

		if (Text[-4:] == " ..."): self.Text = Text[:-3];
		else: self.Text = Text[:-3] + " ";

	def __str__(self) -> str:
		return f"{self.Level}: {self.Caller}() - {self.Text}";

	def Status_Update(self, Status: str) -> None:
		"""
		Replaces the last 3 characters (which are assumed to be "...", done automatically) with {Text}. Used to show progress with statuses such as "[OK]".  
		This functions handles also making changes to the Log file, although the assumed "..." will NOT be removed.
		"""
		global Awaited_Logs, Await_Next;
		if (Can_Log(self.Level)):
			if (self.Level >= Config.Logger.Print_Level):
				if (Await_Next): Logger_Console.log(self.Level, TF.Return_Line + self.Text + Status); #print(f"\033[3D {Status}");
				else: Logger_Console.log(self.Level, self.Text + Status);
			if (Config.Logger.File and (self.Level >= Config.Logger.File_Level)):
				Logger_File.log(self.Level, Clear_TextFormatting(self.Text + Status));

		Await_Next = False; del Awaited_Logs[self.Caller];

	def OK(self) -> None:
		""" [OK] Status Update shortcut"""
		self.Status_Update(f"{FC.Green}[OK]{TF.Normal}");

	def ERROR(self, Error: str) -> None:
		""" [ERROR] Status Update shortcut"""
		self.Status_Update(f"{FC.Red}[ERROR]{TF.Normal}\n{BC.Orange}{FC.White}{Error}{TF.Normal}");

	def EXCEPTION(self, Except: Exception, Raise: bool = False) -> None:
		""" [EXCEPTION] Status Update shortcut"""
		self.Status_Update(f"{FC.Blue}[EXCEPTION]{TF.Normal}\n{BC.Indigo}{FC.White}{Except}{TF.Normal}");
		if (Raise): raise Except;


class Dummy_Awaited_Log:
	"""Used when shits hits the fan."""
	def __init__(self): return;
	def __str__(self): return;
	def Status_Update(self, Status: str): return;
	def OK(self): return;
	def ERROR(self, Error: str): return;
	def EXCEPTION(self, Except: Exception, Raise: bool = False): return;

def Fetch_ALog(Custom_Caller: str | None = None) -> Awaited_Log | Dummy_Awaited_Log:
	""" Fetches the Awaited Log if it exists of the function who ran this.  
	This obviously has its limitations, a singular function cannot have multiple awaited logs at the same time.  
	
	If for some reason the Awaited Log does not exist, a Dummy Awaited Log is returned instead."""
	Caller: str = Get_Caller() if (not Custom_Caller) else Custom_Caller;
	if (Caller in Awaited_Logs.keys()):
		return Awaited_Logs[Caller];
	return Dummy_Awaited_Log();





# Simplified logging functions
def TSN_Debug(Text: str) -> Awaited_Log:
	""" TSN_Debug Log, use to debug libraries. """
	return Log(Text, 10);

def Debug(Text: str) -> Awaited_Log:
	""" Debug Log, use to debug your own code that uses TSNA. """
	return Log(Text, 15);

def Stateless(Text: str) -> Awaited_Log:
	""" Stateless Log, only includes the time. """
	return Log(Text, 20);

def Info(Text: str) -> Awaited_Log:
	""" Info Log """
	return Log(Text, 25);

def Warning(Text: str) -> Awaited_Log:
	""" Warning Log """
	return Log(Text, 30);

def Error(Text: str) -> Awaited_Log:
	""" Error Log """
	return Log(Text, 40);

def Critical(Text: str) -> Awaited_Log:
	""" Critical Log """
	return Log(Text, 50);





# The actual logging function
def Log(Text: str, Level: int = 0, Caller: str = "") -> None:
	""" Logs a specified message manually. Writes the log to a file and displays it to the console.  
	DO NOT USE THIS FUNCTION DIRECTLY, USE THE FUNCTIONS SUCH AS Log.Info()!  

	Arguments:
		Text: String corresponding to the message to Log
		Level: Integer corresponding to how severe the message is.
	"""
	if (not Can_Log(Level)): return;
	global Awaited_Logs, Await_Next; # Awaiting Log System Bullshit

	match Level:
		case 50: Level_Color = FC.Magenta; Level_String = "Critical";
		case 40: Level_Color = FC.Red; Level_String = "Error";
		case 30: Level_Color = FC.Yellow; Level_String = "Warning";
		case 25: Level_Color = FC.Blue; Level_String = "Info";
		case 20: Level_Color = FC.White; Level_String = "Stateless";
		case 15: Level_Color = FC.Cyan; Level_String = "Debug";
		case 10: Level_Color = FC.Grey; Level_String = "TSN_Debug";
		case _: Level_Color = FC.White; Level_String = "Unknown";
	Logger_Console.setLevel(Level); Logger_File.setLevel(Level);

	# Get function name that called the logger
	if (Caller == ""): Caller = Get_Caller(3);
	
	# Detects if the logged text is going to await a status update and changes the terminator accordingly, includes prefix.
	Await_Next = False;
	if (len(Text) >= 3): # Avoids Exception if Text is too short
		if ("..." == Text[-3:]): Await_Next = True;

	# The actual logging part.
	Date_Str, Time_Str = Time.Get_DateStrings(Time.Get_Unix());
	Logged_Text: str = ""; # Prefix if previous log was Awaited
	if (Config.Logger.Display_Date): Logged_Text += f"{FC.Grey}[{Date_Str} - {Time_Str}]{TF.Normal} "; # Date
	if (Level != 20): # Stateless Check
		Logged_Text += f"- {TF.Bold}{Level_Color}{Level_String}{TF.Normal}: "; # Log Level
		if (Config.Logger.Display_Caller): Logged_Text += f"{TF.Underline}{FC.Grey}{Caller}{TF.Normal} → ";
	Logged_Text += Text;

	if (Level >= Config.Logger.Print_Level): # If this is a debug message, don't display to the console.
		Logger_Console.log(Level, Logged_Text);
	if (Config.Logger.File and (Level >= Config.Logger.File_Level)):
		# Check if the Logs folder doesn't exist, create it if it isn't. Assuming it is allowed to do so.
		if (Config.Logger.File): File.Path_Require("logs");
		Logger_File.log(Level, Clear_TextFormatting(Logged_Text));

	if (Await_Next): Awaited_Logs[Caller] = Awaited_Log(Level, Caller, Logged_Text);





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