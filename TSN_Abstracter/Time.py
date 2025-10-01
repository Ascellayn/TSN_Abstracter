import datetime, time;


# Time.Convert_*
def Convert_Datetime(Object: datetime.datetime, Precise: bool = False) -> int | float | None:
	""" Converts a Datetime Object to Unix Time.

	Arguments:
		Object: Datetime Object to be converted to an Integer.
		Precise: Boolean defining if we want a Precise Unix Time.
	Returns:
		Integer representing the Unix Time the Object argument contains.
	"""
	if (Object != None): # For some reason we have to add this check because i dunno cosmic rays
		if (Precise): return Object.timestamp();
		return int(round(Object.timestamp()));
	return None;

def Convert_Unix(Unix: int | float) -> datetime.datetime:
	""" Converts Unix Timestamp to Datetime Object.

	Arguments:
		Unix: Integer/Float representing the time since the Epoch.
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
def Get_Dawn(Unix: int | float) -> int | float:
	""" Get the Unix Time of the specified date day's first second.

	Arguments:
		Unix: Integer/Float representing the time since the Epoch.
	Returns:
		Integer/Float representing the first second of the current day thanks to the Unix Time passed.
	"""
	if (type(Unix) == int): return Convert_Datetime(Convert_Unix(Unix).replace(hour=0, minute=0, second=0));
	return Convert_Datetime(Convert_Unix(Unix).replace(hour=0, minute=0, second=0), True);

def Get_Unix(Precise: bool = False) -> int | float:
	""" Get an Integer/Float representing Unix Time.

	Arguments:
		Precise: Boolean defining if we want a Precise Unix Time.
	Returns:
		Integer/Float representing the current Unix Time.
	"""
	if (Precise): return time.time();
	return int(round(time.time()));

def Get_DateStrings(Unix: int | float) -> str:
	""" Get the specified Unix's date and time string in the preferred format.

	Arguments:
		Unix: Integer/Float representing the time since the Epoch.
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
		"Milliseconds": "ms",
		"Microseconds": "µs",
		"Nanoseconds": "ns"
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
		case "Microseconds": return -2;
		case "Nanoseconds": return -3;

def Unit_BnS(Time_Dict: dict) -> str:
	Biggest_Unit: int = -1; Smallest_Unit: int = -1;
	for Key in Time_Dict.keys():
		if (Time_Dict[Key] != 0):
			if (Unit_Power(Key) > Biggest_Unit): Biggest_Unit = Unit_Power(Key);
			Smallest_Unit = Unit_Power(Key);
	return Biggest_Unit, Smallest_Unit;





# Time Functions with Calculations
def Calculate_Elapsed(Unix: int | float) -> dict:
	""" Calculate how much time since the Epoch has passed.  
	NOTE: Everything is calculated according to a year being 365.25 days long.

	Arguments:
		Unix: Integer/Float representing the time since the Epoch.
	Returns:
		Dictionary with every key containing an Integer correspond to how much [KEY NAME] has passed since the Epoch.
	"""
	return { # The ints are required because otherwise we have a trailing ".X"
		"Years": int(Unix // 31557600),
		"Months": int((Unix // 2629800) % 12),
		"Days": int((Unix // 86400) % 30.4375),

		"Hours": int((Unix // 3600) % 24),
		"Minutes": int((Unix // 60) % 60),
		"Seconds": int(round(Unix % 60)),

		# It gets ugly here
		"Milliseconds": int((Unix - round(Unix))*1000),
		"Microseconds": int(
			round(
				(
					(
						(Unix - round(Unix))*1000 - round((Unix - round(Unix))*1000)
					)
				)*1000
			)
		),
		"Nanoseconds": int(
			(
				(
					(
						(
							(Unix - round(Unix))*1000 - round((Unix - round(Unix))*1000)
						)
					)*1000
				)
				-
				round(
					(
						(
							(Unix - round(Unix))*1000 - round((Unix - round(Unix))*1000)
						)
					)*1000
				)
			)*100

		)
	};


def Elapsed_String(Unix: int | float, Delimiter: str = ", ", Show_Bigger: bool = False, Show_Bigger_Starting: int = 2, Show_Starting: int = 6, Show_Smaller: bool = False, Show_Until: int = 0, Trailing_Until: int = 3, Display_Units: bool = True) -> str:
	""" Gives a dynamically sized string of the amount of time passed since the epoch.

	Arguments:
		Unix: Integer/Float representing the time since the Epoch.
		Delimiter: String representing what should follow the time string after the units.
		Show_Bigger: Should we still display units that are bigger than the smallest unit available?
		Show_Bigger_Starting: Integer representing starting what "Unit Power" we should start forcefully displaying numbers.
		Show_Starting: Integer representing starting what "Unit Power" we should display.
		Show_Smaller: Should we still display units that are smaller than the biggest unit available?
		Show_Until: Integer representing until what "Unit Power" we should display.
		Trailing_Until: Integer representing at what "Unit Power" we should stop adding trailing Zeros.
		Display_Units: Allow the display of Short_Time_Units();
	Returns:
		String in the format "X{Unit}{Delimiter}".
	"""
	Time_Dict = Calculate_Elapsed(Unix);
	Dynamic_String = "";

	Biggest_Unit, Smallest_Unit = Unit_BnS(Time_Dict);
	Smallest_Unit = Show_Until;

	for Key in Time_Dict.keys():
		Power = Unit_Power(Key);
		Display = False;
		if (Time_Dict[Key] != 0): Display = True;
		if (Show_Bigger and Show_Bigger_Starting >= Power): Display = True;
		if (Show_Smaller and Biggest_Unit >= Power): Display = True;
		if (Power >= Show_Starting): Display = False;
		if (Show_Until > Power): Display = False;
		#print(f"{Key}: {Display}")
		if (Display):
			Suffix = Delimiter if ((Power) != Smallest_Unit) else "";

			# Tried my best to make this slightly readable, pretty sure I failed.
			Dynamic_String += \
f"{
	(
		Trailing_Zero(Time_Dict[Key])
		if (Key not in ["Milliseconds", "Microseconds", "Nanoseconds"])
		else Trailing_Zero(Time_Dict[Key], 4)
	)
	if (Power < Trailing_Until)
	else Time_Dict[Key]
}\
{
	Short_Time_Units()[Key]
	if (Display_Units)
	else ""
}\
{Suffix}";

	return Dynamic_String;