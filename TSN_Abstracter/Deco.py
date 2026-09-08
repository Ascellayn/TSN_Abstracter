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
	""" Automatic carriage-based progression display, if you have a task that has a set amount of operations to do this will be useful to show the progression of it.

	Arguments:
		Size (int*): The amount of total tasks to complete.
		Template (str = "Progression: {Done}/{Size} - ({Operations} OP/s) | ETA: {ETA}"): The format of the progression text.
		Delay: (int | float): The __*minimum*__ delay before the progresser has a chance to display its text.

	## Methods:
		Count() → Increment the Progresser, automatically displays the text whenever applicable.

	### PLACEHOLDERS:
		`Progresser()` supports placeholders in the `Template` variable to slightly customize the look of the progression text.
		- `{Done}` → How many tasks have been completed.
		- `{Size}` → How many tasks there is to complete in total.
		- `{Operations}` → The amount of completed tasks done every second.
		- `{ETA}` → An estimation of when all tasks will be finished.
	"""
	def __init__(self,
		SIZE: int, TEMPLATE: str = "Progression: {Done}/{Size} - ({Operations} OP/s) | ETA: {ETA}",
			*,
		DELAY: int | float = 1
	) -> None:
		self.SIZE: int = SIZE;
		self.Delay: int | float = DELAY;
		self.Template = TEMPLATE;

		self.Done: int = 0;
		self.Done_Cycle: int = 0;
		self.Cycles: list[int] = [];

		self.__Precise: bool = True if (type(DELAY) == float) else False;
		self._Unix_Last = Time.Get_Unix(self.__Precise);





	def __text(self) -> str:
		""" Retrieve the text to print out """
		ops: float = round(
			(
				sum(self.Cycles)
				/
				Safe.NotNull(len(self.Cycles))
			)
			/
			Safe.NotNull(self.Delay)
			, 2
		);

		eta: str = Time.Elapsed_String(
			round(
				self.SIZE / ops
			),
		);

		return self.Template\
.replace("{Done}", str(self.Done))\
.replace("{Size}", str(self.SIZE))\
.replace("{Operations}", str(ops))\
.replace("{ETA}", str(eta));



	def count(self, Increment: int = 1) -> None:
		""" Increment the progression counter. Automatically displays progress whenever applicable.

		Arguments:
			Increment (int = 1): The amount of tasks to add as complete.
		"""
		self.Done += Increment; self.Done_Cycle += Increment;
		if ((self._Unix_Last + self.Delay) > Time.Get_Unix(self.__Precise)): return;


		self.Cycles.append(self.Done_Cycle);
		self.Done_Cycle = 0;
		self._Unix_Last = Time.Get_Unix(self.__Precise);


		Log.Carriage(self.__text());