""" ***Implemented in __TSNA `v7.0.0`__***  

This module from TSN Abstracter is in charge of providing functions related to Time.

### Examples
>>> from TSN_Abstracter import Time;
>>> Time.Get_Unix();
441759600
"""
from . import String;


from typing import TypedDict, NotRequired;
from datetime import datetime;
import time, math;





type unix_t = int | float;








class Dict(TypedDict):
	""" ***Implemented in __TSNA `v7.0.0`__***  
	
	Time Dictionary containing the amount of [X] of a particular Unit.
	"""
	Years: NotRequired[int];
	Months: NotRequired[int];
	Days: NotRequired[int];
	Hours: NotRequired[int];
	Minutes: NotRequired[int];
	Seconds: NotRequired[int];
	Milliseconds: NotRequired[int];
	Microseconds: NotRequired[int];
	Nanoseconds: NotRequired[int];



class Unit:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Constants Helpers for Time functions and "Unit Power" related methods.
	"""
	SHORT: dict[str, str] = {
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


	POWER: dict[str, int] = {
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





	@staticmethod
	def edges(TIME_DICT: Dict) -> tuple[int, int]:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Get the maximum and minimum power units of a given Time Dict.

		Arguments:
			TIME_DICT (Time.Dict)*: The dictionary containing time, where we'll look for the biggest unit in it.
		
		Returns:
			tuple (int, int): The biggest then smallest units' powers present in the Time Dict.

		Raises:
			ValueError: A key in the Time_Dict is invalid or unknown to TSNA.
		"""
		unit_biggest: int = -3; unit_smallest: int = -3;
		# [-3] is an alias to min(Unit.POWER.values())
		# It is hardcoded here for performance reasons.

		for K in TIME_DICT.keys():
			if (K not in Unit.POWER.keys()): raise ValueError(f"Invalid Key in Time Dict: \"{K}\".");

			if (TIME_DICT[K] != 0):
				if (Unit.POWER[K] > unit_biggest): unit_smallest = Unit.POWER[K];
				unit_smallest = Unit.POWER[K];

		return unit_biggest, unit_smallest;





class Unix:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Functions to manipulate integers representing Unix Timestamps
	"""
	YEAR: int = 31556925; # Topical Year, this equals roughly to 365 days, 5 hours, 48 minutes and 45 seconds.
	MONTH: float = 2629743.75; # Topical Year / 12, this equals roughly to 30 days, 10 hours, 29 minutes, 3 seconds and 750 milliseconds and 192 microseconds.
	DAY: int = 86400;
	HOUR: int = 3600;
	MINUTE: int = 60;





	@staticmethod
	def now(Precise: bool = False) -> unix_t:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Get an Integer/Float representing Unix Time.

		Arguments:
			Precise (bool = False): Specify if we want a precise Unix Time.

		Returns:
			unix_t: The current Unix Time.

		Examples:
			>>> Time.Unix.now();
			441759600
		"""
		return time.time() if (Precise) else int(round(time.time()));



	@staticmethod
	def dawn(UNIX: unix_t) -> unix_t:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Get the first second of the day specified in the Unix Timestamp.

		Arguments:
			Unix (unix_t)*: The Unix Timestamp.

		Returns:
			int/float: The Unix Timestamp of the first second of the specified day.

		Examples:
			>>> Time.Get_Dawn(441759743);
			441759600
		"""
		return Datetime.toUnix(
			Unix.toDatetime(UNIX).replace(hour=0, minute=0, second=0),
			True if (type(UNIX) == float) else False
		);





	@staticmethod
	def toDatetime(UNIX: unix_t) -> datetime:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Converts an Unix Timestamp to a datetime object.

		Arguments:
			Unix (unix_t)*: The Unix Timestamp.

		Returns:
			datetime: The datetime object that we converted the Unix Timestamp from.

		>>> Examples:
			>>> Time.Convert_Unix(441759600);
			datetime(1984, 1, 1, 0, 0)
		"""
		return datetime.fromtimestamp(UNIX);





	@staticmethod
	def fromString(TEXT: str) -> unix_t:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Get how much time has passed according to the passed string.

		Arguments:
			Text (str)*: A string in the format "X{Unit.SHORT} [...]".

		Returns:
			float: The amount of time that has passed.

		Raises:
			ValueError: If the unit is invalid, this exception will get raised.

		Examples:
			>>> Time.String_Time("1D 1h");
			90000
		"""
		DIGITS: list[str] = ["9", "8", "7", "6", "5", "4", "3", "2", "1", "0", ".", ","];
		timestamp: float = 0;

		numbers: list[str] = TEXT.split(" ");

		for n in numbers:
			for i, char in enumerate(n):
				if (char not in DIGITS):
					unit: str = n[i:];
					number: float = float(n[:i]);
					match unit:
						case "Y": timestamp += number * Unix.YEAR;
						case "M": timestamp += number * Unix.MONTH;
						case "D": timestamp += number * Unix.DAY;
						case "h": timestamp += number * Unix.HOUR;
						case "m": timestamp += number * Unix.MINUTE;
						case "s": timestamp += number;
						case "ms": timestamp += number / 1000;
						case "µs": timestamp += number / 10**6;
						case "ns": timestamp += number / 10**9;
						case _: raise ValueError(f"Invalid Unit \"{unit}\".");
		return timestamp;



class Datetime:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Functions to manipulate datetime objects
	"""
	@staticmethod
	def now() -> datetime:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Get a datetime object of the current date.

		Returns:
			datetime: The current Date/Time in a datetime object.

		Examples:
			>>> Time.Datetime.now();
			<datetime object>
		"""
		return datetime.now();





	@staticmethod
	def toUnix(DATETIME: datetime, PRECISE: bool = False) -> unix_t:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Converts a Datetime Object to a Unix Timestamp.

		Arguments:
			DATETIME (datetime)*: Datetime Object to be converted to an Integer or Float.
			PRECISE (bool = False): Boolean defining if we want a Precise Unix Time. Defaults to False.

		Returns:
			unix_t/None: The Unix Timestamp provided by the datetime object, or nothing if the object is invalid.
		
		Examples:
			>>> Time.Convert_Datetime(Timestamp);
			441759600
		"""
		if (DATETIME == None): return None; # For some reason we have to add this check because i dunno cosmic rays
		return DATETIME.timestamp() if (PRECISE) else int(round(DATETIME.timestamp()));





	@staticmethod
	def fromISO8601(ISO_8601: str) -> datetime:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Converts ISO 8601 Timestamps to datetime objects.

		Arguments:
			ISO_8601 (str)*: A timestamp in the ISO_8601 format.

		Returns:
			datetime: The datetime object that we converted the ISO 8601 from.
		
		Examples:
			>>> Time.Convert_ISO("2023-07-14T17:00:00Z");
			datetime(2023, 7, 14, 17, 0, tzinfo=datetime.timezone.utc)
		"""
		return datetime.fromisoformat(ISO_8601.replace("Z", "+00:00"));








class Elapsed:
	@staticmethod
	def dict(TIMESTAMP: unix_t) -> Dict:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Calculate how much time since the Epoch has passed.  
		**NOTE**: Everything is calculated according to a year being **365.25 days** long. This function will breakdown the moment you reach into the days.

		Arguments:
			TIMESTAMP (unix_t*): Integer/Float representing the time since the Epoch.
		Returns:
			Dictionary with every key containing an Integer correspond to how much [KEY NAME] has passed since the Epoch.
		"""
		time_dict: Dict = { # The ints are required because otherwise we have a trailing ".X"
			"Years": int(TIMESTAMP // Unix.YEAR),
			"Months": int((TIMESTAMP // Unix.MONTH) % 12),
			"Days": int((TIMESTAMP // Unix.DAY) % Unix.MONTH / (Unix.HOUR*24)), # This is stupid, but this is what you have to do to avoid dealing with leap years entirely

			"Hours": int((TIMESTAMP // Unix.HOUR) % 24),
			"Minutes": int((TIMESTAMP // Unix.MINUTE) % 60),
			"Seconds": int(math.floor(TIMESTAMP % 60)),
		};

		x: unix_t = TIMESTAMP;
		x -= math.floor(x);
		x = x*1000;
		time_dict["Milliseconds"] = int(x);

		x -= math.floor(x);
		x = x*1000;
		time_dict["Microseconds"] = int(x);

		x -= math.floor(x);
		x = x*1000;
		time_dict["Nanoseconds"] = int(x);

		return time_dict;



	@staticmethod
	def string(
			TIME: unix_t,
			DELIMITER: str = ", ",
			UNITS: bool = True, UNITS_LONG: bool = False,
				*,
			BIGGER: bool = False, BIGGER_START: int = 2,
			START: int = 6, SMALLER: bool = True,
			UNTIL: int = 0,
			TRAIL_AT: int = 2,
		) -> str:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Gives a dynamically sized string of the amount of time passed.

		Arguments:
			Time (unix_t)*: How much time has passed passed.
			Delimiter (str = ", "): What should separate each unit.
			BIGGER (bool = False): Should we still display units that are bigger than the smallest unit available?
			BIGGER_START (int = 6): At what "Unit Power" we should start displaying the time passed, even if the specified `Time` is too small to naturally display the unit.
			START (int = 2): At what "Unit Power" we should start displaying the time passed.
			SMALLER (bool = True): Should we still display units that are smaller than the smallest unit available?
			UNTIL (int = 0): Until what "Unit Power" we should display the time passed.
			TRAIL_AT (int = 2): At what "Unit Power" we should start adding trailing Zeros.
			UNITS (bool = True): Allow the display of units.
			UNITS_LONG (bool = False): Display full length units instead of just their short name.

		Returns:
			str: The amount of time that has passed in the format "X{Unit}{Delimiter}".

		Examples:
			>>> Time.Elapsed_String(69420, ":", UNITS=False)
			"19:17:00"
		"""
		time_dict: Dict = Elapsed.dict(TIME);
		string: str = "";

		unit_bigger, unit_smaller = Unit.edges(time_dict);
		if (SMALLER): unit_smaller = UNTIL;

		for K in time_dict.keys():
			power = Unit.POWER[K]; display: bool = False;

			if (time_dict[K] != 0): display = True;
			if (BIGGER and (BIGGER_START >= power)): display = True;
			if (SMALLER and (unit_bigger >= power)): display = True;
			if (START < power): display = False;
			if (UNTIL > power): display = False;
			#print(f"{Key}: {display} | Trailing: {String.trailingZero(time_dict[Key])}");
			if (display):
				suffix: str = DELIMITER if ((power) != unit_smaller) else "";

				# Tried my best to make this slightly readable, pretty sure I failed.
				string += \
	f"{
		(
			String.trailingZero(time_dict[K]) # pyright: ignore[reportUnknownArgumentType]
			if (K not in ["Milliseconds", "Microseconds", "Nanoseconds"])
			else String.trailingZero(time_dict[K], 4) # pyright: ignore[reportUnknownArgumentType]
		)
		if (TRAIL_AT >= power)
		else time_dict[K]
	}\
	{
		(
			' ' + (
				K.lower()
				if (time_dict[K] > 1)
				else K.lower()[:-1]
			)
			if (UNITS_LONG)
			else Unit.SHORT[K]
		)
		if (UNITS)
		else ""
	}\
	{suffix}";

		return string;








def dateStrings(Date: unix_t | datetime, REVERSED: bool = True) -> tuple[str, str]:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Get the specified Timestamp's date and time string in the preferred format.

	Arguments:
		Date (unix_t | datetime)*: The timestamp we wish to get readable strings from.
		REVERSED (bool = True): Whenever to use `YYYY/MM/DD` for the date format or `DD/MM/YYYY`.
		*And no, `MM/DD/YYYY` is not a real date format.*

	Returns:
		tuple (str, str): Two strings containing the date in YYYY/MM/DD and HH:MM:SS format respectively.

	Examples:
		>>> Time.Get_DateStrings(441759600);
		('1984/01/01', '00:00:00')
	"""
	if (isinstance(Date, int | float)): Date = Unix.toDatetime(Date);
	# unix_t doesn't work as unix_t is a TypeAlias

	return Date.strftime("%Y/%m/%d") if (REVERSED) else Date.strftime("%d/%m/%Y"), Date.strftime("%H:%M:%S");