"""
This module from TSN Abstracter is in charge of configuring its behavior.  

### Available Configuration Classes:
**Logger**: Class used to configure settings related to the TSNA Logger.  
"""
import platform;





class System:
	OS: str = platform.system();
	TUI_Enabled: bool = False;





class Logger:
	"""
	Class used to configure settings related to the TSNA Logger.  

	### General Settings:
	**Disable** : *bool = False*  
	Global toggle to entirely disable the TSNA Loggers.  
	**Display_Date** : *bool = True*  
	Toggle displaying the date at the beginning of Log Entries.  
	**Display_Caller** : *bool = True*  
	Toggle displaying function that called TSNA to Log a brand new Entry.  
	**SNDL_Group** : *str = "Sun"*  
	Which SNDL Color Group to use for the Logs' Colors.  

	### File Logger:
	**File** : *bool = False*  
	Specifies whenever we allow writing the Log to a File.  
	**File_Level** : *int = 20*  
	The minimum Log level that we should log to a file.  
	**File_Folder** : *str = "Logs"*  
	The relative (or absolute) folder name that will be used to save TSNA Logs.  

	### Text Logger
	**Print_Level** : *int = 20*  
	The minimum Log level that we should log to the console.  
	"""
	Disable: bool = False;
	Display_Date: bool = True;
	Display_Caller: bool = True;

	SNDL_Group: str = "Sun"

	File: bool = False;
	File_Level: int = 20;
	File_Folder: str = "Logs";

	Print_Level: int = 20;

