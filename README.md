# Arma-Reforger-Workshop-Mods-Dependencies-Downloader
This simple project is designed to take the Arma Reforger workshop website and output the `parent mod and any/all mod dependencies` json to put in your server config.json. It also outputs the mod's `scenario id` at the bottom.

2 flavors:
1. Powershell
2. Python

Powershell Instructions:
1. Prerequisite - Install WebRequest module via CMD: `powershell -command "Install-Module WebRequest" -Scope CurrentUser -AllowClobber`
2. Download/copy the `modsDownloader.ps1` script to any directory.
3. Run it like this:
    `. '.\modsDownloader.ps1' -url "https://reforger.armaplatform.com/workshop/5CAB24EF8A549922-ReforgedWastelandPrototype"`

Python Instructions:
1. Prerequisite: Install python: If in Windows, suggest install chocolatey (https://chocolatey.org/install -> run powershell script under "Now run the following command"), then install python (choco install python3).
2. Download/copy the `modsDownloader.py` script to any directory.
3. Run it like this:
   `python .\modsDownloader.py https://reforger.armaplatform.com/workshop/5CAB24EF8A549922-ReforgedWastelandPrototype`

Result:
It will output the main mod + all dependencies, so you can plug it into your server's mods object.

Tool output screenshot (both script outputs are exactly the same):

![image](https://github.com/SirFrostingham/Arma-Reforger-Workshop-Mods-Dependencies-Downloader/assets/4725943/0c3157de-1a75-496c-8a47-53cbe134b2f6)


Plug in the data to your server's config.json:

![image](https://github.com/SirFrostingham/Arma-Reforger-Workshop-Mods-Dependencies-Downloader/assets/4725943/5b22c62c-5085-432d-b799-5831fdc58715)


Troubleshooting:
If you add the json and the server does not start, look for errors:
```
INIT         : Creating game instance(ArmaReforgerScripted), version 0.9.9.104 built 2023-09-22 2:16:53 UTC.
Loading dedicated server config.
 BACKEND      : Server config loaded.
 BACKEND      : JSON Schema Validation:
  BACKEND      : JSON is Valid
 RESOURCES    : GetResourceObject @"{9F7BA3BBF4B38A98}Missions/WastelandHeader.conf"
  RESOURCES (E): Failed to open
 RESOURCES (E): MissionHeader::ReadMissionHeader cannot load the resource 'Missions/WastelandHeader.conf'!
ENGINE       : Game successfully created.
InputManager user settings load from profile @"InputUserSettings.conf"
 DEFAULT   (W): Loading input settings from legacy file, which will be soon unsupported
NETWORK      : Starting dedicated server using command line args.
BACKEND   (E): Http Error apiCode="ResourceNotFoundError", message="Asset '5AF76BA0142BCDDE' not found"
```

At the time of writing this, the mod `5AF76BA0142BCDDE` (Vergys Military Gear) returns a 404 ResourceNotFoundError, which means a dependency of the "ReforgedWastelandPrototype" workshop item is missing.

Enjoy.
