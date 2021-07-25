#!/usr/bin/env python
#
# Python code which helps keep track of monthly updates for official devices
# Working directory : inside https://github.com/ProjectSakura/OTA (branch 11)
# Intended usage : python .github/scripts/list.py
# Note !
# Set env variables as following:
# "BOT_API" to your BOT API Token
# "CHAT_PRIV" to your chat ID
# Install telebot by running "sudo pip install pyTelegramBotAPI"
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

import datetime
import json
import os
import telebot


# Get secrets from Workflow
BOT_API = os.environ.get("BOT_API")
CHAT_ID = os.environ.get("CHAT_PRIV")

# Init the bot
bot = telebot.TeleBot(BOT_API, parse_mode="HTML")

def send_mes(message):
    return bot.send_message(chat_id=CHAT_ID, text=message, disable_web_page_preview=True)


def active_devices ():
    json_processed = json.loads(open("devices.json", "r").read())
    devices = []
    for device in json_processed:
        if device['active']:
            device_json = json.loads(open(device['codename'] + ".json").read())
            devices.append({
                "codename" : device['codename'],
                "maintainer" : device['maintainer_name'],
                "datetime" : device_json['response'][0]['datetime'],
                "device_name" : device['name']
            })
    return devices


current_month = datetime.date.today().month
current_year = datetime.date.today().year
month_start = datetime.datetime(current_year, current_month, 1, 0, 0, 1)
last_month_start = datetime.datetime(current_year, current_month - 1, 1, 0, 0, 1)
last_2month_start = datetime.datetime(current_year, current_month - 2, 1, 0, 0, 1)


yetToUpdate = []
updated = []

for device in active_devices():
    if int(device['datetime']) > month_start.timestamp():
        updated.append(device)
    else:
        yetToUpdate.append(device)

notUpdatedIn2Months = []
for device in yetToUpdate:
    if not int(device['datetime']) > last_month_start.timestamp():
        notUpdatedIn2Months.append(device)

notUpdatedIn3Months = []
for device in notUpdatedIn2Months:
    if not int(device['datetime']) > last_month_start.timestamp():
        notUpdatedIn3Months.append(device)

message = "#UpdateStatus\nThe following devices has <b>been updated</b> in the current month (after " + str(month_start) + " hours):\n"
number = 1
for device in updated:
    message = message + "\n" + str(number) + ". " + device['device_name'] + " (" + device['codename'] + ") By: " + device['maintainer']
    number += 1

message = message + "\n\n\nThe following devices has <b>not been updated</b> in the current month:\n"
number = 1
for device in yetToUpdate:
    message = message + "\n" + str(number) + ". " + device['device_name'] + " (" + device['codename'] + ") By: " + device['maintainer']
    number += 1

message = message + "\n\n\nThe following devices has <b>not been updated in previous month too</b>:\n"
number = 1
for device in notUpdatedIn2Months:
    message = message + "\n" + str(number) + ". " + device['device_name'] + " (" + device['codename'] + ") By: " + device['maintainer']
    number += 1
if len(notUpdatedIn2Months) == 0:
    message = message + "\nNONE"

message = message + "\n\n\nThe following devices has <b>not been updated in 3 months</b>:\n"
number = 1
for device in notUpdatedIn3Months:
    message = message + "\n" + str(number) + ". " + device['device_name'] + " (" + device['codename'] + ") By: " + device['maintainer']
    number += 1
if len(notUpdatedIn3Months) == 0:
    message = message + "\nNONE"

message = message + "\n\nTotal Official Devices = " + str(len(active_devices())) + "\nUpdated during current month = " + str(len(updated)) + "\nNot Updated during current month = " + str(len(yetToUpdate))  + "\nNot Updated in last month = " + str(len(notUpdatedIn2Months)) + "\nNot Updated in 3 months = " + str(len(notUpdatedIn3Months))

message = message + "\n\nInformation as on : " + str(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')) + " hours (UTC)"

send_mes(message)