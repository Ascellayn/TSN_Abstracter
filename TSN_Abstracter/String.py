""" This module from TSN Abstracter is in charge of providing functions related to Strings.

Example:
	>>> from TSN_Abstracter import String;
	>>> String.Split_Length("The quick brown fox jumps over the lazy dog.", 16);
	['The quick brown ', 'fox jumps over ', 'the lazy dog.']
"""
import re;





def Split_Length(Text: str, Max_Length: int) -> list[str]:
	""" Splits a string after a new line (unless there are no line breaks, in that case it will stop after a space, otherwise raw cuts through words if neither lines breaks nor spaces are present) into an array according to Max_Length.

	Arguments:
		Text (str*): The string we want to split.
		Max_Length (int*): The maximum size of each string element.

	Returns:
		list[str]: A list containing the split text, each of around `Max_Length` in size.
	"""
	def Raw_Split() -> None: String_List.append(Text[:Max_Length]);

	def Line_Split(PString: str) -> int:
		End: int = len(PString) - PString.index("\n")
		String_List.append(Text[:End]);
		return End;

	def Space_Split(PString: str) -> int:
		End: int = len(PString) - PString.index(" ")
		String_List.append(Text[:End]);
		return End;



	String_List: list[str] = [];
	while (Text != ""):
		String_Current = Text[:Max_Length][::-1];
		if (len(String_Current) != len(Text)):
			if ("\n" in String_Current): Text = Text[Line_Split(String_Current):]; continue;
			if (" " in String_Current): Text = Text[Space_Split(String_Current):]; continue;
		Raw_Split(); Text = Text[Max_Length:];

	return String_List;





def Clear_ASCII_Formatting(Text: str) -> str:
	""" This function takes in a String and then clears out all the ASCII Formatting according to the TF/FC/BC objects. Used for making Log files look cleaner.

	Arguments:
		Text (str*): A "dirty" Log String that was supposed to be destined for printing on the Console.

	Returns:
		str: A "clean" Log String devoid of special ASCII Formatting text.
	"""
	return re.sub(r"\u001b\[\d*m", "", Text);




class ASCII:
	""" A class containing numerous ASCII Escape Sequences to aid with formatting. """
	Clear_Screen: str = "\x1b[2J";

	class Line:
		""" A class containing numerous ASCII Escape Sequences to aid with clearing lines of text. """
		Return: str = "\x1b[1A\x1b[2K";
		Clear: str = "\x1b[2K";
		Erase_Forward: str = "\x1b[K";

	class Text:
		""" A class containing numerous ASCII Escape Sequences to aid with text formatting. """
		Reset: str = "\x1b[0m";
		Reset_Color: str = "\x1b[39m\x1b[49m";


		Bold: str = "\x1b[1m";
		Bold_OFF: str = "\x1b[24m";

		Dim: str = "\x1b[2m";
		Dim_OFF: str = "\x1b[22m";

		Underline: str = "\x1b[4m";
		Underline_OFF: str = "\x1b[24m";

		Blink: str = "\x1b[5m";
		Blink_OFF: str = "\x1b[25m";

		Reverse: str = "\x1b[7m";
		Reverse_OFF: str = "\x1b[27m";

		Hide: str = "\x1b[8m";
		Hide_OFF: str = "\x1b[28m";


	class Cursor:
		""" A class containing numerous ASCII Escape Sequences to aid with cursor movement. """
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
				Lines (int*): The amount of columns we want to go right.
			
			Returns:
				str: An ASCII escape sequence that makes the cursor go right `Columns` characters.
			"""
			return f"\x1b[{Columns}C";

		@staticmethod
		def Left(Columns: int) -> str:
			""" Move the cursor left `Columns` columns.

			Arguments:
				Lines (int*): The amount of columns we want to go left.
			
			Returns:
				str: An ASCII escape sequence that makes the cursor go left `Columns` characters.
			"""
			return f"\x1b[{Columns}D";


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