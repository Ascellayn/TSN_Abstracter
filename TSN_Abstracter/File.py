import TSN_Abstracter.Log as Log;
import json, os;

# General File Processing
def Exists(Path: str) -> bool:
    """
    Takes in a String representing a RELATIVE file path and returns a boolean if a file or folder exists in the specified path.
    
    Arguments:
        Path: String representing the RELATIVE Path.

    Returns:
        If the file or a folder exists according to "Path", returns True, otherwise False.
    """
    Path = Path_Folder(Path);
    return True if (os.path.isfile(Path) or os.path.isdir(Path)) else False;

def Read(Path: str) -> str:
    """
    Takes in a String representing a RELATIVE file path and returns the contents of the file specified.
    
    Arguments:
        Path: String representing the RELATIVE Path to a file.

    Returns:
        If the file or a folder exists according to "Path", returns its data, otherwise None.
    """
    if Exists(Path):
        try:
            with open(Path, "r", encoding="UTF8") as File:
                Data = File.read();
                Log.Debug(f"{Path}:\n'{Data}'");
                return Data;
        except Exception as Error:
            Log.Error(f"Failed to read file {Path}!\n\tEXCEPTION: {Error}");
    return None;

def Write(Path: str, Data: str) -> bool:
    """
    Takes in a String representing a RELATIVE file path and writes the contents specified in Data.
    
    Arguments:
        Path: String representing the RELATIVE Path to a file.
        Data: String representing the data to write.

    Returns:
        If the write was successful, return True. Otherwise False.
    """
    if Exists(Path):
        try:
            with open(Path, "w", encoding="UTF8") as File:
                Log.Debug(f"{Path}:\n'{Data}'");
                File.write(Data);
                return True;
        except Exception as Error:
            Log.Error(f"Failed to write file '{Path}'!\nData to be written:\n\tDATA: '{Data}'\n\tEXCEPTION: '{Error}'");
    return False;

# Path Manipulation
def Path_Create(Path: str) -> bool:
    """
    Creates the specified file path.

    Arguments:
        Path: String representing the RELATIVE folder path we want to create.

    Returns:
        Boolean telling us if the operation was successful or not.
    """
    Path = Path_Folder(Path);
    if (Path == ""): return; # Unfucking "User" error
    try:
        os.makedirs(Path);
        return True;
    except Exception as Error:
        Log.Error(f"Failed creating folder structure: '{Path}'\n\tEXCEPTION: '{Error}'");
        return False;

def Path_Require(Path: str) -> bool:
    """
    Checks the existence of the Path, if it doesn't then create it.
    
    Arguments:
        Path: String representing the RELATIVE folder path we want to check.

    Returns:
        Boolean telling us if the file path existed before.
    """
    if (Exists(Path)):
        return True;
    Path_Create(Path);
    return False;

def Path_Folder(Path: str) -> str:
    """
    Takes in a Path and returns itself, minus the file name at the end if it exists by checking for "." and "/" in the filename.  
    Yes this function is inherently complete garbage but it does the job good enough.
    
    Arguments:
        Path: String representing the RELATIVE file path we want to transform.

    Returns:
        String representing the Folder Path of the File Path.
    """
    if ("." in Path):
        Folder_Path = Path.split("/");
        Folder_Path.pop(-1);
        Path = "";
        for Folder in Folder_Path:
            Path += f"/{Folder}";
        Path = Path[1:] # Exclude the first "/", yeah this is janky.
    return Path;

# Other Functions
def List(Path: str) -> tuple:
    """
    Returns a matrix of the folders and files inside Path.

    Arguments:
        Path: String representing the RELATIVE folder path we want to check.

    Returns:
        Tuple containing two arrays, the first one being a list of folders, and the second one being files.
    """
    try:
        Results = next(os.walk(f"{os.getcwd()}/{Path}"));
        return (tuple(Results[1]), tuple(Results[2]));
    except Exception as Error:
        Log.Error(f"I'm not exactly sure how the fuck it would fail here so just in case, hello! Kosaka most likely gonna the shit thats gonna blow this function somehow.\n\tEXCEPTION: '{Error}'");
        return None;

def Tree(Path: str) -> tuple:
    """
    Returns a matrix of ALL folders and files inside Path.

    Arguments:
        Path: String representing the RELATIVE folder path we want to check.

    Returns:
        Array containing two arrays, the first one being a list of folders, and the second one being files.  
        Each folder in the first array is in reality
    """
    if Exists(Path):
        try:
            Results = List(Path); # The return looks retarded. But it works so I don't give a shit. Also oh no recursion
            return (tuple((Folder, Tree(f"{Path}/{Folder}")) for Folder in Results[0] if (Results[0] != None)), Results[1]);
        except Exception as Error:
            Log.Error(f"I'm not exactly sure how the fuck it would fail here so just in case, hello! Kosaka most likely gonna the shit thats gonna blow this function somehow.\n\tEXCEPTION: '{Error}'");
            return None;
    return None;

# JSON Specific Abstraction
def JSON_Load(Path: str) -> dict:
    if (Path_Require(Path)):
        return json.loads(Read(Path));
    return {};

def JSON_Write(Path: str, Dictionary: dict) -> bool:
    try:
        Path_Require(Path)
        Write(Path, json.dumps(Dictionary, indent=2));
        return True;
    except Exception as Error:
        Log.Error(f"Error Writing JSON {Path}.\n\tDATA: {Dictionary}\n\tEXCEPTION:{Error}")
    return False;