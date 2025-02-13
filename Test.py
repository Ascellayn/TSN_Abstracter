from TSN_Abstracter import *;
import time;

Log.Delete();

Log.Info(File.Tree("TSN_Abstracter"));
Log.Info(File.Tree("IDontFuckingExist"));

Config.Logging["File"] = True;
Log.Critical("Im the only log to be written bitches, for now");

File.JSON_Write("JSON/Test.json", {"hi": "balls"});

Log.Info("Hey, I'm waiting for status shit here...");
Log.Critical("im gonna fucc shi up now")
Log.OK();

Log.Warning("Doing LITERALLY nothing right now...");
time.sleep(1);
Log.Status_Update("[DONE]");

Config.Logging["File"] = False;

"""
Unix = 0;
while True:
    Log.Carriage(Time.Elapsed_String(Unix));
    Unix += 1;
"""

