from application import *

def call_dog_Data(item):
    for i in item:
        message = FlexSendMessage(
            alt_text="狗狗品種百科",
            contents= {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": i['img'],
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": i['name'],
                        "weight": "bold",
                        "size": "xl",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": i['info'],
                        "wrap": True,
                        "margin": "5px",
                        "size": "lg"
                    }
                    ]
                }
            }
                
        )
    return message

def call_open_link(event, text, url):
    message = TemplateSendMessage(
        alt_text = '顯示' + text,
        template = ButtonsTemplate(
            text = text,
            actions = [
                URIAction(
                    label = '前往' + text +'頁面',
                    uri = url
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def show_pet_info(event):
    message = TemplateSendMessage(
        alt_text='顯示狗狗資訊按鈕',
        template=ButtonsTemplate(
            title='狗狗資訊',
            text='請在下方點選您需要的服務項目',
            actions=[
                MessageAction(
                    label='新增狗狗基本資料',
                    text='新增狗狗基本資料'
                ),
                MessageAction(
                    label='查詢狗狗基本資料',
                    text='查詢狗狗基本資料'
                ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def call_send_liff(event, _id="", userId="", text="", url=""):
    message = FlexSendMessage(
        alt_text=text,
        contents= {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "請您前往頁面",
                    "weight": "bold",
                    "size": "lg"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": text,
                    "uri": url
                    }
                }
                ],
                "flex": 0
            }
            }
    )
    line_bot_api.reply_message(event.reply_token, message)

def ShowCarouselItem(event, item):
    contents = dict()
    contents['type'] = 'carousel'
    bubbles=[]
    for i in item: #change item
        bubble = {
                "type": "bubble",
                "size": "kilo",
                "hero": {
                    "type": "image",
                    "url": i['img'],
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": i['pet_name'],
                        "weight": "bold",
                        "size": "xl",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "生日：",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": i['birth'],
                            "size": "sm",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "offsetEnd": "70px",
                            "color": "#28576a"
                        }
                        ],
                        "justifyContent": "space-around",
                        "alignItems": "center"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "性別：",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": translate(i['sex']),
                            "size": "sm",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "offsetEnd": "70px",
                            "color": "#28576a"
                        }
                        ],
                        "justifyContent": "space-around",
                        "alignItems": "center"
                    },
                    
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "品種：",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": i['pet_type'],
                            "size": "sm",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "offsetEnd": "70px",
                            "color": "#28576a"
                        }
                        ],
                        "justifyContent": "space-around",
                        "alignItems": "center"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "晶片：",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": i['chip_number'],
                            "size": "sm",
                            "margin": "none",
                            "align": "start",
                            "gravity": "center",
                            "offsetEnd": "70px",
                            "color": "#28576a"
                        }
                        ],
                        "justifyContent": "space-around",
                        "alignItems": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "10px"
                    }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://cdn-icons-png.flaticon.com/512/2280/2280557.png",
                            "size": "15px",
                            "offsetEnd": "28px"
                        },
                        {
                            "type": "button",
                            "action": 
                            {
                                "type": "postback",
                                "label": "編輯",
                                "data": "action=passEdit&petId={}&petName={}".format(i['id'], i['pet_name']),
                                "displayText": "編輯" + i['pet_name'],
                            },
                            "color": "#f8b10b",
                            "position": "absolute"
                        }
                        ],
                        "justifyContent": "center",
                        "alignItems": "center"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "image",
                            "url": "https://cdn-icons-png.flaticon.com/512/484/484560.png",
                            "size": "15px",
                            "offsetEnd": "28px"
                        },
                        {
                            "type": "button",
                            "action": 
                            {
                                "type": "postback",
                                "label": "刪除",
                                "data": "action=passDelete&petId={}&petName={}".format(i['id'], i['pet_name']),
                                "displayText": "刪除"+i['pet_name']
                            },
                            "color": "#999999",
                            "position": "absolute"
                        }
                        ],
                        "justifyContent": "center",
                        "alignItems": "center"
                    }
                    ],
                    "justifyContent": "flex-start",
                    "alignItems": "center",
                    "height": "40px",
                    "paddingBottom": "25px"
                }
        }
        bubbles.append(bubble)
    contents['contents']=bubbles
    message = FlexSendMessage(
        alt_text="Dog Info",
        contents= contents
    )
    line_bot_api.reply_message(event.reply_token, message)

def translate(i):
    if i=='male':
        return '男生'
    if i=='female':
        return '女生'

def DeleteConfirm(event, petId, petName):
    confirm_template_message = TemplateSendMessage(
        alt_text='Confirm Delete',
        template=ConfirmTemplate(
            text='是否確定要刪除{}?'.format(petName),
            actions=[
                PostbackAction(
                    label='是',
                    display_text='是',
                    data='action=delete&petId={}'.format(petId),
                ),
                PostbackAction(
                    label='否',
                    display_text='否',
                    data='action=keep'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, confirm_template_message)