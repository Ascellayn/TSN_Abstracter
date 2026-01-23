"""
This module from TSN Abstracter is in charge of storing Application Information and Configuration automatically.  
It simply loads `App.tsna` if it finds it.  

Most keys are self-explainable and serve practically only cosmetic purposes.  
However the TSNA Key which is a tuple (saved as an array) containing the minimum TSNA Version required to run the Application.  
`TSN_Abstracter.Require_Version()` will be automatically ran using that very key if you use `TSN_Abstracter.App_Init()` (which you should).
"""
from . import File, Time;



Name: str = "Unnamed TSNA-Based Program";
Description: str = "This is a program which uses TSN Abstracter.";

Author: list[str] = ["John Doe"];
Contributors: list[str] = [];

License: str = "Public Domain";
License_Year: str = str(Time.Elapsed_Time(Time.Get_Unix())["Years"] + 1970); # Calculates the current year.


Codename: str = "NoCodename";
Branch: str = "Main";
Version: str = "v0";
TSNA: tuple[int, int, int] = (5,0,0);


if (File.Exists("App.tsna")):
	AppTSNA = File.JSON_Read("App.tsna");
	Name = AppTSNA.get("Name", Name);
	Description = AppTSNA.get("Description", Description);

	Author = AppTSNA.get("Author", Author);
	Contributors = AppTSNA.get("Contributors", Contributors);

	License = AppTSNA.get("License", License);
	License_Year = AppTSNA.get("License_Year", License_Year);

	Codename = AppTSNA.get("Codename", Codename);
	Branch = AppTSNA.get("Branch", Branch);
	Version = AppTSNA.get("Version", Version);

	TSNA = tuple(AppTSNA.get("TSNA", TSNA)); # pyright: ignore[reportConstantRedefinition]
	del AppTSNA;