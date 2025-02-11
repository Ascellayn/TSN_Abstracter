from TSN_Abstracter import *;
import time;

Log.Clear();

Config.Logging["File"] = True;
Log.Critical("Im the only log to be written bitches");
Config.Logging["File"] = False;

Log.Info(File.Tree("TSN_Abstracter"));
Log.Info(File.Tree("IDontFuckingExist"));

File.JSON_Write("JSON/Test.json", {"hi": "balls"})

"""
Unix = 0;
while True:
    Log.Carriage(Time.Elapsed_String(Unix));
    Unix += 1;
"""

