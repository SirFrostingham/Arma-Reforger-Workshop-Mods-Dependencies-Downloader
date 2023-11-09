# Arma-Reforger-Workshop-Mods-Dependencies-Downloader
This simple project is designed to take the Arma Reforger workshop website and output the parent mod and any/all mod dependencies json to put in your server config.json.

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

![image](https://github.com/SirFrostingham/Arma-Reforger-Workshop-Mods-Dependencies-Downloader/assets/4725943/a27f0b47-0cc5-44f5-a819-2c197e5a4ee8)


Plug in the data to your server's config.json:

![image](https://github.com/SirFrostingham/Arma-Reforger-Workshop-Mods-Dependencies-Downloader/assets/4725943/5b22c62c-5085-432d-b799-5831fdc58715)


Enjoy.
