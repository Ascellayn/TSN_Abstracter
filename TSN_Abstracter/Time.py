""" This module from TSN Abstracter is in charge of providing functions related to Time.

### Examples
>>> from TSN_Abstracter import Time;
>>> Time.Get_Unix();
441759600
"""
from TSN_Abstracter import String;
import datetime, time, math;





def Convert_Datetime(Object: datetime.datetime, Precise: bool = False) -> int | float:
	""" Converts a Datetime Object to a Unix Timestamp.

	Arguments:
		Object (datetime.datetime*): Datetime Object to be converted to an Integer or Float.
		Precise (bool = False): Boolean defining if we want a Precise Unix Time. Defaults to False.

	Returns:
		int/float/None: The Unix Timestamp provided by the datetime object, or nothing if the object is invalid.
	
	Examples:
		>>> Time.Convert_Datetime(Timestamp);
		441759600
	"""
	if (Object == None): return None; # For some reason we have to add this check because i dunno cosmic rays
	return Object.timestamp() if (Precise) else int(round(Object.timestamp()));


def Convert_Unix(Unix: int | float) -> datetime.datetime:
	""" Converts an Unix Timestamp to a datetime object.

	Arguments:
		Unix (int|float*): The Unix Timestamp.

	Returns:
		datetime: The datetime object that we converted the Unix Timestamp from.

	>>> Examples:
		>>> Time.Convert_Unix(441759600);
		datetime.datetime(1984, 1, 1, 0, 0)
	"""
	return datetime.datetime.fromtimestamp(Unix);



def Convert_ISO8601(ISO_8601: str) -> datetime.datetime:
	""" Converts ISO 8601 Timestamps to datetime objects.

	Arguments:
		ISO_8601 (str*): A timestamp in the ISO_8601 format.

	Returns:
		datetime: The datetime object that we converted the ISO 8601 from.
	
	Examples:
		>>> Time.Convert_ISO("2023-07-14T17:00:00Z");
		datetime.datetime(2023, 7, 14, 17, 0, tzinfo=datetime.timezone.utc)
	"""
	return datetime.datetime.fromisoformat(ISO_8601.replace("Z", "+00:00"));





# Time.Get_*
def Get_Unix(Precise: bool = False) -> int | float:
	""" Get an Integer/Float representing Unix Time.

	Arguments:
		Precise (bool = False): Specify if we want a precise Unix Time.

	Returns:
		int/float: The current Unix Time.

	Examples:
		>>> Time.Get_Unix();
		441759600
	"""
	return time.time() if (Precise) else int(round(time.time()));



def Get_Dawn(Unix: int | float) -> int | float:
	""" Get the first second of the day specified in the Unix Timestamp.

	Arguments:
		Unix (int|float*): The Unix Timestamp.

	Returns:
		int/float: The Unix Timestamp of the first second of the specified day.

	Examples:
		>>> Time.Get_Dawn(441759743);
		441759600
	"""
	return Convert_Datetime(
		Convert_Unix(Unix).replace(hour=0, minute=0, second=0),
		True if (type(Unix) == float) else False
	);


def Get_DateStrings(Timestamp: int | float | datetime.datetime) -> tuple[str, str]:
	""" Get the specified Timestamp's date and time string in the preferred format.

	Arguments:
		Timestamp (int/float/datetime*): The timestamp we wish to get readable strings from.

	Returns:
		tuple (str, str): Two strings containing the date in YYYY/MM/DD and HH:MM:SS format respectively.

	Examples:
		>>> Time.Get_DateStrings(441759600);
		('1984/01/01', '00:00:00')
	"""
	Date: datetime.datetime;
	if (type(Timestamp) == datetime.datetime): Date = Timestamp;
	else: Date = Convert_Unix(Timestamp); # type: ignore | the type hint is retarded

	return Date.strftime("%Y/%m/%d"), Date.strftime("%H:%M:%S");





# Time Functions that aid in String related functions.
Unit_Short: dict[str, str] = {
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


Unit_Power: dict[str, int] = {
	"Years": 5,
	"Months": 4,
	"Days": 3,
	"Hours": 2,
	"Minutes": 1,
	"Seconds": 0,
	"Milliseconds": -1,
	"Microseconds": -2,
	"Nanoseconds": -3
};






def Unit_Edges(Time_Dict: dict[str, int]) -> tuple[int, int]:
	""" Get the maximum and minimum power units of a given Time Dict.

	Arguments:
		Time_Dict (dict[str, int]):
	
	Returns:
		tuple (int, int): The biggest then smallest units' powers present in the Time Dict.

	Raises:
		ValueError: A key in the Time_Dict is invalid or unknown to TSNA.

	Examples:

	"""
	Biggest_Unit: int = -3; Smallest_Unit: int = -3;

	for Key in Time_Dict.keys():
		if (Key not in Unit_Power.keys()): raise ValueError(f"Invalid Key in Time Dict: \"{Key}\".");

		if (Time_Dict[Key] != 0):
			if (Unit_Power[Key] > Biggest_Unit): Biggest_Unit = Unit_Power[Key];
			Smallest_Unit = Unit_Power[Key];

	return Biggest_Unit, Smallest_Unit;





# Time Functions with Calculations
def Elapsed_Time(Unix: int | float) -> dict[str, int]:
	""" Calculate how much time since the Epoch has passed.  
	**NOTE**: Everything is calculated according to a year being **365.25 days** long. This function will breakdown the moment you reach into the days.

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
		"Seconds": int(math.floor(Unix % 60)),

		# It gets ugly here
		"Milliseconds": int((Unix - math.floor(Unix))*1000),
		"Microseconds": int(
			math.floor(
				(
					(
						(Unix - math.floor(Unix))*1000 - math.floor((Unix - math.floor(Unix))*1000)
					)
				)*1000
			)
		),
		"Nanoseconds": int(
			(
				(
					(
						(
							(Unix - math.floor(Unix))*1000 - math.floor((Unix - math.floor(Unix))*1000)
						)
					)*1000
				)
				-
				math.floor(
					(
						(
							(Unix - math.floor(Unix))*1000 - math.floor((Unix - math.floor(Unix))*1000)
						)
					)*1000
				)
			)*100

		)
	};


def Elapsed_String(
		Time: int | float,
		Delimiter: str = ", ",
		Show_Bigger: bool = False, Show_Bigger_Starting: int = 2,
		Show_Starting: int = 6, Show_Smaller: bool = True,
		Show_Until: int = 0,
		Trailing_Starting: int = 2,
		Display_Units: bool = True
	) -> str:
	""" Gives a dynamically sized string of the amount of time passed.

	Arguments:
		Time (int/float*): How much time has passed passed.
		Delimiter (str = ", "): What should separate each unit.
		Show_Bigger (bool = False): Should we still display units that are bigger than the smallest unit available?
		Show_Bigger_Starting (int = 6): At what "Unit Power" we should start displaying the time passed, even if the specified `Time` is too small to naturally display the unit.
		Show_Starting (int = 2): At what "Unit Power" we should start displaying the time passed.
		Show_Smaller (bool = True): Should we still display units that are smaller than the smallest unit available?
		Show_Until (int = 0): Until what "Unit Power" we should display the time passed.
		Trailing_Starting (int = 2): At what "Unit Power" we should start adding trailing Zeros.
		Display_Units (bool = True): Allow the display of "short" units;

	Returns:
		str: The amount of time that has passed in the format "X{Unit}{Delimiter}".

	Examples:
		>>> Time.Elapsed_String(69420, ":", Display_Units=False)
		"19:17:00"
	"""
	Time_Dict = Elapsed_Time(Time);
	Dynamic_String = "";

	Smallest_Unit: int = Unit_Edges(Time_Dict)[1];
	if (Show_Smaller): Smallest_Unit = Show_Until;

	for Key in Time_Dict.keys():
		Power = Unit_Power[Key]; Display: bool = False;

		if (Time_Dict[Key] != 0): Display = True;
		if (Show_Bigger and Show_Bigger_Starting >= Power): Display = True;
		if (Show_Smaller and Smallest_Unit >= Power): Display = True
		if (Show_Starting < Power): Display = False;
		if (Show_Until > Power): Display = False;
		#print(f"{Key}: {Display} | Trailing: {String.Trailing_Zero(Time_Dict[Key])}");
		if (Display):
			Suffix = Delimiter if ((Power) != Smallest_Unit) else "";

			# Tried my best to make this slightly readable, pretty sure I failed.
			Dynamic_String += \
f"{
	(
		String.Trailing_Zero(Time_Dict[Key])
		if (Key not in ["Milliseconds", "Microseconds", "Nanoseconds"])
		else String.Trailing_Zero(Time_Dict[Key], 4)
	)
	if (Trailing_Starting >= Power)
	else Time_Dict[Key]
}\
{
	Unit_Short[Key]
	if (Display_Units)
	else ""
}\
{Suffix}";

	return Dynamic_String;





def String_Time(Text: str) -> float:
	""" Get how much time has passed according to the passed string.

	Arguments:
		Text (str*): A string in the format "X{Unit_Short} [...]".

	Returns:
		float: The amount of time that has passed.

	Raises:
		ValueError: If the unit is invalid, this exception will get raised.

	Examples:
		>>> Time.String_Time("1D 1h");
		90000
	"""
	Digits: list[int] = ["9", "8", "7", "6", "5", "4", "3", "2", "1", "0", ".", ","];
	Timestamp: float = 0;

	Numbers: list[str] = Text.split(" ");

	for Number in Numbers:
		for Index, Character in enumerate(Number):
			if (Character not in Digits):
				T_Unit: str = Number[Index:];
				T_Number: float = float(Number[:Index]);
				match T_Unit:
					case "Y": Timestamp += T_Number*31557600;
					case "M": Timestamp += T_Number*2629800;
					case "D": Timestamp += T_Number*86400;
					case "h": Timestamp += T_Number*3600;
					case "m": Timestamp += T_Number*60;
					case "s": Timestamp += T_Number;
					case "ms": Timestamp += T_Number/1000;
					case "µs": Timestamp += T_Number/10**6;
					case "ns": Timestamp += T_Number/10**9;
					case _: raise ValueError(f"Invalid Unit \"{T_Unit}\".");
	return Timestamp;