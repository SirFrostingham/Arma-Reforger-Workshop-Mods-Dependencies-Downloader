# Arma-Reforger-Workshop-Mods-Dependencies-Downloader
This simple project is designed to take the Arma Reforger workshop website and output the `parent mod and any/all mod dependencies` as json that the game can use.

**2 flavors**
1. Powershell
2. Python

# Powershell Instructions
1. Prerequisite - Install WebRequest module via CMD: `powershell -command "Install-Module WebRequest" -Scope CurrentUser -AllowClobber`
2. Download/copy the `modsDownloader.ps1` script to any directory.
3. Run: cmd
4. Run: powershell
5. **Script usages**:
   - Exclude mod version detail:
        `. '.\modsDownloader.ps1' -url "https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes"`
   - Include mod version detail:
        `. '.\modsDownloader.ps1' -url "https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes" -version true`
   - Output only mods array:
        `. '.\modsDownloader.ps1' -onlyMods -url "https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes"`
   - Output to text file (be sure to delete any previous, since this will append):
        `. '.\modsDownloader.ps1' -url "https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes" -version true >> test.json`

# Python Instructions
1. Prerequisite: Install python: If in Windows, suggest install chocolatey (https://chocolatey.org/install -> run powershell script under "Now run the following command"), then install python (choco install python3).
2. Download/copy the `modsDownloader.py` script to any directory.
3. **Script usages**:
    - Exclude mod version detail:
       `python .\modsDownloader.py https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes`
    - Include mod verison detail:
       `python .\modsDownloader.py https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes --version`
    - Output only mods array:
       `python .\modsDownloader.py https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes --onlyMods`
    - Include mod verison detail (be sure to delete any previous, since this will append):
       `python .\modsDownloader.py https://reforger.armaplatform.com/workshop/5EE637B626221E3F-Conflict2032Utes --version >> test.json`

# Results
Either script will output the content from the website url (main mod + all mod dependencies, Scenario ID, and player count as maxPlayers) to a json format the game can use.

Tool example screenshot (see Powershell or Python usages above - both scripts output the same exact way):

![image](https://github.com/SirFrostingham/Arma-Reforger-Workshop-Mods-Dependencies-Downloader/assets/4725943/ff8c9b57-8fd2-48cf-aa13-056d97edfd44)

That's it! Plug this json into your Arma Reforger server and it will work.

If you output the file with `>> test.json` (see usages above), it can be used like this:

`start "ArmaReforger" /wait /high "ArmaReforgerServer.exe" -maxFPS 60 -config ".\test.json" -profile test`

# Troubleshooting
- If your server starts and is listed in-game with 999+ ping...
  - In your game server's `config.json`, or as shown above `test.json`, change `publicAddress` value to your public IP address.

Enjoy!
