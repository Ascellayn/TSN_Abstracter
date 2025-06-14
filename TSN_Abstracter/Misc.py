import threading, multiprocessing;

def Void() -> None: 
	""" Does absolutely nothing. """
	return None;

def Thread_Start(Function, Arguments: tuple = (), Daemon: bool = True) -> None:
	""" Abstraction to launch a thread, takes in a function and a boolean if the thread should be a daemon or not. """
	threading.Thread(
		target=Function,
		args=Arguments, 
		daemon=Daemon
	).start();
	return;

def Process_Start(Function, Daemon: bool = True) -> None:
	""" Abstraction to launch a Process. """
	multiprocessing.Process(target=Function()).start();
	return;