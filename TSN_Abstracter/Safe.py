def Index(Array: list, Index: int): # Isn't there a Python function to already do this?
	"""
	Attempts to safely try to read an array's specified index.

	Arguments:
		Array: The List that we want to check a specific index.
		Index: The Index element we want to read.
	Returns:
		The returned item can be anything. In the case of a failed read, the return value will always be none.
	"""
	if (Index > len(Array)): return None;
	return Array[Index];