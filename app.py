from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage,ImageSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('s3ISlI0hW7QXDijEL7Fhb1160NEuTq7v18grJRSYlLBzAWWMAWErEaQXpN5G8wFd45l0VP0I/M278hA6zlhp5YraquXnWmxw8wA0Y9peMLr4jzeNv+pFndkrM7cei/mr4XeYwpWXSBYUUK89FMemCwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('55284a15da3bddc81dfb2405775e7b82')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    word=event.message.text
    url=f'https://www.google.com/search?q={word}&tbm=isch'
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)" \
     "AppleWebKit/537.36 (KHTML, like Gecko)" \
     "Chrome/60.0.3112.113"
    headers={"User-Agent": ua}
    response=requests.get(url)
    soup=BeautifulSoup(response.text)
    images=soup.find_all('img')
    del images[0]
    image_url=random.choice(images)['src']
    

    message = ImageSendMessage(
    original_content_url=image_url,
    preview_image_url=image_url
)
    line_bot_api.reply_message(
        event.reply_token,
        message)


if __name__ == "__main__":
    app.run()