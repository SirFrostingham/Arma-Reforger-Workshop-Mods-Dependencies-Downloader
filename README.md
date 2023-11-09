# Arma-Reforger-Workshop-Mods-Dependencies-Downloader
This simple project is designed to take the Arma Reforger workshop website and output the parent mod and any/all mod dependencies json to put in your server config.json.

Instructions:
1. Download/copy the modsDownloader.ps1 script to any directory.
2. Run it like this:
    ```. '.\modsDownloader.ps1' -url "https://reforger.armaplatform.com/workshop/5CAB24EF8A549922-ReforgedWastelandPrototype"```

Result:
It will output the main mod + all dependencies, so you can plug it into your server's mods object.

Tool output screenshot:
![image](https://github.com/SirFrostingham/Arma-Reforger-Workshop-Mods-Dependencies-Downloader/assets/4725943/128c6999-4b21-48f4-8613-353f811f4cdf)

Where you plug in the data to your server's config.json:
![image](https://github.com/SirFrostingham/Arma-Reforger-Workshop-Mods-Dependencies-Downloader/assets/4725943/b09718a9-18b9-4fe6-916e-ab417d9e2686)

Enjoy.
