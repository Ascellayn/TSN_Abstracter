""" ***Implemented in __TSNA `v7.0.0`__***  

This module from TSN Abstracter contains functions related to parallel processing.  
"""
from typing import Any;
from collections.abc import Callable;

import multiprocessing, threading;








def newThread(FUNC: Callable[..., Any], ARGS: list[object] = [], DAEMON: bool = True) -> threading.Thread:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Abstraction to launch a new thread.

	Arguments:
		Function (Callable): The function you wish to execute in the new thread.
		Arguments (list[object] = []): A list of arguments to pass to the function.
		Daemon (bool = True): Whenever the thread should be treated as a daemon.
	
	Examples:
		>>> def Send_To_Brazil(Person: str, Politely: bool = True) -> None: ...;
		>>> Misc.Thread_Start(Send_To_Brazil, ["Ascellayn", False], False);
	"""
	t: threading.Thread = threading.Thread(
		target=FUNC,
		args=ARGS,
		daemon=DAEMON
	); t.start();

	return t;





def newProcess(FUNC: Callable[..., Any], ARGS: list[object] = [], DAEMON: bool = True) -> multiprocessing.Process: 
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Abstraction to launch a new Process.

	Arguments:
		Function (Callable): The function you wish to execute in the new process.
		Arguments (list[object] = []): A list of arguments to pass to the function.
		Daemon (bool = True): Whenever the process should be treated as a daemon.
	
	Examples:
		>>> def Send_To_France(Person: str, HonHon: bool = False) -> None: ...;
		>>> Misc.Process_Start(Send_To_Brazil, ["Arellayn", True]);
	"""
	p: multiprocessing.Process = multiprocessing.Process(
		target=FUNC,
		args=ARGS,
		daemon=DAEMON
	); p.start();
	return p;