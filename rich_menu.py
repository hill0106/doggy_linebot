import requests
import json
from linebot import (
    LineBotApi, WebhookHandler
)

line_access_token = "Ujy55gQnq+VJ4hxrbgTGgK8RSvYiHmFKgIQ/Qku9P1QRASa6TxiInCi9lRT0Er/K9jHa5xu0o/5kxxfpYUufmEmwLeoo8CWJRYc62APITkVKrThOtVnX8QRCMMeTPcjkFxOVOqUBLb7tL1k2LjkK4AdB04t89/1O/w1cDnyilFU="

Authorization_token = "Bearer " + line_access_token

headers = {"Authorization":Authorization_token, "Content-Type":"application/json"}

#---------------------------------------------------------------------------------

# body = {
#     "size": {"width": 2500, "height": 1680},
#     "selected": "false",
#     "name": "Menu",
#     "chatBarText": "選單",
#     "areas":[
#         {
#           "bounds": {"x": 2500/3+1, "y": 0, "width": 2500/3, "height": 840},
#           "action": {"type": "message", "text": "狗狗基本資訊"}
#         },
#         {
#           "bounds": {"x": 2500-(2500/3), "y": 0, "width": 2500/3, "height": 840},
#           "action": {"type": "message", "text": "狗狗百科"}
#         },
#         {
#           "bounds": {"x": 0, "y": 841, "width": 2500/3, "height": 840},
#           "action": {"type": "message", "text": "附近動物收容所"}
#         },
#         {
#           "bounds": {"x": 2500/3+1, "y": 841, "width": 2500/3, "height": 840},
#           "action": {"type": "message", "text": "附近寵物美容"}
#         },
#         {
#           "bounds": {"x": 2500-(2500/3), "y": 841, "width": 2500/3, "height": 840},
#           "action": {"type": "message", "text": "附近動物醫院"}
#         },
#     ]
#   }

# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                        headers=headers,data=json.dumps(body).encode('utf-8'))

# print(req.text)

#---------------------------------------------------------------------------------

line_bot_api = LineBotApi(line_access_token)

rich_menu_id = "richmenu-915e7758b854ea29a3907af27d4ef7c8" # 設定成我們的 Rich Menu ID

path = "static/images/doggy-menu.png"

with open(path, 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)
print(req.text)

rich_menu_list = line_bot_api.get_rich_menu_list()