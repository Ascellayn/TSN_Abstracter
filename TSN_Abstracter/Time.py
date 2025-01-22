import datetime, time;

def Convert_Datetime(Object: datetime.datetime) -> int:
	""" Takes in a datetime object and returns its Unix Time as an Integer.  
	If the Object passed is empty this returns None."""
	return int(round(Object.timestamp())) if (Object != None) else None;

def Convert_Unix(Unix: int) -> datetime.datetime:
	""" Takes in an Integer representing Unix Time and then returns a datetime object corresponding to it. """
	return datetime.datetime.fromtimestamp(Unix);

def Get_Dawn(Unix: int) -> int:
	""" Takes in an Interger representing Unix Time and then get its value if it was exactly midnight according to the Unix day the Integer represents. """
	return Convert_Datetime(Convert_Unix(Unix).replace(hour=0, minute=0, second=0));

def Elapsed(Unix: int) -> dict:
	""" Takes an Integer representing Unix Time and returns a dictionary containing keys which represent how long since the Epoch has passed.  
	WARNING: Does not take into account Leap Years, nor how long months are actually are (assuming they're exclusively 31 days)."""
	return {
		"Seconds": Unix % 60,
		"Minutes": (Unix // 60) % 60,
		"Hours": (Unix // 3600) % 24,
		"Days": (Unix // 86400) % 31,
		"Months": (Unix // 2678400) % 12,
		"Years": Unix // 32140800
    };

def Get_Unix() -> int:
	""" Get an Integer representing Unix Time. """
	return int(round(time.time()));

def Get_DateStrings(Unix: int) -> str:
	""" Takes an Integer representing Unix Time and returns Two Strings representing the Date and Time according to the favored YYYY/MM/DD HH:MM:SS Format. """
	DT = Convert_Unix(Unix);
	Date = DT.strftime("%Y/%m/%d");
	Time = DT.strftime("%H:%M:%S")
	return Date, Time