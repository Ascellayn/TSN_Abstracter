"""
This module from TSN Abstracter contains functions related to processing numbers.  
"""










def underAt(A: tuple[int | float, ...] | list[int], B: tuple[int | float, ...] | list[int | float]) -> int:
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
	for i, n in enumerate(B):
		if (i == A_Length): break;
		if (n > A[i]): return i;
	return -1;