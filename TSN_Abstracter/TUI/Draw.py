""" Generic Drawing Functions such as the Window Frame. """

from .Globals import *;



__all__: list[str] = [
	"Base",
	"Base_Box"
];





def Base(Clear: bool = True) -> None:
	""" Draw the Window Frame with the TSNA App's Name
	
	Arguments:
		Clear (bool = True): Whenever to clear completely the Window before drawing the frame.
	"""
	curses.update_lines_cols();
	if (curses.LINES < 6): Exit(); Log.Critical("Terminal size is way too small! TSN Abstracter's TUI Menu requires a terminal that's at the very least 6 lines long."); exit(78);
	if (Clear): Window.clear();
	Window.border();

	Title: str = String.Abbreviate(f" {App.Name} - {TSN_Abstracter.App_Version()} ", curses.COLS - 4);
	Window.addstr(0, 2, Title, curses.A_BOLD);


def Base_Box(Offset: int = 0) -> None:
	""" Draw a straight line to be used primarily for the description box when hovering elements in `TUI.Menu`.  
	Draws from the bottom, by default with only a size of 1 line.  
	**Requires manual execution of `TUI.Base()`.**  
	
	Arguments:
		offset (int = 0): How many more additional lines the "box" should be.
	
	"""
	Window.hline(curses.LINES - 3 - Offset, 1, curses.ACS_HLINE, curses.COLS -2);