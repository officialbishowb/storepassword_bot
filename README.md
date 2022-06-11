# Telegram Bot to store credentials


## Install
1.) Clone the repository

2.) Run `pip install -r requirements.txt`

3.) Setup the following `.env` variables:

- `TELEGRAM_BOT_TOKEN` - Your Telegram Bot Token
-  `MASTER_KEY` - A master key to create a password for encryption/decryption of passwords
-  `KEY_SALT` - Salt for the password
- `ADMIN_IDS` - A list of admin ids separated by commas

4.) Then run `python bot.py` to start the Bot

---
Author: [@officialbishowb](https://github.com/officialbishowb)