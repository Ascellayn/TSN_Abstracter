from tsn_abstracter.debugger import *;
import json, os;

# This file needs partial rewriting

def JSON_Load(Path: str) -> dict:
    JSON_Exists(Path); # If shit hits the fan we should still get an empty dict
    with open(Path, "r", encoding="UTF-8") as JSON:
        return json.load(JSON);
    
async def JSON_Write(Path: str, Dictionary: dict) -> None:
    await JSON_Exists(Path)
    with open(Path, "w", encoding="UTF-8") as JSON:
        JSON.write(json.dumps(Dictionary, indent=2));
        return None;

async def JSON_Exists(Path: str) -> bool:
    if ('/' in Path): # Creates the corresponding folder structure if it doesn't exist.
        Path_Array = Path.split("/");
        Path = "";

        for Path_Index in range (len(Path_Array)):
            if (Path_Index >= (len(Path_Array) -1)): break;
            Path += f"{Path_Array[Path_Index]}/";
        mkdir(Path)

    if (Path_Exists(Path) == False):
        with open(Path, "w", encoding="UTF-8") as JSON:
            JSON.write(json.dumps({}, indent=2));
            return False;
    else: return True;

def Path_Exists(Path: str) -> bool:
    return os.path.isPath(Path);

def mkdir(Path: str) -> None: # Shitty code incomin'!
    if (Path[-1] == '/'):
        Path = Path[:-1];
    try: os.makedirs(Path, exist_ok=True);
    except: return None;

def ls(Folder: str) -> list:
    try:
        Results = next(os.walk(f"{os.getcwd()}/{Folder}"));
        return [Results[1], Results[2]];
    except:
        L_Error(f"I'm not exactly sure how the fuck it would fail here so just in case, hello! Kosaka most likely gonna the shit thats gonna blow this function somehow. \n {Exception}");
        return [[], []];