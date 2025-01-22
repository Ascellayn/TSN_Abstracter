import Global;
import logging, datetime, sys;

def Void() -> None: 
    """ Does absolutely nothing. """
    return None;

def Log(Text: str, Level: int = Global.INFO) -> None:
    """ Takes in a String "Text" in which this function will Log using Logger and, if "Level" which is an Integer that represents how severe the logged message is, if it is 20 or above, will display also in the Terminal. """
    # Verify the "logs" folder exists
    
    # Start logging stuff now
    Logger = logging.getLogger();
    Handlers = [ logging.FileHandler(filename=f"logs/{datetime.datetime.now().strftime("%Y-%m_%d")}.log") ]; # By default this function ALWAYS saves to a file.
    if (Level >= Global.INFO):
          Handlers.append(logging.StreamHandler(stream=sys.stdout)) # Displays Text to the Console
    logging.basicConfig(
        level = 20,
        format = "[%(asctime)s] - %(levelname)s: %(message)s",
        datefmt = "%Y/%m/%d - %H:%M:%S",
        handlers = Handlers
    );
    Logger.log(Level, Text);
    return None;