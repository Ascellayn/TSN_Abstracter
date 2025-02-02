import TSN_Abstracter.File as File;
import logging, datetime, sys, inspect;


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

def Log(Text: str, Level: int = 0) -> None:
    """
    Logs a specified message manually. Writes the log to a file and displays it to the console.

    Arguments:
        Text: String corresponding to the message to Log
        Level: Integer corresponding to how severe the message is.

    TODO:
        - Add config to prevent generation of logs
        - Make Logger Global so we don't have to redeclare EVERY TIME this shit
    """
    # Check if the Logs folder doesn't exist, create it if it isn't.
    File.Path_Require("logs");
    
    # Configure Logger
    Logger = logging.getLogger();
    Logger.setLevel(Level);

    Handlers = [];
    if (Level >= 10): # If this is a debug message, don't display to the console.
        Handlers.append(logging.StreamHandler(stream=sys.stdout));
    if (True): # TODO: add config to prevent generation of logs
        Handlers.append(logging.FileHandler(filename=f"logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log"));
    
    logging.basicConfig(
        format = "[%(asctime)s] - %(levelname)s: %(message)s",
        datefmt = "%Y/%m/%d - %H:%M:%S",
        handlers = Handlers
    );

    Logger.log(Level, f"{Get_Caller(3)}(): {Text}");


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
