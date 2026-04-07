# YouTube Music Discord RPC
An efficient Discord Rich Presence script that will update with your music playing through the YouTube Music player. The script is designed to work efficiently, without taking too much memory or processing power.

## ✨ Features

Headless Version: Without any GUI interface. Completely runs from terminal.
Low System Resources: Uses less CPU/RAM because the updates are checked every few seconds.
Auto Track Change Detection: The track changes are detected through the YouTube Music playback history.
Progress Bar: Shows how much you've listened and the total duration of the track.
Shortened Podcast Names: Automatically shortens long podcast names from selected artists/podcasts to improve the appearance of your Discord profile.

## ⚠️ Important Information
> [!WARNING]
> - Podcast Mode - it failed on the same grounds since the operation had been done with YTMusicapi using browser.json; therefore, it is now inactive in certain code sections
> - Listen Button - it is nonfunctional, I am yet to figure out why, but that may take a while

Listen Button: You won't be able to use this button because of how Discord works with Rich Presence. To you, the button will look like nothing happens when clicked. But when someone sees your profile, they'll be able to click it and listen to the song through YouTube Music.
Tracking Delay: In order to save as much RAM as possible, there is a delay of up to ~2 to 15 seconds between the track change and Discord.
OAuth2.0 Browsing: You will need a browser.json file with OAuth2.0 tokens.


## 📋 Requirements
- Python 3.7+

- Discord Desktop App or Discord Web

- [pypresence](https://pypi.org/project/pypresence/) and [ytmusicapi](https://ytmusicapi.readthedocs.io/en/stable/) libraries

## 🚀 Setup & Installation
### 1. Install Dependencies
Open your terminal and run:
```
pip install pypresence
```
```
pip install ytmusicapi
```
### 2. Generate browser.json
For the script to "listen" to what you're listening to, you need to permit it through your browser:

Follow the [YTMusicAPI setup for browser.json](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html)

### 3. Discord Developer Application Creation

In order to connect the script with your Discord account, it will be necessary to create your Discord developer application:

Visit Discord Developer Portal.

Press “New Application” and give a name to it (e.g. YouTube Music).

Retrieve your Application ID under the “General Information” section (that’s where the script will look up).

Setting Up Application Icon:

Open Rich Presence -> Art Assets

Upload an image (YouTube Music icon)

Rename this file to “embedded_cover” (as per the requirements of the code).

Save changes.

### 3b. Configuring Your Python Script

Open Main_File_NoUI.py and locate the “configuration” part:

Look for client_id and insert your Application ID there.

>[!NOTE]
>Do not confuse it with "Bot Token"

### 3c. Allowing the Script Access (The Connection Step)

In order for the script to have the ability to edit your activities within Discord, you will need to grant access. This may be done by selecting the “Installation” tab from the menu on the left side, which appears below “Overview.” When required, make sure to select “User Installation” and deselect “Server Installation.” Under “Install Link,” ensure that the setting has been set to “Discord Provided Link.” Open a tab and enter the link to allow the app access.

### 4. execute the Code
Execute the code using browser.json file, Discord ID, and Discord image name
> [!IMPORTANT]
> For some reason, it only works when executed in debug mode in VSCode, trying to fix this issue, but for now, you can execute using debug mode

# 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
