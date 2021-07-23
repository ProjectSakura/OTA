# Auto OTA poster
## Overview 
A code written in Python that is meant to be run using Github Actions on push which posts an update on our telegram channel whenever there is an OTA update.
## Requirements
* [Python 3.X](https://www.python.org/)
* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)

## Running the code

Code is meant to be inside of a folder named ```post-bot``` in the ```OTA``` repository. To run it, set environment variable ```BOT_API``` to your API Token and ```CHAT``` to chat ID, then run the code below : 
```shell
python3 post-bot/post.py
```