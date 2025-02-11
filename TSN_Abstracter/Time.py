import datetime, time;


# Time.Convert_*
def Convert_Datetime(Object: datetime.datetime) -> int:
	""" 
	Converts a Datetime Object to Unix Time.

	Arguments:
		Object: Datetime Object to be converted to an Integer.

	Returns:
		Integer representing the Unix Time the Object argument contains.
	"""
	return int(round(Object.timestamp()));

def Convert_Unix(Unix: int) -> datetime.datetime:
	"""
	Converts Unix Timestamp to Datetime Object.

	Arguments:
		Unix: Integer representing the time since the Epoch.
	
	Returns:
		Datetime Object with the time set according to the Unix argument.
	"""
	return datetime.datetime.fromtimestamp(Unix);


# Time.Get_*
def Get_Dawn(Unix: int) -> int:
	"""
	Get the Unix Time of the specified date day's first second.

	Arguments:
		Unix: Integer representing the time since the Epoch.

	Returns:
		Integer representing the first second of the current day thanks to the Unix Time passed.
	"""
	return Convert_Datetime(Convert_Unix(Unix).replace(hour=0, minute=0, second=0));

def Get_Unix() -> int:
	""" 
	Get an Integer representing Unix Time.

	Returns:
		Integer representing the current Unix Time.
	"""
	return int(round(time.time()));

def Get_DateStrings(Unix: int) -> str:
	"""
	Get the current date and time in the preferred format.

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


# Time.Calculate_*
def Calculate_Elapsed(Unix: int) -> dict:
	"""
	Calculate how much time since the Epoch has passed.  
	NOTE: Everything is calculated according to a year being 365.25 days long.

	Arguments:
		Unix: Integer representing the time since the Epoch.

	Returns:
		Dictionary with every key containing an Integer correspond to how much [KEY NAME] has passed since the Epoch.
	"""
	return {
		"Years": Unix // 31557600,
		"Months": (Unix // 2629800) % 12,
		"Days": int((Unix // 86400) % 30.4375), # The int is required because otherwise this is automatically a float which we do not want.
		"Hours": (Unix // 3600) % 24,
		"Minutes": (Unix // 60) % 60,
		"Seconds": Unix % 60
    };

def Elapsed_String(Unix: int) -> str:
	"""
	Gives a dynamically sized string of the amount of time passed since the epoch.

	Arguments:
		Unix: Integer representing the time since the Epoch.

	Returns:
		String in the format "Xy, Xm, Xd, Xh, Xm, Xs".
	"""
	Elapsed = Calculate_Elapsed(Unix);
	Dynamic_String = "";
	for Key in Elapsed.keys():
		if (Elapsed[Key] != 0):
			Suffix = ", " if (Key != "Seconds") else "";
			Dynamic_String += f"{Elapsed[Key]}{Key[:1].lower()}{Suffix}";
	return Dynamic_String;