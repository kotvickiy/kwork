#!/usr/bin/env python3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, CHAT_ID
from crontab import CronTab
from main import main
import os
import socket


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myselfserver = s.getsockname()[0]


def cron():
    return str(list(CronTab(user="vladium"))[-1])


def installation_crontab(grid_one="# ", grid_two="# ", grid_three="# "):
    os.system(f'crontab -l > foocron; echo "{grid_one}@reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n{grid_two}@reboot /usr/bin/sleep 20; cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/bot.py >> out.log 2>&1\n{grid_three}*/5 * * * * cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/main.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')


try:
    cron()
except:
    installation_crontab()


def kb():
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_client


b1 = KeyboardButton("Запустить")
b2 = KeyboardButton("Включить планировщик")
b3 = KeyboardButton("Выключить планировщик")
b4 = KeyboardButton("Проверить")
b5 = KeyboardButton("Перезагрузить")
b6 = KeyboardButton("Меню")


acl = (CHAT_ID, )
admin_only = lambda message: message.from_user.id not in acl


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(b1, b4))
    await message.delete()


async def verify(message):
    if cron()[0] == "#":
        await bot.send_message(message.from_user.id, "Выключен", reply_markup=kb().row(b2, b6))
    else:
        await bot.send_message(message.from_user.id, "Включен", reply_markup=kb().row(b3, b6))


@dp.message_handler()
async def send(message : types.Message):
    if message.text == "Запустить":
        await bot.send_message(message.from_user.id, "Запущен", reply_markup=ReplyKeyboardRemove())
        await message.delete()
        main()
        await bot.send_message(message.from_user.id, "Завершен")
        await verify(message)
    elif message.text == "Проверить":
        await message.delete()
        await verify(message)
    elif message.text == "Перезагрузить":
        await message.delete()
        sudoPassword = '241215'
        command = 'reboot'
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    elif message.text == "Secure":
        await message.delete()
        await bot.send_message(message.from_user.id, "Secure", reply_markup=kb().row(b1, b5, b6))
    elif message.text == "Меню":
        await message.delete()
        await bot.send_message(message.from_user.id, "Меню", reply_markup=kb().row(b1, b4).row(b5))
    elif message.text == "Включить планировщик":
        cron()
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(b1, b3, b6))
        await message.delete()
        installation_crontab("", "", "")
        cron()
        await bot.send_message(message.from_user.id, "Включен")
    elif message.text == "Выключить планировщик":
        cron()
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(b1, b2, b6))
        await message.delete()
        installation_crontab("", "")
        cron()
        await bot.send_message(message.from_user.id, "Выключен")


executor.start_polling(dp, skip_updates=True)
