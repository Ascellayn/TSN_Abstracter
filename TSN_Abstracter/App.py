"""
This module from TSN Abstracter is in charge of storing Application Information and Configuration automatically.  
It simply loads `App.tsna` if it finds it.  

Most keys are self-explainable and serve practically only cosmetic purposes.  
However the TSNA Key which is a tuple (saved as an array) containing the minimum TSNA Version required to run the Application.  
`TSN_Abstracter.Require_Version()` will be automatically ran using that very key if you use `TSN_Abstracter.App_Init()` (which you should).
"""
from . import File, Time;
from typing import Any;



Name: str = "Unnamed TSNA-Based Program";
Description: str = "This is a program which uses TSN Abstracter.";

Author: list[str] = ["John Doe"];
Contributors: list[str] = [];

License: str = "Public Domain";
License_Year: str = str(Time.Elapsed_Time(Time.Get_Unix())["Years"] + 1970); # Calculates the current year.


Codename: str = "NoCodename";
Branch: str = "Main";
Version: tuple[int, ...] = (0, 0, 0);
Version_Prefix: str = "";
Version_Suffix: str = "";
TSNA: tuple[int, int, int] = (6,0,0);
Public: dict[str, Any] = {};
Private: dict[str, Any] = {};

if (File.Exists(f"{File.Main_Directory}/App.tsna")):
	AppTSNA = File.JSON_Read(f"{File.Main_Directory}/App.tsna");
	Name = AppTSNA.get("Name", Name);
	Description = AppTSNA.get("Description", Description);

	Author = AppTSNA.get("Author", Author);
	Contributors = AppTSNA.get("Contributors", Contributors);

	License = AppTSNA.get("License", License);
	License_Year = AppTSNA.get("License_Year", License_Year);

	Codename = AppTSNA.get("Codename", Codename);
	Branch = AppTSNA.get("Branch", Branch);
	Version = tuple(AppTSNA.get("Version", Version));
	Version_Prefix = AppTSNA.get("Version_Prefix", Version_Prefix);
	Version_Suffix = AppTSNA.get("Version_Suffix", Version_Suffix);

	Public = AppTSNA.get("Public", Public);
	Private = AppTSNA.get("Private", Private);

	TSNA = tuple(AppTSNA.get("TSNA", TSNA)); # pyright: ignore[reportConstantRedefinition]
	del AppTSNA;





def Dump(Private: bool = False) -> dict[str, str | list[str] | tuple[int, ...] | dict[str, Any]]:
	""" Retrieve the currently active-in-memory TSNA App JSON

	Arguments:
		Private (bool*): Whenever to also include the "Private" key of the TSNA App JSON.

	Returns:
		dict[str, str | list[str] | tuple[int, ...]]: The TSNA App JSON
	
	Examples:
		>>> App.Dump(True);
		{
			"Name": "Serina",
			"Description": "Serina Host-Machine Server for retrieving the current state of all TSNA based applications with the Sena Client enabled.",
			"Author": ["Ascellayn", "The Sirio Network"],
			"Contributors": [],
			"License": "TSN License 2.1 - Base",
			"License_Year": "2026",
			"Codename": "TSN_Serina",
			"Branch": "Azure",
			"Version": [1,0,0],
			"Version_Prefix": "",
			"Version_Suffix": "",
			"TSNA": [6,2,0],
			"Public": [],
			"Private": []
		}
	"""
	Dict: dict[str, str | list[str] | tuple[int, ...] | dict[str, Any]] = {
		"Name": Name,
		"Description": Description,
		"Author": Author,
		"Contributors": Contributors,
		"License": License,
		"License_Year": License_Year,
		"Codename": Codename,
		"Branch": Branch,
		"Version": Version,
		"Version_Prefix": Version_Prefix,
		"Version_Suffix": Version_Suffix,
		"TSNA": TSNA,
		"Public": Public,
		"Private": {}
	};
	if (Private): Dict["Private"] = Private; # pyright: ignore[reportArgumentType] // Unsure why the typing gets angry here
	return Dict;