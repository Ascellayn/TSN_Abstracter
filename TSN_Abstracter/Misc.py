"""
This module from TSN Abstracter contains various random functions that currently do not deserve their own dedicated TSNA Module.

## Examples
>>> from TSN_Abstracter import Misc;
>>> 69/Misc.NotNull(0);
69 # The 0 was replaced with a 1, resulting in no Exceptions!
>>> 420/Misc.NotNull(0, 2);
210
"""
import multiprocessing, threading;

def Void() -> None:
	""" Does absolutely nothing. Frequently used when you want to ignore Exceptions.

	## Examples
	>>> try: print(80082/0);
	>>> except: Misc.Void();
	"""
	return None;



# Multi-Tasking
def Thread_Start(Function: callable, Arguments: list[object] = [], Daemon: bool = True) -> None: # type: ignore | "callable" isn't taken seriously
	""" Abstraction to launch a new thread

	Arguments:
		Function (callable*): The function you wish to execute in the new thread.
		Arguments (list[object] = []): A list of arguments to pass to the function.
		Daemon (bool = True): Whenever the thread should be treated as a daemon.
	
	Examples:
		>>> def Send_To_Brazil(Person: str, Politely: bool = True) -> None: ...;
		>>> Misc.Thread_Start(Send_To_Brazil, ["Ascellayn", False], False);
	"""
	threading.Thread(
		target=Function, # type: ignore | FUCK OFF
		args=Arguments,
		daemon=Daemon
	).start();

def Process_Start(Function: callable, Arguments: list[object] = [], Daemon: bool = True) -> None: # type: ignore | NAH WE SENDING THIS TO BRAZIL
	""" Abstraction to launch a new Process

	Arguments:
		Function (callable*): The function you wish to execute in the new process.
		Arguments (list[object] = []): A list of arguments to pass to the function.
		Daemon (bool = True): Whenever the process should be treated as a daemon.
	
	Examples:
		>>> def Send_To_France(Person: str, HonHon: bool = False) -> None: ...;
		>>> Misc.Process_Start(Send_To_Brazil, ["Arellayn", True]);
	"""
	multiprocessing.Process(
		target=Function, # type: ignore | @©ÞZAÆ<ØªıđÞ<¢243
		args=Arguments,
		daemon=Daemon
	).start();



# Integer related stuff
def NotNull(Number: int, Default: int = 1) -> int:
	""" Returns the `Number` unless it is 0, in this case we return whatever `Default` is set to.

	Arguments:
		Number (int*): Which number we want to check if it's potentially null.
		Default (int = 1): What integer we replace `Number` with.

	Returns:
		int: Either `Number` or `Default` depending on if `Number` is equal to zero.

	Examples:
		>>> 69/Misc.NotNull(0);
		69 # The 0 was replaced with a 1, resulting in no Exceptions!
		>>> 420/Misc.NotNull(0, 2);
		210 # 420/2 since a zero is a zero, shocking I know.
	"""
	if (Number == 0): return Default;
	return Number;

def is_Even(Number: int) -> bool:
	""" Checks if `Number` is even.

	Arguments:
		Number (int*): Which number we want to check if it's even.

	Returns:
		bool: True if it is, False otherwise.

	Examples:
		>>> Misc.is_Even(1);
		False
		>>> Misc.is_Even(1);
		True
	"""
	return ((Number % 2) == 0);