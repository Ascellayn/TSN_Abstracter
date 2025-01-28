from TSN_Abstracter.Debugger import *;
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
    return True if (os.path.isfile(Path) or os.path.isdir(Path)) else False;

def Read(Path: str) -> str:
    """ Docs TBW """
    if Exists(Path):
        try:
            with open(Path, "r", encoding="UTF8") as File:
                return File.read();
        except:
            L_Error(f"Failed to read file {Path}!\nEXCEPTION: {Exception}");
    return None;

def Write(Path: str, Data: str) -> bool:
    """ Docs TBW """
    if Exists(Path):
        try:
            with open(Path, "w", encoding="UTF8") as File:
                File.write(Data);
                return True;
        except:
            L_Error(f"Failed to write file {Path}!\nData to be written:\n{Data}\nEXCEPTION: {Exception}");
    return False;


# Path Manipulation
def Path_Create(Path: str) -> bool:
    try:
        os.makedirs(Path);
        return True;
    except:
        L_Error(f"Failed creating folder structure: {Path}\nEXCEPTION: {Exception}");
        return False;

def Path_Exists(Path: str) -> bool:
    return os.path.isPath(Path);


# Other Functions
def Tree(Path: str) -> list:
    """
    Returns a matrix of all folders and files inside Path.

    Arguments:
        Path: String representing the RELATIVE folder path we want to check.

    Returns:
        Array containing two arrays, the first one being a list of folders, and the second one being files.
    """
    try:
        Results = next(os.walk(f"{os.getcwd()}/{Path}"));
        return [Results[1], Results[2]];
    except:
        L_Error(f"I'm not exactly sure how the fuck it would fail here so just in case, hello! Kosaka most likely gonna the shit thats gonna blow this function somehow. \n {Exception}");
        return None;


# Deprecated
def JSON_Load(Path: str) -> dict:
    JSON_Exists(Path); # If shit hits the fan we should still get an empty dict
    with open(Path, "r", encoding="UTF-8") as JSON:
        return json.load(JSON);
    
def JSON_Write(Path: str, Dictionary: dict) -> None:
    JSON_Exists(Path)
    with open(Path, "w", encoding="UTF-8") as JSON:
        JSON.write(json.dumps(Dictionary, indent=2));
        return None;

def JSON_Exists(Path: str) -> bool:
    if ('/' in Path): # Creates the corresponding folder structure if it doesn't exist.
        Path_Array = Path.split("/");
        Path = "";

        for Path_Index in range (len(Path_Array)):
            if (Path_Index >= (len(Path_Array) -1)): break;
            Path += f"{Path_Array[Path_Index]}/";
        mkdir(Path)

    if (Path_Exists(Path) == False):
        with open(Path, "w", encoding="UTF-8") as JSON:
            JSON.write("{}");
        return False;
    return True;