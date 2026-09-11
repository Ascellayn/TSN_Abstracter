- # TSN Abstracter now follows [The Sirio Network's Code Style](https://sirio-network.com/guideline/code_style)
	- ## __This COMPLETELY BREAKS ***EVERY SINGLE TSNA BASED*** PROGRAM to date.__
	### We do not recommend updating to v7 unless you're ready to refactor all of your projects based off TSNA.



<br>



- ## General Changes
	- Every single function/method/module now starts with the string specifying which version of TSNA it was implemented.  
	This will hopefully help developers know which version of TSNA is the bare minimum for them to support.  
	Since everything was refactored and renamed, everything is specified as being implemented in TSNA `v7.0.0`.



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



- ### `Deco` Changes
	- `Deco.Progresser`'s `DELAY` argument is now a keyword argument
	- Renamed attribute `Deco.Progresser.Size` → `Deco.Progresser.SIZE`
	- Renamed method `Deco.Progresser.__Text` → `Deco.Progresser.__text`
	- Renamed method `Deco.Progresser.count` → `Deco.Progresser.count`



- ### `File` Changes
	- `CSV` support. (TBD)
	- `DIRECTORY` is now far more accurate as TSNA now sets it to the location of `App.tsna` if it can be found.
	- Optimized `File.Path.folder()` by using the modern ancient technology of learning that `os.dirname()` exists.
	- The `Append` argument no longer exists for `File.write()`, it instead was sent to be on its own function to reduce unnecessary operations on a barely used feature. This also helps improve code readability by not having confusing `write()` calls everywhere that in the end appends data.
	- Improved the `Folder_*` types by adding `Folder_Name`, `File_Name` TypeAliases to improve readability.
	- Deleted `Folder_Tree` and modified `Folder_Matrix` to make better sense.
		- Reworked `File.tree()` as a consequence, the code is also SIGNIFICANTLY more readable.
	- Rewrote core `read()` `write()` functions to be faster (TBD)
	- Renamed Constant `Main_Directory` → `DIRECTORY`
	- Renamed function `File.Exists()` → `File.exists()`
	- Renamed function `File.List()` → `File.ls()`
	- Renamed function `File.Tree()` → `File.tree()`
	- Renamed function `File.Read()` → `File.read()`
	- Renamed function `File.Write()` → `File.write()`
	- Renamed function `File.Read_JSON()` → `File.readJSON()`
	- Renamed function `File.Write_JSON()` → `File.writeJSON()`
	- Renamed function `File.Update_JSON()` → `File.appendJSON()`
	- Renamed function `File.Read_Array()` → `File.readArray()`
	- Renamed function `File.Write_Array()` → `File.writeArray()`
	- Renamed function `File.Update_Array()` → `File.appendArray()`
	- Renamed function `File.Path_Create()` → `File.Path.create()`
	- Renamed function `File.Path_Require()` → `File.Path.require()`
	- Renamed function `File.Path_Folder()` → `File.Path.folder()`



- ### `Log` Changes
	- (TBD)



- ### `Misc` Changes
	- The `Misc` module has entirely been "removed", its functions have been moved to other modules such as `Multi` and `Number`.
	- Removed `Misc.is_Even()` to promote more performant practice (due to not calling a function for `X % 2`)



- ### "New" `Multi` Module
	- `newThread` and `newProcess` now return their appropriate objects.
	- Resolved typing issues for `newThread` and `newProcess`
	- Renamed function `Misc.Thread_Start()` → `Multi.newThread()`
	- Renamed function `Misc.Process_Start()` → `Multi.newProcess()`


- ### "New" `Number` Module
	- Renamed and moved function `Misc.Under_At()` → `Number.underAt()`



- ### `Safe` Changes
	- Renamed function `Safe.Index()` → `Safe.array()`
	- Renamed function `Safe.Nested_Dict()` → `Safe.dictionary()`
	- Renamed function `Safe.NotNull()` → `Safe.nonZero()`



- ### `String` Changes
	- Renamed function `String.ify_Array()` → `String.ifyArray()`
	- Renamed function `String.Bulk_Replace()` → `String.bulkReplace()`
	- Renamed function `String.Trailing_Zero()` → `String.trailingZero()`
	- Renamed function `String.Split_Length()` → `String.lengthSplit()`
	- Renamed function `String.Abbreviate()` → `String.abbreviate()`
	- Moved and renamed function `String.Clear_ASCII_Formatting()` → `String.ASCII.clearFormatting()`



- ### `Time` Changes
	- `Time.dateStrings()` has been optimized and no longer duplicates objects.
	- `Time.dateStrings()` now has an extra option to use `DD/MM/YYYY` instead of `YYYY/MM/DD` by setting its new `REVERSED` argument to `False` (reversed format stays the default).
	- Fixed a bug where the value for the length of a day inside of `Time.Unix.*` was the same as an hour and the amount of seconds inside of a minute was the one of an hour
	- TSNA now considers a year to be as long as a **tropical year**
		- This equals roughly to 365 days, 5 hours, 48 minutes and 45 seconds.
	- TSNA now considers a month to be as long as a **tropical year divided by 12**
		- This equals roughly to 30 days, 10 hours, 29 minutes, 3 seconds and 750 milliseconds and 192 microseconds.
	- `Time.Elapsed.dict()` has been made slower in order to make the code significantly more readable and accurate.
	- `Time.Elapsed.dict()` now uses the defined values in `Unix.[UNIT]` whenever applicable.
	- `Time.Unix.fromString()` now uses the defined values in `Unix.[UNIT]` whenever applicable.
	- `Time.Unix.fromString()` now correctly uses the `unix_t` return data type.
	- You can now acquire directly a datetime object of the current time (similar to `Time.Unix.now()`) with `Time.Datetime.now()`.
	- Created new `Unit` class to regroup constants under `Unit_*`
	- Created new `Elapsed` class to regroup all functions related to time passing.
	- Renamed function `Time.Get_Unix()` → `Time.Unix.now()`
	- Renamed function `Time.Get_Dawn()` → `Time.Unix.dawn()`
	- Renamed function `Time.Convert_Unix()` → `Time.Unix.toDatetime()`
	- Renamed function `Time.Convert_Datetime()` → `Time.Datetime.toUnix()`
	- Renamed function `Time.Convert_ISO8601()` → `Time.Datetime.fromISO8601()`
	- Renamed function `Time.Get_DateStrings()` → `Time.dateStrings()`
	- Renamed function `Time.Elapsed_Time()` → `Time.Elapsed.dict()`
	- Renamed function `Time.Elapsed_String()` → `Time.Elapsed.string()`
	- Renamed function `Time.String_Time()` → `Time.Unix.fromString()`
	- Renamed constant `Time.Unit_Short` → `Time.Unit.SHORT`
	- Renamed constant `Time.Unit_Power` → `Time.Unit.POWER`
	- Renamed class `Time.Time_Dict()` → `Time.Dict()`
	- Moved and Renamed function `Time.Unit_Edges()` → `Time.Unit.edges()`



- ### `TSNDL` Changes
	- Added `TSNDL.Hex.fromTuple()` which converts a list of decimal numbers into their hex counterpart.
	- Added `TSNDL.decimalConversion()` which converts any decimal number to by default hexadecimal. Configurable to use any base to convert to, along with a base alphabet that is also configurable.
	- `TSNDL.Hex.toDecimal()` now converts the WHOLE string instead of just the first character.
	- Renamed function `TSNDL.Hex_Tuple()` → `TSNDL.Hex.toTuple()`
	- Renamed function `TSNDL.Hex_To_Decimal()` → `TSNDL.Hex.toDecimal()`
	- Renamed function `TSNDL.ASCII_Color()` → `TSNDL.Hex.toASCII()`
	- Renamed function `TSNDL.Log_Color()` → `TSNDL.Color.log()`



- ### `TUI` Changes
	- (TBD)



- #### Miscellaneous Changes
	- Added `App.tsna.template` example for configuring TSNA Based programs