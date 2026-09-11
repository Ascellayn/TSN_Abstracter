""" ***Implemented in __TSNA `v7.0.0`__***  

This module from TSN Abstracter is in charge of providing functions related to File Operations.

### Examples
>>> from TSN_Abstracter import File;
>>> File.exists("README.MD");
True
"""
from . import Log, String;
import pathlib, os, lzma, json, typing;
from typing import Any, TypeAlias;





# Get folder where the TSNA Application is located by searching for App.tsna, if it can't be found then use `__file__`.
tmp: list[str] = os.path.dirname(__file__).split("/");
while (len(tmp) != 0):
	if (pathlib.Path(f"/{'/'.join(tmp)}/App.tsna").exists()): break;
	tmp.pop();
DIRECTORY: str = os.path.dirname(__file__) if (len(tmp) == 0) else f"/{'/'.join(tmp)}";
del tmp;








Folder_Name: TypeAlias = str;
File_Name: TypeAlias = str;
type Folder_Matrix = tuple[
	Folder_Name, # Folder Name
	tuple[Folder_Matrix, ...], # Sub-Folders, Recursive
	tuple[File_Name, ...] # Files
];
type Folder_Contents = tuple[
	tuple[Folder_Name, ...], # Sub-Folders, NOT Recursive
	tuple[File_Name, ...] # Files
];








# General File Processing
def exists(PATH: str) -> bool:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Verifies whenever a file or folder exists at the provided path.

	Arguments:
		PATH (str): String representing the Path.

	Returns:
		bool: If the file or a folder exists according to `Path`, returns True, otherwise False.

	Examples:
		>>> File.exists("README.MD");
		True
	"""
	return pathlib.Path(PATH).exists();





def ls(PATH: str = ".") -> Folder_Contents:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Returns a matrix of the folders and files inside Path.

	Arguments:
		Path (str): The folder we wish to view the contents of.

	Returns:
		Folder_Contents: A tuple containing two other tuples, the first containing folders, the second files.

	Examples:
		>>> File.ls("TSN_Abstracter");
		(
			('__pycache__',), # Reminder that a `,` inside a tuple of a single element is required or otherwise Python thinks it's a literal which is BAD
			('String.py', 'Cryptography.py', 'Time.py', 'File.py', 'Log.py', 'Misc.py', '__init__.py', 'Config.py', 'Safe.py', 'TSNDL.py')
		)
	"""
	if (not exists(PATH)): return ((), ());
	Results = next(os.walk(PATH));

	return (
		tuple(sorted(Results[1])),
		tuple(sorted(Results[2]))
	);



def tree(PATH: str = ".") -> Folder_Matrix:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Returns a matrix of ALL folders and files inside Path.  
	**WARNING**: You will loose your sanity using this function.

	Arguments:
		Path (str): The folder we wish	 to view the contents of, including its sub-folders.

	Returns:
		ARRAY containing two arrays, the first one being a list of folders, and the second one being files.  
		Each folder in the first array is in reality

	Examples:
		>>> File.tree();
		(
			'.',
			(
				(
					'./__pycache__',
					(),
					(
						'Archive.cpython-313.pyc',
						'Globals.cpython-313.pyc',
						'Interface.cpython-313.pyc',
						'Mika.cpython-313.pyc',
						'Nagisa.cpython-313.pyc',
						'Type.cpython-313.pyc',
						'__init__.cpython-313.pyc'
					)
				),
			),
			(
				'Globals.py',
				'Interface.py',
				'Mika.py',
				'Nagisa.py',
				'Type.py',
				'__init__.py'
			)
		)
	"""
	if (not exists(PATH)): return (os.path.dirname(PATH), (), ());

	RESULTS: Folder_Contents = ls(PATH);
	return (
		PATH,
		tuple([tree(f"{PATH}/{FOLDER}") for FOLDER in RESULTS[0]]),
		RESULTS[1]
	);








# Path Manipulation
class Path:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Class full of methods to easily manipulate folders.
	"""
	@staticmethod
	def create(PATH: str) -> bool:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Creates the full folder structure specified. Equivalent to `mkdir -p`.

		Arguments:
			PATH (str): String representing the Path of folders you wish to create.

		Returns:
			bool: Represents whenever the action was successful.

		Examples:
			>>> File.Path.create("super secret folder/dont look big silly/ok fine there it is/theres nothing here are you happy");
			True
		"""
		PATH_FOLDER: str = Path.folder(PATH);
		if (PATH_FOLDER == ""): return True; # Unfucking "User" error

		try: os.makedirs(PATH_FOLDER); return True;
		except Exception as Error:
			Log.Error(f"Create Folder Structure: \"{PATH_FOLDER}\"\n{String.ASCII.Shortcut.BSOD}{Error}");
			return False;



	@staticmethod
	def require(PATH: str) -> bool:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Similar to `Path.create()`, but instead specifies if the folder structure already existed before.

		Arguments:
			Path (str): String representing the Path of folders you wish to require.

		Returns:
			bool: Represents if the folder structure already existed before.

		Examples:
			>>> File.Path.require("i didnt exist before/hehehe");
			False
		"""
		PATH_FOLDER: str = Path.folder(PATH);
		if (exists(PATH_FOLDER) or PATH_FOLDER == ""):
			return True;
		Path.create(PATH_FOLDER); # This doesn't handle exceptions properly when wrapped in this function... Needs fixing
		return False;



	@staticmethod
	def folder(PATH: str) -> str:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Takes in a Path and returns itself, minus the file name at the end if it exists by checking for "." and "/" in the filename.  

		Arguments:
			Path (str): String representing the Path of a file or folder where we wish to remove the file from the string.

		Returns:
			str: The same path string, devoid of the file at the end.

		Examples:
			>>> File.Path.folder("trade_secrets/hubert.txt");
			"trade_secrets"
		"""
		return os.path.dirname(PATH);
		"""
		absolute: bool = True if (PATH[:1] == "/") else False;
		if (PATH[-1] == "/"): return PATH;

		if ("." not in PATH): return PATH;
		path_folders: list[str] = PATH.split("/");
		path_folders.pop(-1);
		return "/" if (absolute) else "" + "/".join(path_folders);
		"""








def read(PATH: str, COMPRESSED: bool = False) -> str | None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Read the contents of a file, supports LZMA COMPRESSED files.

	Arguments:
		Path (str): String representing the Path to a file.
		COMPRESSED (bool = False): Specify the use of LZMA Compression.

	Returns:
		str/None: If the file or a folder exists according to "Path", returns its data, otherwise None.

	Examples:
		>>> File.read("Mika.ctxt", True);
		"Hug a Mika a night, keeps your smile shinning bright~"
	"""
	if exists(PATH):
		Log.TSN_Debug(f"Reading {PATH} - Compression: {COMPRESSED}...");
		try:
			if (COMPRESSED):
				with lzma.open(PATH, "rt") as FILE: data = FILE.read();
			else:
				with open(PATH, "r", encoding="UTF8") as FILE: data = FILE.read(); # pyright: ignore[reportConstantRedefinition] // you are fucking stupid pyright

			Log.Awaited().Status_Update(f"[OK] - {len(data)} characters\n{String.ASCII.Text.Dim}{data}", 10); return data;

		except Exception as Except:
			if (not Log.Can_Log(10)): Log.Error(f"Reading {Path} - Compression {COMPRESSED}\n{String.ASCII.Shortcut.BSOD}{Except}");
			else: Log.Awaited().EXCEPTION(Except);

	return None;



def write(PATH: str, DATA: str, COMPRESSED: bool = False, APPEND: bool = False) -> bool:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Write the contents of a string to a file, supports LZMA COMPRESSED files.
	
	Arguments:
		Path (str): String representing the Path to a file.
		Data (str): Whichever data we wish to write to the file.
		COMPRESSED (bool = False): Specify the use of LZMA Compression.

	Returns:
		bool: Represents whenever the write was successful.

	Examples:
		>>> File.write("README.MD", "haha made you look");
		True
	"""
	mode: str = "a" if (APPEND) else "w";

	if (exists(Path.folder(PATH))):
		Log.TSN_Debug(f"Writing {PATH} - Compression: {COMPRESSED} - Mode: {mode} - Data:\n{String.ASCII.Text.Dim}{DATA}{String.ASCII.Text.Dim_OFF}\n({len(DATA)} characters)...");
		try:
			if (COMPRESSED):
				with lzma.open(PATH, mode) as FILE: FILE.write(DATA.encode("utf-8"));
			else:
				with open(PATH, mode, encoding="UTF-8") as FILE: FILE.write(DATA); # pyright: ignore[reportConstantRedefinition] // you are fucking stupid pyright

			Log.Awaited().OK(); return True;
		except Exception as Except:
			if (not Log.Can_Log(10)): Log.Error(f"{'Writing' if (mode == "w") else 'Appending'} {PATH} - Compression: {COMPRESSED} - Data: {len(DATA)} Characters\n{String.ASCII.Shortcut.BSOD}{Except}");
			else: Log.Awaited().EXCEPTION(Except);
	return False;








# JSON Specific Abstraction
def readJSON(PATH: str, COMPRESSED: bool = False) -> dict[str, Any]:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	`read()` Wrapper for reading JSON Files.  
	**QUIRK**: Automatically creates the file path if it doesn't exist, returns an empty dictionary if the file didn't exist prior.
	
	Arguments:
		Path (str): String representing the Path to a json file.
		COMPRESSED (bool = False): Specify the use of LZMA Compression.

	Returns:
		dict: If the file or a folder exists according to "Path", returns its data, otherwise an empty dictionary is provided.

	Examples:
		>>> File.readJSON("BigData.cjson", True);
		{
			"Data": "big cheese redacted this :("
		}
	"""
	if (not Path.require(PATH)):
		Log.TSN_Debug(f"404 Warning - {PATH}"); return {};
	JSON: str | None = read(PATH, COMPRESSED);
	return json.loads(JSON if (JSON) else "{}");



def writeJSON(PATH: str, Data: typing.Mapping[str, Any] | list[Any], COMPRESSED: bool = False) -> bool:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	`write()` Wrapper for writing JSON Files.  
	Automatically creates the file structure and file if it doesn't exist.
	
	Arguments:
		Path (str): String representing the Path to a json file.
		Data (dict / list): Serializable data that we want to write to a JSON File.
		COMPRESSED (bool = False): Specify the use of LZMA Compression.

	Returns:
		bool: Represents whenever the write was successful.

	Examples:
		>>> File.writeJSON("BigData.cjson", {"Cheese Stocks": 9001});
		True
	"""
	try:
		Path.require(PATH);
		return write(PATH, json.dumps(Data, indent=2 if (not COMPRESSED) else 0), COMPRESSED);
	except Exception as Error:
		Log.Error(f"Error Writing JSON {PATH}.\n\tDATA: {Data}\n\tEXCEPTION:{Error}");
	return False;



def appendJSON(PATH: str, Dictionary: typing.Mapping[str, Any], COMPRESSED: bool = False) -> bool:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	`write()` Wrapper for updating data to JSON Files.  
	**QUIRK**: Acts as a regular `writeJSON()` if the file did not exist prior.
	
	Arguments:
		Path (str): String representing the Path to a json file.
		Dictionary (dict): A serializable dictionary that we want to append to the JSON File.
		COMPRESSED (bool = False): Specify the use of LZMA Compression.

	Returns:
		bool: Represents whenever the write was successful.

	Examples:
		>>> File.writeJSON("BigData.json", {"Debt": 999999999});
		True
		# If you want to know how the file looks like after that operation...
		>>> File.readJSON("BigData.json");
		{
			"Cheese Stocks": 9001,
			"Debt": 999999999
		}
	"""
	try:
		if (not exists(PATH)): return writeJSON(PATH, Dictionary, COMPRESSED);

		JSON: dict[str, Any] = readJSON(PATH, COMPRESSED);
		JSON.update(Dictionary);
		return writeJSON(PATH, JSON, COMPRESSED);

	except Exception as Except: Log.Error(f"Updating {PATH} - Compression: {COMPRESSED}\n{String.ASCII.Shortcut.BSOD}{Except}");
	return False;





def readArray(PATH: str, COMPRESSED: bool = False) -> list[Any]:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	`readJSON()` alias, but instead of Dictionaries, it's Arrays.  
	This function has a very slight difference with `readJSON()`: it returns an empty list instead of an empty dictionary. """
	if (not Path.require(PATH)):
		Log.TSN_Debug(f"404 Warning - {PATH}"); return [];
	JSON: str | None = read(PATH, COMPRESSED);
	return json.loads(JSON if (JSON) else "[]");



def writeArray(PATH: str, ARRAY: list[Any], COMPRESSED: bool = False) -> bool:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	`writeJSON()` alias, but instead of Dictionaries it's Arrays.  
	This function directly calls `writeJSON()` and should only be used to make code easier to read and comprehend."""
	return writeJSON(PATH, ARRAY, COMPRESSED);



def appendArray(PATH: str, ARRAY: list[Any], COMPRESSED: bool = False) -> bool:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	`appendJSON()` alias, but instead of Dictionaries it's Arrays.  
	This function behaves identically to `appendJSON()`. """
	try:
		if (not exists(PATH)): return writeJSON(PATH, ARRAY, COMPRESSED);

		JSON: list[Any] = readArray(PATH, COMPRESSED);
		JSON.extend(ARRAY);
		return writeJSON(PATH, JSON, COMPRESSED);

	except Exception as Except: Log.Error(f"Updating {PATH} - Compression: {COMPRESSED}\n{String.ASCII.Shortcut.BSOD}{Except}");
	return False;