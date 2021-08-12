import requests


def send_telegram(text: str):
    token = "1899350948:AAH7q4oXwqRgWOMXWftGOzrMMZzVqQgyhUs"
    url = "https://api.telegram.org/bot"
    channel_id = "389561175"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")

