""" This module from TSN Abstracter is in charge of providing functions related to Strings.

### Examples
>>> from TSN_Abstracter import String;
>>> String.Split_Length("The quick brown fox jumps over the lazy dog.", 16);
['The quick brown ', 'fox jumps over ', 'the lazy dog.']
"""
import re;
from typing import Any, Iterable;








# String Modification
def abbreviate(Text: str, MAX_LENGTH: int, ABBREVIATION: str = "(...)") -> str:
	""" Shortens end of text with `Abbreviate` if `Text` is longer than `Max_Length`

	Arguments:
		Text (str*): The string we want to potentially abbreviate.
		Max_Length (int*): The maximum size of the string.
		Abbreviate (str = "(...)"): The string to replace the end of the text with.

	Returns:
		str: The string with its end potentially replaced with `Abbreviate`
	"""
	if (len(Text) > MAX_LENGTH):
		Text = Text[:MAX_LENGTH - len(ABBREVIATION)] + ABBREVIATION;
	return Text;



def trailingZero(NUMBER: int, ZEROS: int = 2) -> str:
	""" Adds trailing Zeros to a specified Number.

	Arguments:
		Number (int*): The Number we want to potentially add zeros at the start.
		Zeros (int = 2): The amount of digits we aim to have at the end.

	Returns:
		str: The Number, now with its trailing zeros added if needed.

	Examples:
		>>> Time.Trailing_Zero(69, 3);
		"069"
	"""
	max_digits: int = len(str(NUMBER));
	extra_zeros: int = ZEROS - max_digits;

	if (max_digits >= ZEROS): return str(NUMBER);
	return f"{'0'*extra_zeros}{str(NUMBER)}";



def ifyArray(ARRAY: list[Any] | tuple[Any, ...]) -> list[str]:
	""" Transforms everything inside `Array` into strings.

	Arguments:
		Array (list[Any] | tuple[Any, ...]*): The array we wish to turn all its items into strings.

	Returns:
		list[str]: A newly formed list with all of the elements of `Array` as strings.

	Examples:
		>>> String.ify_Array([1.9.4]);
		["1", "9", "4"]
	"""
	return [str(ITEM) for ITEM in ARRAY];



def lengthSplit(Text: str, MAX_LENGTH: int) -> list[str]:
	""" Splits a string after a new line (unless there are no line breaks, in that case it will stop after a space, otherwise raw cuts through words if neither lines breaks nor spaces are present) into an array according to Max_Length.

	Arguments:
		Text (str*): The string we want to split.
		MAX_LENGTH (int*): The maximum size of each string element.

	Returns:
		list[str]: A list containing the split text, each of around `MAX_LENGTH` in size.
	"""
	def splitRaw() -> None: String_List.append(Text[:MAX_LENGTH]);

	def splitLine(PString: str) -> int:
		end: int = len(PString) - PString.index("\n");
		String_List.append(Text[:end]);
		return end;

	def splitSpace(PString: str) -> int:
		end: int = len(PString) - PString.index(" ");
		String_List.append(Text[:end]);
		return end;


	String_List: list[str] = [];
	while (Text != ""):
		string_current: str = Text[:MAX_LENGTH][::-1];
		if (len(string_current) != len(Text)):
			if ("\n" in string_current): Text = Text[splitLine(string_current):]; continue;
			if (" " in string_current): Text = Text[splitSpace(string_current):]; continue;
		splitRaw(); Text = Text[MAX_LENGTH:];

	return String_List;



def bulkReplace(REPLACERS: Iterable[tuple[str, str] | list[str] | str], String: str, NEW: str = "") -> str:
	""" Bulk replaces every string in `String` to `New` or the 2nd element of a pair inside `Replacers`.

	Arguments:
		Replacers (list[tuple[str, str] | list[str] | str]*): A list of strings or a list of lists/tuples containing the first element being which element to replace within `String` to replace with the second element of the pair.
		String (str*): The string to replace stuff from.
		New (str = ""): If `Replacers` isn't in pairs of strings, the replaced string will have the value of `New`.

	Returns:
		str: The string with all its replacements done.

	Examples:
		>>> String.Bulk_Replace([
			("sanity away", "smile shinning bright"),
			"day"
		], "Hug a Mika a day keeps your sanity away.", "night");
		"Hug a Mika a night keeps your smile shinning bright."
	"""
	for ITEM in REPLACERS:
		if (isinstance(ITEM, str)): String = String.replace(ITEM, NEW);
		else: String = String.replace(ITEM[0], ITEM[1]);
	return String;








class ASCII:
	""" A class containing numerous ASCII Escape Sequences to aid with formatting. """
	Clear_Screen: str = "\x1b[2J";





	@staticmethod
	def clearFormatting(TEXT: str) -> str:
		""" This function takes in a String and then clears out all the ASCII Formatting according to the TF/FC/BC objects. Used for making Log files look cleaner.

		Arguments:
			Text (str*): A "dirty" Log String that was supposed to be destined for printing on the Console.

		Returns:
			str: A "clean" Log String devoid of special ASCII Formatting text.
		"""
		return re.sub(r"\[[\d;]*m", "", TEXT);





	class Shortcut:
		""" A class containing frequently used ASCII Escape Sequences combinaisons. """
		BSOD: str = "\x1b[48;2;40;0;255m\x1b[38;2;255;250;255m";



	class Text:
		""" A class containing numerous ASCII Escape Sequences to aid with text formatting. """
		Reset: str = "\x1b[0m"; Reset_Color: str = "\x1b[39m\x1b[49m";
		Bold: str = "\x1b[1m"; Bold_OFF: str = "\x1b[24m";
		Dim: str = "\x1b[2m"; Dim_OFF: str = "\x1b[22m";
		Underline: str = "\x1b[4m"; Underline_OFF: str = "\x1b[24m";
		Blink: str = "\x1b[5m"; Blink_OFF: str = "\x1b[25m";
		Reverse: str = "\x1b[7m"; Reverse_OFF: str = "\x1b[27m";
		Hide: str = "\x1b[8m"; Hide_OFF: str = "\x1b[28m";

	class Line:
		""" A class containing numerous ASCII Escape Sequences to aid with clearing lines of text. """
		Return: str = "\x1b[1A\x1b[2K";
		Clear: str = "\x1b[2K";
		Erase_Forward: str = "\x1b[K";





	class Cursor:
		""" A class containing numerous ASCII Escape Sequences to aid with cursor movement. """
		@staticmethod
		def Save() -> str:
			""" Save the current cursor position.

			Returns:
				str: An ASCII escape sequence that saves the current cursor position.
			"""
			return f"\x1b[s";

		@staticmethod
		def Load() -> str:
			""" Load the saved cursor position.

			Returns:
				str: An ASCII escape sequence that loads the last saved cursor position.
			"""
			return f"\x1b[u";

		@staticmethod
		def Move(X: int, Y: int) -> str:
			""" Move the cursor to Line X and Column Y.

			Arguments:
				X (int*): The Line to go to.
				Y (int*): The Column to go to.
			
			Returns:
				str: An ASCII escape sequence that makes the cursor go to Line X and Column Y.
			"""
			return f"\x1b[{X};{Y}H";



		@staticmethod
		def Up(Lines: int) -> str:
			""" Move the cursor up `Lines` lines.

			Arguments:
				Lines (int*): The amount of lines we want to go up.
			
			Returns:
				str: An ASCII escape sequence that makes the cursor go up `Lines` lines.
			"""
			return f"\x1b[{Lines}A";

		@staticmethod
		def Down(Lines: int) -> str:
			""" Move the cursor down `Lines` lines.

			Arguments:
				Lines (int*): The amount of lines we want to go down.
			
			Returns:
				str: An ASCII escape sequence that makes the cursor go down `Lines` lines.
			"""
			return f"\x1b[{Lines}B";

		@staticmethod
		def Right(Columns: int) -> str:
			""" Move the cursor right `Columns` columns.

			Arguments:
				Columns (int*): The amount of columns we want to go right.
			
			Returns:
				str: An ASCII escape sequence that makes the cursor go right `Columns` characters.
			"""
			return f"\x1b[{Columns}C";

		@staticmethod
		def Left(Columns: int) -> str:
			""" Move the cursor left `Columns` columns.

			Arguments:
				Columns (int*): The amount of columns we want to go left.
			
			Returns:
				str: An ASCII escape sequence that makes the cursor go left `Columns` characters.
			"""
			return f"\x1b[{Columns}D";