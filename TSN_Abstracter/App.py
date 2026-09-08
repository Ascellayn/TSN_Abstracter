"""
This module from TSN Abstracter is in charge of storing Application Information and Configuration automatically.  
It simply loads `App.tsna` if it finds it.  

Most keys are self-explainable and serve practically only cosmetic purposes.  
However the TSNA Key which is a tuple (saved as an array) containing the minimum TSNA Version required to run the Application.  
`TSN_Abstracter.Require_Version()` will be automatically ran using that very key if you use `TSN_Abstracter.App_Init()` (which you should).

### `App.tsna` Example:
```
{
	"Name": "Kiyosumi",
	"Description": "Host Server for verifying whenever TSNA-Based Programs are healthy.",
	"Author": ["Ascellayn", "The Sirio Network"],
	"Contributors": [],
	"License": "TSN License 2.3 - Universal",
	"Year": "2025-2026",
	"Codename": "TSN_Kiyosumi",
	"Branch": "Release",
	"Version": [1,0,0],
	"TSNA": [7,0,5],
	"Serina": {
		"Icon": "https://sirio-network.com/Media/Serina/Kiyosumi.png",
		"Data": [
			{
				"Key": "Pixiv API Latency",
				"Description": "The latency between The Sirio Network and Pixiv.",
				"Type": "Integer",
				"Warning": 250,
				"Error": 500,
				"Critical": 1000,
				"isHidden": false,
				"doGraph": true
			}
		]
	}
}
```
"""
from . import File, String, Time;
from typing import Any, TypedDict, Sequence;





Name: str = "Unnamed TSNA-Based Program";
Description: str = "This is a program which uses TSN Abstracter.";
Author: list[str] = ["John Doe"]; Contributors: list[str] = [];

License: str = "Public Domain";
Year: str = str(Time.Elapsed_Time(Time.Get_Unix())["Years"] + 1970); # pyright: ignore[reportTypedDictNotRequiredAccess] | Calculates the current year.


Codename: str = "NoCodename";
Branch: str = "Main";
Version: tuple[int, ...] = (0, 0, 0);
Version_Prefix: str = "";
Version_Suffix: str = "";


TSNA: tuple[int, int, int] = (7,0,0);
Serina: dict[str, Any] = {};
Data: dict[str, Any] = {};








class Type():
	class Dictionary(TypedDict):
		Name: str;
		Description: str;
		Author: list[str];
		Contributors: list[str];
		License: str;
		Year: str;
		Codename: str;
		Branch: str;
		Version: Sequence[int];
		Version_Prefix: str;
		Version_Suffix: str;
		TSNA: Sequence[int];
		Serina: dict[str, Any]; # TEMPORARY! MUST HAVE TYPEDDICT
		Data: dict[str, Any];








def info() -> Type.Dictionary:
	""" Retrieve the currently active-in-memory TSNA App JSON

	Returns:
		dict[str, str | list[str] | tuple[int, ...] | dict[str, Any]]: The TSNA App JSON
	
	Examples:
		>>> App.Dump(True);
		{
			"Name": "Serina",
			"Description": "Serina Host-Machine Server for retrieving the current state of all TSNA based applications with the Sena Client enabled.",
			"Author": ["Ascellayn", "The Sirio Network"],
			"Contributors": [],
			"License": "TSN License 2.1 - Base",
			"Year": "2026",
			"Codename": "TSN_Serina",
			"Branch": "Azure",
			"Version": [1,0,0],
			"Version_Prefix": "",
			"Version_Suffix": "",
			"TSNA": [6,2,0],
			"Data": {}
		}
	"""
	return {
		"Name": Name,
		"Description": Description,
		"Author": Author,
		"Contributors": Contributors,
		"License": License,
		"Year": Year,
		"Codename": Codename,
		"Branch": Branch,
		"Version": Version,
		"Version_Prefix": Version_Prefix,
		"Version_Suffix": Version_Suffix,
		"TSNA": TSNA,
		"Serina": Serina,
		"Data": Data
	};



def version() -> str:
	"""Returns a readable string of the TSNA-Based Application Version."""
	return f"v{Version_Prefix}{".".join(String.ify_Array(Version))}{Version_Suffix}";





def load(JSON: dict[str, Any]) -> None:
	""" Replaces the currently active TSNA App Data with whatever data is present in the argument.

	Arguments:
		JSON (dict[str, Any]*): A TSNA App Dictionary.

	Examples:
		>>> App.Name;
		"Unnamed TSNA-Based Program"

		>>> App.JSON({
			"Name": "Serina",
			"Description": "Serina Host-Machine Server for retrieving the current state of all TSNA based applications with the Sena Client enabled.",
			"Author": ["Ascellayn", "The Sirio Network"],
			"Contributors": [],
			"License": "TSN License 2.1 - Base",
			"Year": "2026",
			"Codename": "TSN_Serina",
			"Branch": "Azure",
			"Version": [1,0,0],
			"Version_Prefix": "",
			"Version_Suffix": "",
			"TSNA": [6,2,0],
			"Serina": {}
		});

		>>> App.Name;
		"Serina"
	"""
	global Name, Description, Author, Contributors, License, Year, Codename, Branch, Version, Version_Prefix, Version_Suffix, TSNA, Serina;


	Name = JSON.get("Name", Name);
	Description = JSON.get("Description", Description);

	Author = JSON.get("Author", Author);
	Contributors = JSON.get("Contributors", Contributors);

	License = JSON.get("License", License);
	Year = JSON.get("Year", Year);


	Codename = JSON.get("Codename", Codename);
	Branch = JSON.get("Branch", Branch);
	Version = tuple(JSON.get("Version", Version));
	Version_Prefix = JSON.get("Version_Prefix", Version_Prefix);
	Version_Suffix = JSON.get("Version_Suffix", Version_Suffix);

	TSNA = tuple(JSON.get("TSNA", TSNA)); # pyright: ignore[reportConstantRedefinition]
	Serina = JSON.get("Serina", Serina);



def reload(Path: str | None = None) -> None:
	if (not Path):
		if (File.Exists(f"{File.Main_Directory}/App.tsna")): reload(f"{File.Main_Directory}/App.tsna");
		if (File.Exists("App.tsna")): reload("App.tsna");
	else:
		app_tsna: dict[str, Any] = File.Read_JSON(Path);
		if ("Private" in app_tsna): del app_tsna["Private"]; # You are not supposed to insert ANYTHING in the Private key from the App.tsna file, only within the code you should access this.
		load(app_tsna);
		del app_tsna;










reload();