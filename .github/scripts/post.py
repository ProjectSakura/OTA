#!/usr/bin/env python
#
# Python code which automatically sends a Message in a Telegram Group if any new update is found.
# Intended to be run on every push
# USAGE : python post.py
# See README for more.
#
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
BOT_API = os.environ.get("BOT_API")
CHAT_ID = os.environ.get("CHAT")

STICKER_ID = "CAADBQADhQEAAuMfMFaRTTlHKvI1RwI"

# Init the bot
bot = telebot.TeleBot(BOT_API, parse_mode="HTML")

# Where to look for .json files
fileDir = "website"
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
    with open(".github/scripts/log.txt", "w+") as f:
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
        file = open( fileDir + "/" + a, "r")
        json_processed = json.loads(file.read())
        file_id.append(json_processed['response'][0]['id'])
    return file_id


# Return previous IDs
def read_old():
    old_id = []
    file = open(".github/scripts/log.txt", "r")
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
        file = open(fileDir + "/" + a, "r")
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
    elif "GAPPS-Core" in required['filename']:
        variant = "GApps Core"
    elif "GAPPS-Basic" in required['filename']:
        variant = "GApps Basic"
    elif "microg" in required['filename'].lower():
        variant = "MicroG"
    else:
        variant = "GApps"

    if required['updater']:
        notes = "✅ OTA has been pushed; Clean flash not mandatory"
    else:
        notes = "❎ OTA not pushed; Clean flash mandatory"

    print("Device is : " + device)
    print("Size is : " + str(required['size']))
    print("Maintained by : " + maintainer)
    print("File name : " + required['filename'])
    print("Version : " + required['version'])
    print("Variant : " + variant)
    print("Notes : " + notes)

    return {
        "device": device,
        "size": str(required['size']),
        "maintainer": maintainer,
        "variant": variant,
        "version" : required['version'],
        'name' : name,
        "brand" : brand,
        "notes" : notes,
        "time" : required['datetime'],
        "filename" : required['filename'],
        "id" : required['id'],
        "romtype" : required['romtype'],
        "url" : required['url'],
        "updater" : required['updater']
    }


def bold(text1, text2):
    message = "<b>" + text1 + "</b>" + text2
    return message


# Prepare in the format needed
def cook_content(information):
    message = ""
    # links need to be in this format <a href="http://www.example.com/">inline URL</a>
    message = message + \
        "<b>New Update for " + information['name'] +  " (" + str(information['device'] ) + ") is here!</b>\n" + \
        "👤 " + bold("by ", str(information["maintainer"])) + "\n\n" + \
        "ℹ️ " + bold("Version : ", str(information['version'])) + "\n" +\
        "📆 " + bold("Date: ", str(datetime.date.today()).replace("-", "/")) + "\n" + \
        "❕ " + bold("Variant: ", str(information["variant"])) + "\n" + \
        "⬇️ " + bold("<a href=\"https://projectsakura.xyz/download/#/\">Download</a>", "") + "\n" + \
        "📰 " + bold("<a href=\"https://projectsakura.xyz/blog/#/\">Blog</a>", "") + "\n\n" + \
        bold(information['notes'], "") + "\n\n" + \
        "#" + str(information['device']) + " | #projectsakura" + "\n" + \
        "@ProjectSakuraUpdates | @ProjectSakura"
    return message


def update_json(information):
    new = "{\n" \
          "\"response\": [\n" \
          "{\n" \
          " \"datetime\": \"" + information['time'] + "\",\n" \
          " \"filename\": \"" + information['filename'] + "\",\n" \
          " \"id\": \""+ information['id']+  "\",\n" \
          " \"romtype\":\"" + information['romtype'] + "\",\n" \
          " \"size\": " + information['size'] + ",\n" \
          " \"url\": \"" + information['url'] + "\",\n"\
          " \"version\": \"" + information['version'] + "\"\n"\
          "}\n" \
          "]\n" \
          "}\n"
    file = open("updater/" + information['device'] + ".json", "w+")
    file.write(new)

new = get_id()
old = read_old()

if len(get_diff(new, old)) == 0:
    print("All Updated\nNothing to do\nExiting")
    exit()

print(get_diff(new, old))
for i in get_diff(new, old):
    print(i)
    info = get_info(i)
    bot.send_sticker(CHAT_ID, STICKER_ID)
    #send_mes(cook_content(info))
    send_photo(".github/scripts/banner.png", cook_content(info))
    if info["updater"]:
        update_json(info)
    time.sleep(15)

update(new)
