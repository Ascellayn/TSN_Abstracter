"""
This module from TSN Abstracter contains various random functions that currently do not deserve their own dedicated TSNA Module.

## Examples
>>> from TSN_Abstracter import Misc;
>>> Misc.is_Even(32768);
True
"""
import multiprocessing, threading;





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






def Under_At(A: tuple[int | float, ...] | list[int], B: tuple[int | float, ...] | list[int | float]) -> int:
	""" Specify at which index a value of A is under B. Returns `-1` if no value is.

	Arguments:
		A (tuple[int | float, ...] | list[int | float]*): The iterable of numbers we wanna know the index of the value under B.
		B (tuple[int | float, ...] | list[int | float]*): The iterable of numbers to compare A to.

	Returns:
		int: The index of A[x] that is under B[x]. Returns `-1` if it never happens.

	Examples:
		>>> Misc.Under_At([1,5], [1,6]);
		1
		>>> Misc.Under_At([1,8], [1,6]);
		-1
	"""
	A_Length: int = len(B);
	for Index, Number in enumerate(B):
		if (Index == A_Length): break;
		if (Number > A[Index]): return Index;
	return -1;