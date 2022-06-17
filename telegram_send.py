#!/usr/bin/env python3

import requests

api_token = '5256488014:AAFDMO3yLOtQDI5fo5PpTzUMf-8WWJyXpP8'
chat_id='389561175' # узнать chat_id нужно в username_to_id_bot

def send(msg):
    requests.get(f'https://api.telegram.org/bot{api_token}/sendMessage', params=dict(chat_id=chat_id,text=msg))
