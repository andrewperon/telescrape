# telescrape

A python tool to scrape Telegram users from supergroups. Supports persistent sessions and 2FA login.

Requires **telethon** ([https://github.com/LonamiWebs/Telethon](https://github.com/LonamiWebs/Telethon)) for interfacing with Telegram APIs and **python-slugify**. This tool allows you to scrape username, userid, groupid, and more from supergroups to CSV for further analysis and use.

Requires Telegram API as user (not @botfather) - you can generate your keys here:  [https://my.telegram.org/auth](https://my.telegram.org/auth)

# requirements

Install **telethon** and **python-slugify**:

    pip install telethon python-slugify

Make sure you have Telegram API credentials - [https://my.telegram.org/auth](https://my.telegram.org/auth)

# config

Once you have your credentials, insert your values in *credentials.py*:
![enter image description here](https://i.imgur.com/hW8FEyB.png)

These values are loaded into the main script - because telethon is sessioned, you can use & store login credentials for multiple accounts based on folder structure without needing to modify the script.

# usage

Run the script. On first run, you will be prompted to enter an SMS or 2FA one-time password (OTP):

    > python groupscrape.py 

    Enter OTP code:

Upon successful login, you will be shown a list of supergroups your user is a member of. Choose a group to scrape members for. All members will be saved to a CSV file, inside of a csv subfolder in the directory where the script was launched. Naming follows the following format:

    groupname_YYYYMMDD-hhmmss.csv

This should allow for comparison over time.

More functionality to come.
