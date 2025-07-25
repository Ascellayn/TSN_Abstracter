class Logger:
	"""
	Class used to configure settings related to the TSNA Logger.  

	- File
		→ Specifies whenever we allow writing the Log to a File.  
	- File_Level
		→ The minimum Log level that we should log to a file.  
	- Print_Level
		→ The minimum Log level that we should log to the console.  
	"""
	Disable: bool = False;
	Display_Date: bool = True;
	Display_Caller: bool = True;

	File: bool = False;
	File_Level: int = 20;

	Print_Level: int = 20;