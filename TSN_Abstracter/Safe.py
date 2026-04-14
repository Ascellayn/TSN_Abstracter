""" This module from TSN Abstracter is in charge of providing ways to access elements without causing exceptions.

## Examples
>>> from TSN_Abstracter import Safe;
>>> Array: list[str] = ["Arellayn was here"];
>>> Safe.Index(Array, 0);
"Arellayn was here"
>>> Safe.Index(Array, 1);
None
"""
from typing import Any;





def Index(Array: list[object], Index: int) -> Any: # Isn't there a Python function to already do this?
	""" Attempts to safely try to read an array's specified index.

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



def NotNull(Number: int | float, Default: int = 1) -> int | float:
	""" Returns the `Number` unless it is 0, in this case we return whatever `Default` is set to.

	Arguments:
		Number (int*): Which number we want to check if it's potentially null.
		Default (int = 1): What integer we replace `Number` with.

	Returns:
		int: Either `Number` or `Default` depending on if `Number` is equal to zero.

	Examples:
		>>> 69/Safe.NotNull(0);
		69 # The 0 was replaced with a 1, resulting in no Exceptions!
		>>> 420/Safe.NotNull(0, 2);
		210 # 420/2 since a zero is a zero, shocking I know.
	"""
	if (Number == 0): return Default;
	return Number;



def Nested_Dict(Dict: dict[str, Any], Keys: list[str], Default: Any = None) -> Any:
	""" Safely retrieve the data from a nested dictionary, returns `Default` when the function fails due to a key not existing.

	Arguments:
		Dict (dict[str, Any]*): The dictionary we wish to retrieve data from its sub-dictionaries.
		Keys (list[str]*): A list of key strings we wish to go through in the Dictionary.
		Default (Any = None): The value to return when no data from Dict[*Keys] can be retrieved.

	Returns:
		Any: The data from `Dict[Keys[0]][Keys[1]][...]`

	Examples:
		>>> Safe.Nested_Dict({
			"Hello": {
				"ItAppearsThat": "I am very silly"
			}
		}, ["Hello", "ItAppearsThat"]);
		"I am very silly"
		>>> Safe.Nested_Dict({
			"Hello": {
				"ItAppearsThat": "I am very silly"
			}
		}, ["Hello", "WeHaveBeenTryingToReachYouAboutYourCarsExtendedWarranty"], "NO");
		"NO"
	"""
	for Key in Keys:
		if (type(Dict) != dict): return Default;
		Dict = Dict.get(Key, Default);
	return Dict;