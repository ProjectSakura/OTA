#!/usr/bin/env python
#
# Python code which automatically sends a Message in a Telegram Group if any new update is found.
# Intended to be run on every push
# USAGE : python post.py <Telegram API Key> <Chat ID>
# Copyright (C) 2021 Ashwin DS <astroashwin@outlook.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import sys
import datetime
import json
import os
import time
import telebot

# Get secrets from Workflow
BOT_API = sys.argv[2]
CHAT_ID = sys.argv[1]

# Init the bot
bot = telebot.TeleBot(BOT_API, parse_mode="HTML")

# Where to look for .json files
fileDir = "."
fileExt = ".json"


def send_mes(message):
    return bot.send_message(chat_id=CHAT_ID, text=message, disable_web_page_preview=True)


def send_photo(image, caption):
    if not caption or caption == "" or caption is None:
        return bot.send_photo(chat_id=CHAT_ID, photo=open(image, "rb"))
    else:
        return bot.send_photo(chat_id=CHAT_ID, photo=open(image, "rb"), caption=caption)


# store MD5s in a file to compare
def update(IDs):
    with open("post-bot/log.txt", "w+") as f:
        for s in IDs:
            f.write(str(s) + "\n")


# Return IDs of all latest files from *.json files
def get_id():
    result = []
    for a in os.listdir(fileDir):
        if a.endswith(fileExt):
            if a != "devices.json":
                result.append(a)

    file_id = []
    for a in result:
        file = open(a, "r")
        json_processed = json.loads(file.read())
        file_id.append(json_processed['response'][0]['id'])
    return file_id


# Return previous IDs
def read_old():
    old_id = []
    file = open("post-bot/log.txt", "r")
    for line in file.readlines():
        old_id.append(line.replace("\n", ""))
    return old_id


# remove elements in 2nd list from 1st, helps to find out what device got an update
def get_diff(new_id, old_id):
    first_set = set(new_id)
    sec_set = set(old_id)
    return list(first_set - sec_set)


# Grab needed info using id of the file
def get_info(id):
    devices = []
    for a in os.listdir(fileDir):
        if a.endswith(fileExt):
            if a != "devices.json":
                devices.append(a)
    for a in devices:
        file = open(a, "r")
        json_processed = json.loads(file.read())
        if json_processed['response'][0]['id'] == id:
            print(json_processed['response'][0])
            required = json_processed['response'][0]
            device = a.replace(".json", "")
            break
    file = open("devices.json", "r")
    json_processed = json.loads(file.read())
    for devices in json_processed:
        if devices['codename'] == device:
            maintainer = devices['maintainer_name']
            name = devices['name']
            brand = devices['brand']

    if "VANILLA" in required['filename']:
        variant = "Vanilla"
    else:
        variant = "GApps"

    print("Device is : " + device)
    print("Size is : " + str(required['size']))
    print("Maintained by : " + maintainer)
    print("File name : " + required['filename'])
    print("Version : " + required['version'])
    print("Variant : " + variant)

    return {
        "device": device,
        "size": str((int(required['size'])/1000000).__trunc__()),
        "maintainer": maintainer,
        "variant": variant,
        "version" : required['version'],
        'name' : name,
        "brand" : brand
    }


def space(text1, text2):
    message = "<b>" + text1 + "</b>" + text2
    return message


# Prepare in the format needed
def cook_content(information):
    message = ""
    # links need to be in this format <a href="http://www.example.com/">inline URL</a>
    message = message + \
        "<b>New Update for " + information['name'] +  " (" + str(information['device'] ) + ") is here!</b>\n" + \
        "👤 " + space("by ", str(information["maintainer"]) ) + "\n\n" + \
        "ℹ️ " + space("Version : ", str(information['version'])) + "\n" +\
        "📆 " + space("Date: ", str(datetime.date.today()).replace("-", "/") )+ "\n" + \
        "❕ " + space("Variant: ", str(information["variant"]) ) + "\n" + \
        "⬇️ " + space("<a href=\"https://projectsakura.xyz/download/#/\">Download</a>", "") + "\n" + \
        "📰 " + space("<a href=\"https://projectsakura.xyz/blog/#/\">Blog</a>", "") + "\n\n" + \
        "#" + str(information['device']) + " | #projectsakura" + "\n" + \
        "@ProjectSakuraUpdates | @ProjectSakura"
    return message


new = get_id()
old = read_old()

if new == old:
    print("All Updated\nNothing to do\nExiting")
    exit()

print(get_diff(new, old))
for i in get_diff(new, old):
    print(i)
    info = get_info(i)
    send_mes(cook_content(info))
    send_photo("post-bot/post.jpg", cook_content(info))
    time.sleep(15)

update(new)
