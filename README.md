# TSN Abstracter (TSNA)
Python Module used across all newer Python Projects containing a bunch of commonly used functions.  

TSNA aims to facilitate development of numerous TSN Python projects such as the [Kosaka Eco-System](https://github.com/stars/Ascellayn/lists/kosaka-related-repositories), [TSN "Trinity"](https://github.com/Ascellayn/TSN_Trinity), [Caerbannog](https://github.com/Ascellayn/Caerbannog) and MANY other projects aimed to serve The Sirio Network.  

## Installation / Usage
TSNA does not come with a proper pip Python Package, you must MANUALLY install TSNA on your computer by downloading the whole repository and unzipping it somewhere.  
In the case of Linux, with an installation at `/System/Library/TSN_Abstracter`, you must add to your `.bashrc` the following line: `export PYTHONPATH=/System/Library/TSN_Abstracter:$`.  
All that's left to do is simply include at the very top of your Python script `from TSN_Abstracter import *;` and then get to roll with it.  
We recommend the following template file to start your TSNA fueled programs:
```python
# [Program] (c) [Author] (Date) - [License]
from TSN_Abstracter import *;

Root_CFG: dict = File.JSON_Read("Root_CFG.json");
Debug_Mode: bool = Root_CFG["Debug"];

if (__name__ == '__main__'):
	Log.Clear(); TSN_Abstracter.Require_Version((3,1,0)); # Change (3.1.0) to which ever minimal TSNA version you want to target.
	Config.Logger.Print_Level = 15 if (Debug_Mode) else 20;
	Config.Logger.File = True;
	
	Log.Stateless(f"[Program Name] {Root_CFG["Version"]}");
	# Do whatever your program does here
```
TSN Abstracter is obviously __developer oriented__, it is **your job to look at TSNA and find functions that are deemed useful** to you.

## Dependencies
- python3-cryptography
- The "LZMA" Python Module (should be shipped with your OS's Libraries)

###### [TSN Abstracter (TSNA) © Ascellayn (2025) - TSN License 1.0 - Base](https://github.com/Ascellayn/TSN_Abstracter/LICENSE.md)