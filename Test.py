from TSN_Abstracter import *;
import time;

Log.Delete();
Config.Logging["File"] = True;
Log.Critical("Im the only log to be written bitches");
Config.Logging["File"] = False;

Log.Info(File.Tree("TSN_Abstracter"));
Log.Info(File.Tree("IDontFuckingExist"));

File.JSON_Write("JSON/Test.json", {"hi": "balls"});

Log.Warning("Doing LITERALLY nothing right now...");
time.sleep(2);
Log.Status_Update("[DONE]");

"""
Unix = 0;
while True:
    Log.Carriage(Time.Elapsed_String(Unix));
    Unix += 1;
"""

