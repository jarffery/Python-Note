# Windows terminal setting-up

Here is the setting json file:

```json

// To view the default settings, hold "alt" while clicking on the "Settings" button.
// For documentation on these settings, see: https://aka.ms/terminal-documentation

{
    "$schema": "https://aka.ms/terminal-profiles-schema",

    "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
    "requestedTheme": "dark",

    "profiles":
    {
        "defaults":
        {
            // Put settings here that you want to apply to all profiles
        },
        "list":
        [
            {
                // Make changes here to the powershell.exe profile
                "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
                "name": "Windows PowerShell",
				"fontFace": "JetBrains Mono",
				"fontSize": 10,
                "commandline": "powershell.exe",
				"colorScheme": "Neutron",
                "hidden": false,
				"useAcrylic": true,
				"acrylicOpacity": 0.75
            },
            {
                // Make changes here to the cmd.exe profile
                "guid": "{0caa0dad-35be-5f56-a8ff-afceeeaa6101}",
                "name": "cmd",
                "commandline": "cmd.exe",
                "hidden": false
            },
            {
                "guid": "{b453ae62-4e3d-5e58-b989-0a998ec441b8}",
                "hidden": false,
                "name": "Azure Cloud Shell",
                "source": "Windows.Terminal.Azure"
            }
        ]
    },

    // Add custom color schemes to this array
    "schemes": [
	{
      "name": "Neutron",
      "black": "#23252b",
      "red": "#b54036",
      "green": "#5ab977",
      "yellow": "#deb566",
      "blue": "#6a7c93",
      "purple": "#a4799d",
      "cyan": "#3f94a8",
      "white": "#e6e8ef",
      "brightBlack": "#23252b",
      "brightRed": "#b54036",
      "brightGreen": "#5ab977",
      "brightYellow": "#deb566",
      "brightBlue": "#6a7c93",
      "brightPurple": "#a4799d",
      "brightCyan": "#3f94a8",
      "brightWhite": "#ebedf2",
      "background": "#1c1e22",
      "foreground": "#e6e8ef"
	}
],

    // Add any keybinding overrides to this array.
    // To unbind a default keybinding, set the command to "unbound"
    "keybindings": []
}

```

you could refer to the guide [link](https://www.notion.so/terminal-dfd59254c9a24c18a73b02355133f4e2).

**remember to down the font**:  [JetBrains Mono](https://www.jetbrains.com/lp/mono/)

