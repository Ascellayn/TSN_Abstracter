""" This module from TSN Abstracter is in charge of providing Python Decorators, mostly to time the execution of functions or doing light processing.

### Examples
>>> from TSN_Abstracter import Deco;
>>> X = [...]
>>> P = Deco.Progresser(len(X));
>>> for y in X:
>>>	...
>>>	P.Count();

"""
from . import Time;
from . import Log;
from . import Safe;



class Progresser():
	""" Automatic carriage-based progression display"""
	def __init__(self, Size: int, Template: str = "Progression: {Done}/{Size} - ({Operations} OP/s) | ETA: {ETA}", Delay: int | float = 1) -> None:
		self.Size: int = Size;
		self.Delay: int | float = Delay;
		self.Template = Template;

		self.Done: int = 0;
		self.Done_Cycle: int = 0;
		self.Cycles: list[int] = [];

		self.__Precise: bool = True if (type(Delay) == float) else False;
		self._Unix_Last = Time.Get_Unix(self.__Precise);


	def __Text(self) -> str:
		""" Retrieve the text to print out """
		OPs: float = round(
			(
				sum(self.Cycles)
				/
				Safe.NotNull(len(self.Cycles))
			)
			/
			Safe.NotNull(self.Delay)
			, 2
		);

		ETA: str = Time.Elapsed_String(
			round(
				self.Size / OPs
			),
		)

		return self.Template\
.replace("{Done}", str(self.Done))\
.replace("{Size}", str(self.Size))\
.replace("{Operations}", str(OPs))\
.replace("{ETA}", str(ETA))


	def Count(self) -> None:
		""" Increment the progression counter. Automatically displays progress when the update rate for it is reached. """
		self.Done += 1; self.Done_Cycle += 1;
		if ((self._Unix_Last + self.Delay) < Time.Get_Unix(self.__Precise)): return;

		self.Cycles.append(self.Done_Cycle);
		self.Done_Cycle = 0;
		self._Unix_Last = Time.Get_Unix(self.__Precise);

		Log.Carriage(self.__Text());