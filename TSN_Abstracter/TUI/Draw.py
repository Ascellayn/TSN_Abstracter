""" ***Implemented in __TSNA `v7.0.0`__***  

Generic Drawing Functions such as the Window Frame.
"""

from .Globals import *;








def frame(CLEAR: bool = True) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Draw the Window Frame with the TSNA App's Name
	
	Arguments:
		CLEAR (bool = True): Whenever to clear completely the Window before drawing the frame.
	"""
	curses.update_lines_cols();
	if (curses.LINES < 6): exit(); Log.crit("Terminal size is way too small! TSN Abstracter's TUI Menu requires a terminal that's at the very least 6 lines long."); exit(78);
	if (CLEAR): Window.clear();
	Window.border();
	
	Window.addstr(0, 2, String.abbreviate(f" {App.Name} - {App.version()} ", curses.COLS - 4), curses.A_BOLD);



def frameLine(OFFSET: int = 0) -> None:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Draw a straight line to be used primarily for the description box when hovering elements in `TUI.Menu`.  
	Draws from the bottom, by default with only a size of 1 line.  
	**Requires manual execution of `TUI.frame()`.**  
	
	Arguments:
		OFFSET (int = 0): How many more additional lines the "box" should be.
	
	"""
	Window.hline(curses.LINES - 3 - OFFSET, 1, curses.ACS_HLINE, curses.COLS -2);










__all__: list[str] = [
	"frame",
	"frameLine"
];