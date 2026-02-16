<p align="center">
	<img src="https://sirio-network.com/Root/projects/tsna_banner.png" alt="Adellian Banner">
	<h2 align="center">The pillar of The Sirio Network</h2>
</p>

<br>

**__TSN Abstracter__** *(also called* ***TSNA)*** is a monolithic Python Module containing commonly used functions to avoid rewriting them for every project.  
TSNA can be used to make fully featured [Terminal Applications](./TSN_Abstracter/TUI.py) or CLI Based tools with some ease. **It is however crucial to mention that TSNA lacks any formal documentation**, only **DocStrings** within the Python Files are the unique type of documentation available for TSNA.

<br>

TSN Abstracter is currently used to power numerous tools and applications built by The Sirio Network such as:
- [Tachibana](https://github.com/Ascellayn/TSN_Tachibana)
- [Adellian](https://github.com/Ascellayn/Adellian)
- [Kozeki](https://github.com/Ascellayn/TSN_Kozeki)
- [The Kosaka Discord Bot's Eco-System](https://github.com/stars/Ascellayn/lists/kosaka-eco-system)
- [Caerbannog](https://github.com/Ascellayn/Caerbannog)
- [TSN "Yae"](https://sirio-network.com/Projects/Yae/Browser)
- [TSN "Himeki"](https://himeki.sirio-network.com/)

<br>

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
	"Version": [1,0,0],
	"Version_Prefix": "",
	"Version_Suffix": "_dev",
	"TSNA": [6,0,0] # Minimum required TSNA Version for the Application to run
}
```
TSN Abstracter is obviously __developer oriented__, it is **your job to look at TSNA and find functions that are deemed useful** to you.

## Dependencies
- The "LZMA" Python Module (should be shipped with your OS's Libraries)
- **If you import the "Cryptography" TSNA Module"**:
	- python3-cryptography
- **If you import the "TUI" TSNA Module"**:
	- python3-curses

###### [TSN Abstracter (TSNA) © Ascellayn / The Sirio Network (2025-2026) - TSN License 2.1 - Base](https://github.com/Ascellayn/TSN_Abstracter/LICENSE.md)