# TSN Abstracter (TSNA)
Python Module used across all newer "built-for-TSN" Python Projects containing a bunch of commonly used functions.  

TSNA aims to facilitate development of numerous TSN Python projects such as the [Kosaka Eco-System](https://github.com/stars/Ascellayn/lists/kosaka-related-repositories), [TSN "Trinity"](https://github.com/Ascellayn/TSN_Trinity), [Caerbannog](https://github.com/Ascellayn/Caerbannog) and MANY other projects aimed to serve The Sirio Network.  

## Installation / Usage
TSNA does not come with a proper pip Python Package, you must MANUALLY install TSNA on your computer by downloading the whole repository and unzipping it somewhere.  
In the case of Linux, with an installation at `/System/Library/TSN_Abstracter`, you must add to your `.bashrc` the following line: `export PYTHONPATH=/System/Library/TSN_Abstracter:$`.  
All that's left to do is simply include at the very top of your Python script `from TSN_Abstracter import *;` and then get to roll with it.  
We recommend the following template file Python File to start your TSNA fueled programs:
```python
# [Program] (c) [Author] (Date) - [License]
from TSN_Abstracter import *;

Debug_Mode: bool = Root_CFG["Debug"];

if (__name__ != "__main__"): TSN_Abstracter.Import_Unsupported(); # Remove this if your script can be imported as a Python Module
else:
	TSN_Abstracter.App_Init(True);
	Config.Logger.Print_Level = 15 if (Debug_Mode) else 20;
	Config.Logger.File = True;

	# Do whatever your program does here
	...
```
TSNA automatically attempts to read data from `App.tsna`, this file contains basic information about your application:
```json
{
	"Name": "Tachibana",
	"Description": "Tachibana is a (work in progress) TSNA-Based rewrite of Adellian's SSHMan Application.",
	"Author": ["Ascellayn", "The Sirio Network"],
	"Contributors": [],
	"License": "TSN License 2.1 - Base",
	"License_Year": "2026",
	"Codename": "TSN_Tachibana",
	"Branch": "Azure",
	"Version": "v0_dev",
	"TSNA": [5,6,0] # Minimum required TSNA Version for the Application to run
}
```
TSN Abstracter is obviously __developer oriented__, it is **your job to look at TSNA and find functions that are deemed useful** to you.

## Dependencies
- python3-cryptography
- The "LZMA" Python Module (should be shipped with your OS's Libraries)

###### [TSN Abstracter (TSNA) © Ascellayn / The Sirio Network (2025-2026) - TSN License 2.1 - Base](https://github.com/Ascellayn/TSN_Abstracter/LICENSE.md)