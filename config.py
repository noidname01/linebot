from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# ====== call richMenu class =====
from richmenu import *
# ====== call richMenu class =====

# ======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
from config import *
from richmenu import *
from postgresql import *
# ======這裡是呼叫的檔案內容=====


# Channel Access Token
line_bot_api = LineBotApi(
    'UKlTbRDYfiAr5qRlevtnw54VDBLcVkZJFrf8wjSGK7jzGkw1Repbz5sZlr/hZtWc7hCZJ1ueQRjyfUetBpFABV1mcglowltYbXYEe6jXr3zq4Oal8HBEJf+OyFxt/vEypMyNAAuV2vU+IJlO7xr+4AdB04t89/1O/w1cDnyilFU=')

# Channel Secret
handler = WebhookHandler('38b13a972ae57555c8bd095501d9b184')


stateDict = {

}


# ====================================== 這邊是有齊的部分 =======================================


# Read json file

with open('bubble_1.json') as json_file:
    bubble_template = json.load(json_file)


# ====================================== 這邊是友廷的部分 =========================================

generalRichMenuSize = (2500, 1686)

mainRichMenuDict = {
    "coordinates": [(0, 0), (833, 0), (1666, 0), (0, 843), (1250, 843)],
    "sizes": [(833, 843), (833, 843), (834, 843), (1250, 843, 1250, 843)],
    "postBackActions":
    [
        PostbackAction(label=i, data=i, display_text=i) for i in range(5)
    ],
    "img_path": "./static/image/richmenutest.png",
    "main": True,
}

# mainRichMenu = richMenu(
#     line_bot_api, generalRichMenuSize, "homepage", "click one")
# mainRichMenu.setRichMenu(mainRichMenuDict)
# mainRichMenuId = mainRichMenu.getRichMenuId()


richMenuIdDict = {

}
