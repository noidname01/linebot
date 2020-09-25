import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


# ======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
from config import *
from richmenu import *
# ======這裡是呼叫的檔案內容=====


# ======python的函數庫==========
import tempfile
import os
import datetime
import time
import json
import copy

# ======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


# Opening JSON file
# with open('carousel.json') as json_file:
#     carousel_template = json.load(json_file)

# with open('bubble_1.json') as json_file:
#     bubble_template = json.load(json_file)
mainRichMenu = richMenu(
    line_bot_api, generalRichMenuSize, "homepage", "click one")
mainRichMenu.setRichMenu(mainRichMenuDict)
mainRichMenuId = mainRichMenu.getRichMenuId()


def create_flex_message(data_list, bubble_template, carousel_template):

    carousel = copy.deepcopy(carousel_template)

    for data in data_list:

        bubble = copy.deepcopy(bubble_template)

        question_no = data[0]
        header_text = '  '.join(data[1])
        url = data[2]
        body_text = data[3]

        bubble['header']['contents'][0]['text'] = header_text
        bubble['hero']['url'] = url
        bubble['hero']['action']['uri'] = url

        for text in body_text:

            text_dict = dict()
            text_dict['type'] = 'text'
            text_dict['text'] = text

            bubble['body']['contents'].append(text_dict)

        bubble['footer']['contents'][0]['action']['text'] = '我要解第' + \
            str(question_no) + '題'
        bubble['footer']['contents'][1]['action']['uri'] = url

        carousel['contents'].append(bubble)

    return carousel


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)

    elif 'test1' in msg:
        message = TextSendMessage(text='測試')
        message = TextSendMessage(text=str(message))
        line_bot_api.reply_message(event.reply_token, message)

    elif 'test2' in msg:
        message = Carousel_Template()
        message = TextSendMessage(text=str(message))
        line_bot_api.reply_message(event.reply_token, message)

    elif 'test3' in msg:

        question_list = [
            # |題號|            header                |           圖片url                 |                  body中的文字
            [1005, ['交換電路與邏輯設計', '課本', '7.1'], 'https://i.imgur.com/8Mjhu0Y.png',
                ['第一段我有點不懂', '第二段我也不太懂', '第三段我也不會，我是不是太笨了QQ？']],
            [1006, ['計算機概論', '作業',  '1'],
                'https://i.imgur.com/FwVstGx.png', ['這次作業好難喔', '我都不會寫']],
            [1007, ['微積分 ', '考古題', '108.1'],
                'https://i.imgur.com/x3Sftiv.png', ['吉鈞救救我']]
        ]

        carousel = create_flex_message(
            question_list, bubbleTemplate, carouselTemplate)

        message = FlexSendMessage(
            alt_text='hello',
            contents=carousel
        )

        line_bot_api.reply_message(event.reply_token, message)

    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(PostbackEvent, message=None)
def handle_postback(event):

    data = event.postback.data
    user_id = event.source.user_id

    # TODO
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
