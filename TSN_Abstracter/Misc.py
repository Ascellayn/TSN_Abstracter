"""
This module from TSN Abstracter contains various random functions that currently do not deserve their own dedicated TSNA Module.

## Examples
>>> from TSN_Abstracter import Misc;
>>> Misc.is_Even(32768);
True
"""
import multiprocessing, threading, typing;





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


def All_Includes(A: typing.Iterable[typing.Any], B: typing.Iterable[typing.Any]) -> bool:
	""" verify every item in B is present in A"""
	for Item in B:
		if (Item not in A): return False;
	return True;

def Under_At(A: tuple[int, ...] | list[int], B: tuple[int, ...] | list[int]) -> int:
	""" use to compare version tuples"""
	A_Length: int = len(B);
	for Index, Number in enumerate(B):
		if (Index == A_Length): break;
		if (Number > A[Index]): return Index;
	return -1;

def Nested_Get(Dict: dict[str, typing.Any], Keys: list[str], Default: typing.Any = None) -> typing.Any:
	""" safely get data from nested dicts with an argument for a default value """
	for Key in Keys:
		Dict = Dict.get(Key, Default);
	return Dict;