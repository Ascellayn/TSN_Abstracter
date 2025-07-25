import datetime, time;


# Time.Convert_*
def Convert_Datetime(Object: datetime.datetime) -> int | None:
	""" Converts a Datetime Object to Unix Time.

	Arguments:
		Object: Datetime Object to be converted to an Integer.
	Returns:
		Integer representing the Unix Time the Object argument contains.
	"""
	if (Object != None): # For some reason we have to add this check because i dunno cosmic rays
		return int(round(Object.timestamp()));
	return None;

def Convert_Unix(Unix: int) -> datetime.datetime:
	""" Converts Unix Timestamp to Datetime Object.

	Arguments:
		Unix: Integer representing the time since the Epoch.
	Returns:
		Datetime Object with the time set according to the Unix argument.
	"""
	return datetime.datetime.fromtimestamp(Unix);

def Convert_ISO(ISO_8601: str) -> datetime.datetime:
	""" Converts ISO 8601 Timestamp to Datetime Object.

	Arguments:
		ISO_8601: String containing the time in ISO_8601 format such as "2025-06-10T07:31:59Z".
	Returns:
		Datetime Object with the time set according to the ISO_8601 argument.
	"""
	return datetime.datetime.fromisoformat(ISO_8601.replace("Z", "+00:00"));





# Time.Get_*
def Get_Dawn(Unix: int) -> int:
	""" Get the Unix Time of the specified date day's first second.

	Arguments:
		Unix: Integer representing the time since the Epoch.
	Returns:
		Integer representing the first second of the current day thanks to the Unix Time passed.
	"""
	return Convert_Datetime(Convert_Unix(Unix).replace(hour=0, minute=0, second=0));

def Get_Unix() -> int:
	"""  Get an Integer representing Unix Time.

	Returns:
		Integer representing the current Unix Time.
	"""
	return int(round(time.time()));

def Get_DateStrings(Unix: int) -> str:
	""" Get the specified Unix's date and time string in the preferred format.

	Arguments:
		Unix: Integer representing the time since the Epoch.
	Returns:
		Date: String corresponding to the date in YYYY/MM/DD format.  
		Time: String corresponding to the time in HH:MM:SS format.
	"""
	DT = Convert_Unix(Unix);
	Date = DT.strftime("%Y/%m/%d");
	Time = DT.strftime("%H:%M:%S")
	return Date, Time





# Time Functions that aid in String related functions.
def Short_Time_Units() -> dict:
	return {
		"Years": "Y",
		"Months": "M",
		"Days": "D",
		"Hours": "h",
		"Minutes": "m",
		"Seconds": "s",
		"Milliseconds": "ms"
	};

def Trailing_Zero(Number: int) -> str:
	""" Adds a trailing Zero"""
	if (Number > 9): return Number;
	return f"0{Number}";


def Unit_Power(Unit: str) -> int:
	match Unit:
		case "Years": return 5;
		case "Months": return 4;
		case "Days": return 3;
		case "Hours": return 2;
		case "Minutes": return 1;
		case "Seconds": return 0;
		case "Milliseconds": return -1;





# Time Functions with Calculations
def Calculate_Elapsed(Unix: int) -> dict:
	""" Calculate how much time since the Epoch has passed.  
	NOTE: Everything is calculated according to a year being 365.25 days long.

	Arguments:
		Unix: Integer representing the time since the Epoch.
	Returns:
		Dictionary with every key containing an Integer correspond to how much [KEY NAME] has passed since the Epoch.
	"""
	return { # The ints are required because otherwise we have a trailling ".X"
		"Years": int(Unix // 31557600),
		"Months": int((Unix // 2629800) % 12),
		"Days": int((Unix // 86400) % 30.4375), 
		"Hours": int((Unix // 3600) % 24),
		"Minutes": int((Unix // 60) % 60),
		"Seconds": round(Unix % 60),
		"Milliseconds": round((Unix % 60 - round(Unix % 60))*1000)
	};


def Elapsed_String(Unix: int, Delimiter: str = ", ", Show_Smaller: bool = False, Show_Until: int = 0, Trailing_Until: int = 3, Display_Units: bool = True) -> str:
	""" Gives a dynamically sized string of the amount of time passed since the epoch.

	Arguments:
		Unix: Integer representing the time since the Epoch.
		Delimiter: String representing what should follow the time string after the units.
		Show_Smaller: Should we still display units that are smaller than the biggest unit available?
		Show_Until: Integer representing until what "Unit Power" we should display.
		Trailing_Until: Integer representing at what "Unit Power" we should stop adding trailing Zeros.
		Display_Units: Allow the display of Short_Time_Units();
	Returns:
		String in the format "X{Unit}{Delimiter}".
	"""
	Elapsed = Calculate_Elapsed(Unix);
	Dynamic_String = ""; Biggest_Unit: int = -1; Smallest_Unit = -1;

	for Key in Elapsed.keys():
		if (Elapsed[Key] != 0):
			if (Unit_Power(Key) > Biggest_Unit): Biggest_Unit = Unit_Power(Key);
			Smallest_Unit = Unit_Power(Key);
	if (Show_Smaller): Smallest_Unit = Show_Until;

	for Key in Elapsed.keys():
		Power = Unit_Power(Key);
		if ((Elapsed[Key] != 0 or (Show_Smaller and Biggest_Unit >= Power)) and Power >= Show_Until):
			Suffix = Delimiter if ((Power) != Smallest_Unit) else "";
			Dynamic_String += f"{Trailing_Zero(Elapsed[Key]) if (Power < Trailing_Until) else Elapsed[Key]}{Short_Time_Units()[Key] if (Display_Units) else ""}{Suffix}";
	return Dynamic_String;