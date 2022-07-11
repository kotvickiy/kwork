#!/usr/bin/env python3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from crontab import CronTab
from run import run
import os
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myselfserver = s.getsockname()[0]

try:
    cron  = str(list(CronTab(user="vladium"))[-1])
except:
    os.system(f'crontab -l > foocron; echo "# @reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n# @reboot /usr/bin/sleep 20; cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/bot.py >> out.log 2>&1\n# */5 * * * * cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/run.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

b0 = KeyboardButton("verify")
b1 = KeyboardButton("run")
b2 = KeyboardButton("kcu")
b3 = KeyboardButton("kcd")

kb_client0 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client0.row(b1, b0)

kb_client1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client1.row(b1, b2)

kb_client2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client2.row(b1, b3)

@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await bot.send_message(message.from_user.id, "start", reply_markup=kb_client0)
    await message.delete()


async def on_startup(_):
    print(f"Бот вышел в онлайн {datetime.now().strftime('%H:%M:%S %d-%m-%y')}")


@dp.message_handler()
async def echo_send(message : types.Message):
    if message.text.lower() == "run":
        await bot.send_message(message.from_user.id, "run..")
        await message.delete()
        run()
        await bot.send_message(message.from_user.id, "runend")
    elif message.text.lower() == "verify":
        await message.delete()
        cron  = str(list(CronTab(user="vladium"))[-1])
        if cron[0] == "#":
            await bot.send_message(message.from_user.id, "Выключен", reply_markup=kb_client1)
        else:
            await bot.send_message(message.from_user.id, "Включен", reply_markup=kb_client2)
    elif message.text.lower() == "kcu":
        cron  = str(list(CronTab(user="vladium"))[-1])
        await bot.send_message(message.from_user.id, "kcu", reply_markup=kb_client2)
        await message.delete()
        os.system(f'crontab -l > foocron; echo "@reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n@reboot /usr/bin/sleep 20; cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/bot.py >> out.log 2>&1\n*/5 * * * * cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/run.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')
        cron  = str(list(CronTab(user="vladium"))[-1])
        await bot.send_message(message.from_user.id, "Включен")
    elif message.text.lower() == "kcd":
        cron  = str(list(CronTab(user="vladium"))[-1])
        await bot.send_message(message.from_user.id, "kcd", reply_markup=kb_client1)
        await message.delete()
        os.system(f'crontab -l > foocron; echo "@reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n@reboot /usr/bin/sleep 20; cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/bot.py >> out.log 2>&1\n# */5 * * * * cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/run.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')
        cron  = str(list(CronTab(user="vladium"))[-1])
        await bot.send_message(message.from_user.id, "Выключен")


executor.start_polling(dp, skip_updates=True)
