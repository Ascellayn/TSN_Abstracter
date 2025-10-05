"""
This module from TSN Abstracter is in charge of providing ways to access elements without causing exceptions.

## Examples
>>> from TSN_Abstracter import Safe;
>>> Array: list[str] = ["Arellayn was here"];
>>> Safe.Index(Array, 0);
"Arellayn was here"
>>> Safe.Index(Array, 1);
None
"""





def Index(Array: list[object], Index: int) -> object: # Isn't there a Python function to already do this?
	"""
	Attempts to safely try to read an array's specified index.

	Arguments:
		Array (list[object]*): The List that we want to check a specific index.
		Index (int*): The Index element we want to read.

	Returns:
		object/None: The returned item can be anything. In the case of a failed read, the return value will always be None.

	Examples:
		>>> Array: list[str] = ["Arellayn was here"];
		>>> Safe.Index(Array, 0);
		"Arellayn was here"
		>>> Safe.Index(Array, 1);
		None
	"""
	if (Index > len(Array)): return None;
	return Array[Index];