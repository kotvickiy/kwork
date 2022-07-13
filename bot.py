#!/usr/bin/env python3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, CHAT_ID
from crontab import CronTab
from run import run
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
    os.system(f'crontab -l > foocron; echo "{grid_one}@reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n{grid_two}@reboot /usr/bin/sleep 20; \
    cd /home/vladium/code/kwork/ \
    && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/bot.py >> out.log 2>&1\n{grid_three}*/5 * * * * cd /home/vladium/code/kwork/ && \
    /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/run.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')


try:
    cron()
except:
    installation_crontab()
    # os.system(f'crontab -l > foocron; echo "# @reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n# @reboot /usr/bin/sleep 20; cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/bot.py >> out.log 2>&1\n# */5 * * * * cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/run.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')


b0 = KeyboardButton("Главное меню")
b1 = KeyboardButton("Запустить")
b2 = KeyboardButton("Включить планировщик")
b3 = KeyboardButton("Выключить планировщик")
b4 = KeyboardButton("Проверить")
b5 = KeyboardButton("Перезагрузить")
b6 = KeyboardButton("Secure")


def kb(button_one, button_two, button_three):
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_client.row(button_one, button_two).add(button_three)


async def verify(message):
    if cron()[0] == "#":
        await bot.send_message(message.from_user.id, "Выключен", reply_markup=kb(b1, b2, b0))
    else:
        await bot.send_message(message.from_user.id, "Включен", reply_markup=kb(b1, b3, b0))


acl = (CHAT_ID, )
admin_only = lambda message: message.from_user.id not in acl


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb(b1, b4, b6))
    await message.delete()


@dp.message_handler()
async def echo_send(message : types.Message):
    if message.text == "Запустить":
        await bot.send_message(message.from_user.id, "Запущен", reply_markup=ReplyKeyboardRemove())
        await message.delete()
        run()
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
        await bot.send_message(message.from_user.id, "Secure", reply_markup=kb(b1, b5, b0))
    elif message.text == "Главное меню":
        await message.delete()
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb(b1, b4, b6))
    elif message.text == "Включить планировщик":
        cron()
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb(b1, b3, b0))
        await message.delete()
        installation_crontab("", "", "")
        cron()
        await bot.send_message(message.from_user.id, "Включен")
    elif message.text == "Выключить планировщик":
        cron()
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb(b1, b2, b0))
        await message.delete()
        installation_crontab("", "")
        cron()
        await bot.send_message(message.from_user.id, "Выключен")


executor.start_polling(dp, skip_updates=True)
