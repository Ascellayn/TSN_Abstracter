import threading, multiprocessing;

def Void() -> None: 
    """ Does absolutely nothing. """
    return None;

def Thread_Start(Function, Daemon: bool = True) -> None:
    """ Abstraction to launch a thread, takes in a function and a boolean if the thread should be a daemon or not. """
    threading.Thread(target=Function()).setDaemon(Daemon).start();
    return;

def Process_Start(Function, Daemon: bool = True) -> None:
    """ Abstraction to launch a Process. """
    multiprocessing.Process(target=Function()).start();
    return;

Loading_Index: int = 0;
def Loading_Spin() -> str:
    """ Returns a singular character used for the spinning / - \ | animation. """
    global Loading_Index; Loading_Index+=1;
    Loading_Characters: list = ["\\", "|", "/", "-"];
    if (Loading_Index != len(Loading_Characters)):
        return Loading_Characters[Loading_Index];
    Loading_Index: int = 0;
    return Loading_Characters[Loading_Index];
