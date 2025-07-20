def Split_Length(Text: str, Max_Length: int) -> list[str]:
	"""
	Splits a string after a new line (unless there are no line breaks, in that case it will stop after a space, otherwises raw cuts through words if neither lines breaks nor spaces are present) into an array according to Max_Length.

	Arguments:
		String: The string we want to split.
		Max_Length: The maximum size of each string element.
	Returns:
		A list containing strings.
	"""
	def Raw_Split() -> None: String_List.append(Text[:Max_Length]);
	def Line_Split(PString) -> int:
		End: int = len(PString) - PString.index("\n")
		String_List.append(Text[:End]);
		return End;
	def Space_Split(PString) -> int:
		End: int = len(PString) - PString.index(" ")
		String_List.append(Text[:End]);
		return End;
	
	String_List: list[str] = [];
	while (Text != ""):
		String_Current = Text[:Max_Length][::-1];
		if (len(String_Current) != len(Text)):
			if ("\n" in String_Current): Text = Text[Line_Split(String_Current):]; continue;
			if (" " in String_Current): Text = Text[Space_Split(String_Current):]; continue;
		Raw_Split(); Text = Text[Max_Length:]
	return String_List;