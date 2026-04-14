"""
This module from TSN Abstracter is in charge of configuring its behavior.  

### Available Configuration Classes:
**Logger**: Class used to configure settings related to the TSNA Logger.  
"""
import platform;





# Read Only Attributes, not meant to be modified by the Developer, only by TSNA itself.
class System:
	OS: str = platform.system();
	TUI_Enabled: bool = False;





class Logger:
	"""
	Class used to configure settings related to the TSNA Logger.  

	### General Settings:
	Settings that are primarily visual or super basic.

	**Disable** : *bool = False*  
	Global toggle to entirely disable the TSNA Loggers.  
	**Display_Date** : *bool = True*  
	Toggle displaying the date at the beginning of Log Entries.  
	**Display_Caller** : *bool = True*  
	Toggle displaying function that called TSNA to Log a brand new Entry.  
	**TSNDL_Group** : *str = "Sun"*  
	Which TSNDL Color Group to use for the Logs' Colors.  

	### File Logger:
	Settings that are related specifically to logging to files.

	**File** : *bool = False*  
	Specifies whenever we allow writing the Log to a File.  
	**File_Level** : *int = 20*  
	The minimum Log level that we should log to a file.  
	**File_Folder** : *str = "Logs"*  
	The relative (or absolute) folder name that will be used to save TSNA Logs.  

	
	### Text Logger
	Settings that are related specifically to logging to the console.

	**Print_Level** : *int = 20*  
	The minimum Log level that we should log to the console.  
	"""
	Disable: bool = False;
	Display_Date: bool = True;
	Display_Caller: bool = True;

	TSNDL_Group: str = "Sun"

	File: bool = False;
	File_Level: int = 20;
	File_Folder: str = "Logs";

	Print_Level: int = 20;





class TUI:
	"""
	Class used to configure settings related to the TUI Framework.

	### Visual Settings:
	Generic changes to the visual style of how the TUI Framework behaves.

	**Checkbox_Fill** : *str = X*  
	The character to use to represent an active checkbox.  

	**Scroll_Center** : *float = 2*  
	The amount to divide the amount `Max_Visible` Lines available to get at which position the currently selected element is when in a scrolling situation.  
	"""
	Checkbox_Fill: str = "X";
	Scroll_Center: float = 2;