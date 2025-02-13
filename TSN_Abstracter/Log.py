import TSN_Abstracter.Config as Config;
import TSN_Abstracter.File as File;
import datetime, inspect, logging, shutil, sys;

# My hope is that the "await" status system is so fucking bad that I'm NEVER EVER ALLOWED TO TOUCH PYTHON CODE IN MY ENTIRE LIFE EVER AGAIN
Await_Status = False;
Await_Level = 0;
Await_Text = "";
Await_Caller = "";
Last_Awaited = False;


# Simplified logging functions
def Debug(Text: str) -> None:
    """ Debug Log """
    Log(Text=Text, Level=10);

def Info(Text: str) -> None:
    """ Info Log """
    Log(Text=Text, Level=20);

def Warning(Text: str) -> None:
    """ Warning Log """
    Log(Text=Text, Level=30);

def Error(Text: str) -> None:
    """ Error Log """
    Log(Text=Text, Level=40);

def Critical(Text: str) -> None:
    """ Critical Log """
    Log(Text=Text, Level=50);

def Log(Text: str, Level: int = 0, Caller: str = "") -> None:
    """
    Logs a specified message manually. Writes the log to a file and displays it to the console.

    Arguments:
        Text: String corresponding to the message to Log
        Level: Integer corresponding to how severe the message is.

    TODO:
        - Add config to prevent generation of logs
        - Make Logger Global so we don't have to redeclare EVERY TIME this shit
    """
    # We edit these global variables so that using Status_Update() is much less painful on the "user" side.
    global Await_Status, Await_Level, Await_Text, Await_Caller, Last_Awaited;

    # Check if the Logs folder doesn't exist, create it if it isn't.
    File.Path_Require("logs");
    
    # Configure Logger
    Logger = logging.getLogger(__name__);
    Logger.setLevel(Level);

    # Handlers
    Handlers = [];
    Logger.handlers.clear(); # Clearing handlers otherwise the fucking conditions compared to the config never work?????
    if (Level >= Config.Logging["Print_Level"]): # If this is a debug message, don't display to the console.
        Handlers.append(logging.StreamHandler(stream=sys.stdout));
    if (Config.Logging["File"] and (Level >= Config.Logging["File_Level"])):
        Handlers.append(logging.FileHandler(filename=f"logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log"));
    
    # Get function name that called the logger
    if (Caller == ""):
        Caller = Get_Caller(3);
    
    # Detects if the logged text is going to await a status update and changes the terminator accordingly, includes prefix.
    Prefix = "\n" if (Last_Awaited) else "";
    Terminator = "\n";
    if (Text != None): # Avoids Exception if Text is None which actually can happen due to coding errors on whichever script is using this module
        if ("..." == Text[-3:]):
            Terminator = "";
            Await_Status = True;
            Await_Level = Level;
            Await_Text = Text;
            Await_Caller = Caller;
            Last_Awaited = True;
        else:
            Last_Awaited = False;

    Format = logging.Formatter(
        fmt = f"{Prefix}[%(asctime)s] - %(levelname)s: %(message)s", 
        datefmt = "%Y/%m/%d - %H:%M:%S"
    );

    for Handler in Handlers:
        Handler.terminator = Terminator;
        Handler.setFormatter(Format);
        Logger.addHandler(Handler);

    Logger.log(Level, f"{Caller}() - {Text}");

# Logging Dependencies
def Get_Caller(Depth: int = 2) -> str:
     """
     Gives the name of the function who called the function where this function is executed OR the filename where the function was executed if the function returned is "<module>".

     Arguments:
        Depth: Integer representing how far we go back to get the function name. By default it is 2.
     
     Returns:
        String with the name of the function or module name.
     """
     Function = inspect.getouterframes(inspect.currentframe())[Depth][3];
     if (Function == "<module>"):
         Function = __name__;
     return Function;

# Miscellaneous Logging
def Status_Update(Text: str) -> None:
    """
    Replaces the last 3 characters (which are assumed to be "...", done automatically) with {Text}. Used to show progress with statuses such as "[OK]".  
    This functions handles also making changes to the Log file, although the assumed "..." will NOT be removed.
    """
    global Await_Status, Last_Awaited;
    if (Await_Status and Last_Awaited):
        print(f"\033[3D {Text}");
        if (Config.Logging["File"] and (Await_Level >= Config.Logging["File_Level"])):
            Logger = logging.getLogger(__name__);
            Logger.handlers.clear();
            Logger.addHandler(logging.FileHandler(filename=f"logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log"))
            Logger.log(msg=f" {Text}", level=Await_Level)
    else:
        Log(Await_Text.replace("...", f" {Text}"), Await_Level, Await_Caller);
    Await_Status = Last_Awaited = False;


def OK() -> None:
    """ [OK] Status Update shortcut"""
    Status_Update(f"[OK]");

def ERROR(Except: Exception) -> None:
    """ [ERROR] Status Update shortcut"""
    Status_Update(f"[ERROR]\n\tEXCEPTION: {Except}");

def Carriage(Text: str) -> None:
    """
    Prints using "\r" while also completely clearing the line to be sure there won't be artifacts from the previous text.
    """
    print(" "*shutil.get_terminal_size()[0], end="\r");
    print(Text, end="\r");

def Clear() -> None:
    """
    Simply empties the entire console's text.
    """
    print(f"\033[2J");

def Delete() -> None:
    """
    COMPLETELY Empties the latest Log File.
    """
    Clear();
    Critical("=== DELETING THE LOG FILE! ===");
    File.Write(f"logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log", "");