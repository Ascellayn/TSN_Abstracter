""" This module from TSN Abstracter is in charge of providing functions related to File Operations.

### Examples
>>> from TSN_Abstracter import File;
>>> File.Exists("README.MD");
True
"""
from . import Log, String;
import pathlib, os, lzma, json, typing;
Working_Directory: str = os.getcwd();





# General File Processing
def Exists(Path: str) -> bool:
	""" Verifies whenever a file or folder exists at the provided path.

	Arguments:
		Path (str*): String representing the Path.

	Returns:
		bool: If the file or a folder exists according to `Path`, returns True, otherwise False.

	Examples:
		>>> File.Exists("README.MD");
		True
	"""
	return pathlib.Path(Path).exists();



def Read(Path: str, Compressed: bool = False) -> str | None:
	""" Read the contents of a file, supports LZMA compressed files.

	Arguments:
		Path (str*): String representing the Path to a file.
		Compressed (bool = False): Specify the use of LZMA Compression.

	Returns:
		str/None: If the file or a folder exists according to "Path", returns its data, otherwise None.

	Examples:
		>>> File.Read("Mika.ctxt", True);
		"Hug a Mika a night, keeps your smile shinning bright~"
	"""
	if Exists(Path):
		Log.TSN_Debug(f"Reading {Path} - Compression: {Compressed}...");
		try:
			if (Compressed):
				with lzma.open(Path, "rt") as File: Data = File.read();
			else:
				with open(Path, "r", encoding="UTF8") as File: Data = File.read();

			Log.Awaited().Status_Update(f"[OK] - {len(Data)} characters\n{String.ASCII.Text.Dim}{Data}"); return Data;

		except Exception as Except:
			if (not Log.Can_Log(10)): Log.Error(f"Reading {Path} - Compression {Compressed}\n{String.ASCII.Shortcut.BSOD}{Except}");
			else: Log.Awaited().EXCEPTION(Except);

	return None;


def Write(Path: str, Data: str, Compressed: bool = False, Append: bool = False) -> bool:
	""" Write the contents of a string to a file, supports LZMA compressed files.
	
	Arguments:
		Path (str*): String representing the Path to a file.
		Data (str*): Whichever data we wish to write to the file.
		Compressed (bool = False): Specify the use of LZMA Compression.

	Returns:
		bool: Represents whenever the write was successful.

	Examples:
		>>> File.Write("README.MD", "haha made you look");
		True
	"""
	Mode: str = "a" if (Append) else "w";

	if Exists(Path_Folder(Path)):
		Log.TSN_Debug(f"Writing {Path} - Compression: {Compressed} - Mode: {Mode} - Data:\n{String.ASCII.Text.Dim}{Data}{String.ASCII.Text.Dim_OFF}\n({len(Data)} characters)...");
		try:
			if (Compressed):
				with lzma.open(Path, Mode) as File: File.write(Data.encode("utf-8"));
			else:
				with open(Path, Mode, encoding="UTF-8") as File: File.write(Data);

			Log.Awaited().OK(); return True;
		except Exception as Except:
			if (not Log.Can_Log(10)): Log.Error(f"{'Writing' if (Mode == "w") else 'Appending'} {Path} - Compression: {Compressed} - Data: {len(Data)} Characters\n{String.ASCII.Shortcut.BSOD}{Except}");
			else: Log.Awaited().EXCEPTION(Except);
	return False;





# Path Manipulation
def Path_Folder(Path: str) -> str:
	""" Takes in a Path and returns itself, minus the file name at the end if it exists by checking for "." and "/" in the filename.  

	Arguments:
		Path (str*): String representing the Path of a file or folder where we wish to remove the file from the string.

	Returns:
		str: The same path string, devoid of the file at the end.

	Examples:
		>>> File.Path_Folder("trade_secrets/hubert.txt");
		"trade_secrets"
	"""
	Absolute: bool = True if (Path[:1] == "/") else False;

	if ("." in Path):
		Folder_Path = Path.split("/"); Folder_Path.pop(-1);

		Path = "";
		for Folder in Folder_Path: Path += f"/{Folder}";
		if (not Absolute): Path = Path[1:];
	return Path;





def Path_Create(Path: str) -> bool:
	""" Creates the full folder structure specified. Equivalent to `mkdir -p`.

	Arguments:
		Path (str*): String representing the Path of folders you wish to create.

	Returns:
		bool: Represents whenever the action was successful.

	Examples:
		>>> File.Path_Create("super secret folder/dont look big silly/ok fine there it is/theres nothing here are you happy");
		True
	"""
	Path = Path_Folder(Path);
	if (Path == ""): return True; # Unfucking "User" error

	try: os.makedirs(Path); return True;
	except Exception as Error:
		Log.Error(f"Create Folder Structure: \"{Path}\"\n{String.ASCII.Shortcut.BSOD}{Error}");
		return False;


def Path_Require(Path: str) -> bool:
	""" Similar to `Path_Create()`, but instead specifies if the folder structure already existed before.

	Arguments:
		Path (str*): String representing the Path of folders you wish to require.

	Returns:
		bool: Represents if the folder structure already existed before.

	Examples:
		>>> File.Path_Require("i didnt exist before/hehehe");
		False
	"""
	Path = Path_Folder(Path);
	if (Exists(Path) or Path == ""):
		return True;
	Path_Create(Path); # This doesn't handle exceptions properly when wrapped in this function... Needs fixing
	return False;





# Other Functions
type Folder_Matrix = tuple[
	str, # Folder Name
	tuple[
		tuple[Folder_Matrix, ...], # Sub-Folders, Recursive
		tuple[str, ...] # Files
	]
];
type Folder_Contents = tuple[
	tuple[str, ...], # Sub-Folders, NOT Recursive
	tuple[str, ...] # Files
];
type Folder_Tree = tuple[tuple[Folder_Matrix, ...], Folder_Contents];



def List(Path: str) -> Folder_Contents:
	""" Returns a matrix of the folders and files inside Path.

	Arguments:
		Path (str*): The folder we wish to view the contents of.

	Returns:
		Folder_Contents: A tuple containing two other tuples, the first containing folders, the second files.

	Examples:
		>>> File.List("TSN_Abstracter");
		(
			('__pycache__',), # WARNING: The extra "," when there's *only one* folder, is a visual bug! I'm not sure how to get rid of it...
			('String.py', 'Cryptography.py', 'Time.py', 'File.py', 'Log.py', 'Misc.py', '__init__.py', 'Config.py', 'Safe.py', 'SNDL.py')
		)
	"""
	if (not Exists(Path)): return ((),());
	Results = next(os.walk(Path));

	return (
		tuple(Results[1]),
		tuple(Results[2])
	);


def Tree(Path: str) -> Folder_Tree:
	""" Returns a matrix of ALL folders and files inside Path.  
	**WARNING**: You will loose your sanity using this function.

	Arguments:
		Path (str*): The folder we wish to view the contents of, including its sub-folders.

	Returns:
		Array containing two arrays, the first one being a list of folders, and the second one being files.  
		Each folder in the first array is in reality

	Examples:
		>>> File.Tree("/media/Nodesaron/FluentSky/Neutral Wallpapers")
		(
			( # tuple[Folder_Matrix, ...]
				(
					'Pack_Noon', # /media/Nodesaron/FluentSky/Neutral Wallpapers/Pack_Noon
					(
						(), # May contain other sub-folders!
						('panorama_0.png', 'panorama_1.png', 'panorama_3.png', 'panorama_2.png', 'panorama_5.png', 'panorama_4.png')
					)
				),
				(
					'Pack_Night',  # /media/Nodesaron/FluentSky/Neutral Wallpapers/Pack_Night
					(
						(),
						('panorama_0.png', 'panorama_1.png', 'panorama_3.png', 'panorama_2.png', 'panorama_5.png', 'panorama_4.png')
					)
				),
			),
			('4 - PackBack_Classic.png',) # /media/Nodesaron/FluentSky/Neutral Wallpapers/
		)
	"""
	if (not Exists(Path)): return ((),()); # type: ignore | shuuush, it'll be fine baby gurl

	Results: Folder_Contents = List(Path);
	return ( # The return looks retarded. But it works so I don't give a shit. Also oh no recursion
		tuple(
			(Folder, Tree(f"{Path}/{Folder}")) for Folder in Results[0] if (Results[0] != ())
		),
		Results[1]
	); # type: ignore | This is what I'd like to call an ugly mf





# JSON Specific Abstraction
def JSON_Read(Path: str, Compressed: bool = False) -> dict[str|int, typing.Any]:
	""" `Read()` Wrapper for reading JSON Files.  
	**QUIRK**: Automatically creates the file path if it doesn't exist, returns an empty dictionary if the file didn't exist prior.
	
	Arguments:
		Path (str*): String representing the Path to a json file.
		Compressed (bool = False): Specify the use of LZMA Compression.

	Returns:
		dict: If the file or a folder exists according to "Path", returns its data, otherwise an empty dictionary is provided.

	Examples:
		>>> File.JSON_Read("BigData.cjson", True);
		{
			"Data": "big cheese redacted this :("
		}
	"""
	if (not Path_Require(Path)):
		Log.TSN_Debug(f"404 Warning - {Path}"); return {};
	JSON: str | None = Read(Path, Compressed);
	return json.loads(JSON if (JSON) else "{}");


def JSON_Write(Path: str, Dictionary: dict[str|int, typing.Any], Compressed: bool = False) -> bool:
	""" `Write()` Wrapper for writing JSON Files.  
	Automatically creates the file structure and file if it doesn't exist.
	
	Arguments:
		Path (str*): String representing the Path to a json file.
		Dictionary (dict*): A serializable dictionary that we want to write to a JSON File.
		Compressed (bool = False): Specify the use of LZMA Compression.

	Returns:
		bool: Represents whenever the write was successful.

	Examples:
		>>> File.JSON_Write("BigData.cjson", {"Cheese Stocks": 9001});
		True
	"""
	try:
		Path_Require(Path)
		return Write(Path, json.dumps(Dictionary, indent=2), Compressed)
	except Exception as Error:
		Log.Error(f"Error Writing JSON {Path}.\n\tDATA: {Dictionary}\n\tEXCEPTION:{Error}");
	return False;


def JSON_Update(Path: str, Dictionary: dict[str|int, typing.Any], Compressed: bool = False) -> bool:
	""" `Write()` Wrapper for updating data to JSON Files.  
	**QUIRK**: Acts as a regular `JSON_Write()` if the file did not exist prior.
	
	Arguments:
		Path (str*): String representing the Path to a json file.
		Dictionary (dict*): A serializable dictionary that we want to append to the JSON File.
		Compressed (bool = False): Specify the use of LZMA Compression.

	Returns:
		bool: Represents whenever the write was successful.

	Examples:
		>>> File.JSON_Write("BigData.json", {"Debt": 999999999});
		True
		# If you want to know how the file looks like after that operation...
		>>> File.JSON_Read("BigData.json");
		{
			"Cheese Stocks": 9001,
			"Debt": 999999999
		}
	"""
	try:
		if (not Exists(Path)): return JSON_Write(Path, Dictionary, Compressed);

		JSON: dict[str|int, typing.Any] = JSON_Read(Path, Compressed);
		JSON.update(Dictionary);
		return JSON_Write(Path, JSON, Compressed);

	except Exception as Except: Log.Error(f"Updating {Path} - Compression: {Compressed}\n{String.ASCII.Shortcut.BSOD}{Except}");
	return False;
