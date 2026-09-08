- # TSN Abstracter now follows [The Sirio Network's Code Style](https://sirio-network.com/guideline/code_style)
	- ## __This COMPLETELY BREAKS ***EVERY SINGLE TSNA BASED*** PROGRAM to date.__
	### We do not recommend updating to v7 unless you're ready to refactor all of your projects based off TSNA.



<br>



- ## Serina Heartbeat Module
	- (TBD)



- ## Crypto Module Rework
	- After years of the `Cryptography` module being deprecated, it finally has been reworked.
	- (TBD)



- ### `TSNA` Changes
	- `TSN_Abstracter.*` is now `TSNA.*`
	- Added `NotRequired` to global imports
	- `TSNA.require()` no longer by default closes the program immediately if the TSNA version is incompatible, instead it warns the user that the program is incompatible and that the program may be broken but they may proceed.
	- Moved `TSNA.App_Info()` to `App.info()`
	- Moved `TSNA.App_Version()` to `App.version()`
	- Removed `NULL`
	- Removed `TypeAlias` from global imports
	- Renamed attribute `TSNA.Version_Tuple` → `TSNA.VERSION`
	- Renamed and made private class `TSNA.Bad_Version` → `TSNA.__VersionBad`
	- Renamed and made private class `TSNA.Outdated_Version` → `TSNA.__Outdated`
	- Renamed and made private class `TSNA.Breaking_Version` → `TSNA.__Breaking`
	- Renamed method `TSNA.Version()` → `TSNA.version()`
	- Renamed method `TSNA.Require_Version()` → `TSNA.require()`
	- Renamed method `TSNA.Version()` → `TSNA.version()`
	- Renamed method `TSNA.Import_Unsupported()` → `TSNA.denyImport()`
	- Renamed method `TSNA.App_Init()` → `TSNA.init()`




- ### `App` Changes
	- Added `Serina` Key (see Serina Heartbeat Module section for more information)
	- Added `App.version()`, replacing `TSN_Abstracter.App_Version()`
	- Removed `Private` Key
	- Renamed Key `License_Year` → `Year`
	- Renamed Key `Public` → `Data`
	- Renamed function `App.Dump()` → `App.info()`
	- Renamed function `App.Reload()` → `App.reload()`
	- Renamed function `App.JSON()` → `App.load()`



- ### `File` Changes
	- `CSV` support. (TBD)



- #### Miscellaneous Changes
	- Added `App.tsna.template` example for configuring TSNA Based programs