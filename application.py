from flask import *
from urllib.parse import parse_qsl, parse_qs
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    VideoSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    PostbackEvent, ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage
)

from dynamoDB import *
import uuid
from werkzeug.utils import secure_filename
from line_bot import *
from azure_blob import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config["UPLOAD_FOLDER"] = "static/images/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

line_bot_api = LineBotApi('Ujy55gQnq+VJ4hxrbgTGgK8RSvYiHmFKgIQ/Qku9P1QRASa6TxiInCi9lRT0Er/K9jHa5xu0o/5kxxfpYUufmEmwLeoo8CWJRYc62APITkVKrThOtVnX8QRCMMeTPcjkFxOVOqUBLb7tL1k2LjkK4AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5bcba98158a399ea72911c72162da036')

web = "https://doggylinebot.azurewebsites.net"

@app.route("/dic", methods=['POST', 'GET'])
def dic():
    item = ShowAll()
    for i in item:
        info = i['info'].split('\n')
        i['info'] = info
    return render_template('dic.html', item = item)

@app.route("/dogInfo", methods=['POST', 'GET'])
def dogInfo():
    return render_template('all_dog_info.html')

@app.route("/sendDogInfo", methods=['POST', 'GET'])
def sendDogInfo():
    userId = session.get('userId', None)
    item = ShowAllPet(userId)
    return jsonify(item)

@app.route("/hospital", methods=['POST', 'GET'])
def hospital():
    return render_template('pet_hospital.html')

@app.route("/displayLiff", methods=['POST', 'GET'])
def displayLiff():
    return render_template('empty.html')

@app.route("/petStore", methods=['POST', 'GET'])
def petStore():
    return render_template('pet_store.html')

@app.route("/shelter", methods=['POST', 'GET'])
def shelter():
    return render_template('pet_shelter.html')


@app.route("/addPet", methods=['POST', 'GET']) 
def addPet():
    return render_template('add_pet.html')

@app.route("/editPet", methods=['POST', 'GET']) 
def editPet():
    return render_template('edit_pet.html')

@app.route('/liff', methods = ['POST'])
def liff():
    session['userId'] = request.form.get('userId')
    return render_template('add_pet.html') #receiveEditPet

@app.route('/receiveAddPet', methods = ['GET', 'POST'])
def receiveAddPet():
    if request.method == 'POST':
        name = request.form['petName']
        birthDate = request.form['petBirthDate']
        sex  = request.form['petSex']
        type  = request.form['petType']        
        userId = session.get('userId', None)
        petNumber = request.form['petNumber']  
        _id = str(uuid.uuid1())
        file = request.files['file']
        if file and is_allowed_file(file.filename):
            filename = _id + '.jpeg'
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
        imgUrl = uploadImage(path, filename)
        pet = [userId, _id, name, birthDate, sex, petNumber, type, imgUrl] # save to DB
        insertPet(pet)
        session.clear()
    return '<h1 style="display: flex; justify-content: center; align-items: center; font-size: 3rem">已新增資料，您可以關閉畫面了</h1>'

@app.route('/receiveParams', methods=['POST'])
def receiveParams():
    user_id = request.form.get('userId')
    item_id = request.form.get('itemId')

    session['userId'] = user_id
    session['itemId'] = item_id

    item = ShowPet(user_id, item_id)

    return jsonify(item)


@app.route('/edited', methods = ['GET', 'POST'])
def edited():
    if request.method == 'POST':
        name = request.form['petName']
        birthDate = request.form['petBirthDate']
        sex  = request.form['petSex']
        type  = request.form['petType']        
        userId = session.get('userId', None)
        petNumber = request.form['petNumber']
        userId = session.get('userId', None)
        oldid = session.get('itemId', None)
        _id = str(uuid.uuid1()) 
        file = request.files['file']
        if file and is_allowed_file(file.filename):
            filename = _id + '.jpeg'
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            imgUrl = uploadImage(path, filename)
            deleteImage(oldid)
        else:
            imgUrl = "https://1111ainutrition.blob.core.windows.net/dog/" + oldid + ".jpeg"
        pet = [userId, oldid, name, birthDate, sex, petNumber, type, imgUrl] # save to DB
        
        updatePet(pet)
        # os.remove(path)
    return '<h1 style="display: flex; justify-content: center; align-items: center; font-size: 3rem">已修改資料，您可以關閉畫面了</h1>'


@app.route("/callback", methods=['POST', 'GET'])
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



@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    postback_data = dict(parse_qsl(event.postback.data))
    if postback_data.get('action')=='delete':
        if deletePet(user_id, postback_data.get('petId')):
            deleteImage(postback_data.get('petId'))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "刪除成功"))

        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "無法刪除，請稍後再試"))
    elif postback_data.get('action')=='passDelete':
        petId = postback_data.get('petId')
        petName = postback_data.get('petName')
        DeleteConfirm(event, petId, petName)
    elif postback_data.get('action')=='passEdit':
        petId = postback_data.get('petId')
        petName = postback_data.get('petName')
        call_send_liff(event, _id=petId, userId=user_id, text="編輯"+petName, url="https://liff.line.me/1657798815-EoY1x9KN?itemId={}?userId={}".format(petId, user_id))

@handler.add(MessageEvent)
def handle_something(event):
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    if event.message.type=='text':
        receive_text=event.message.text
        if '狗狗基本資訊' in receive_text:
            show_pet_info(event)
        elif '查詢狗狗基本資料' in receive_text:
            item = ShowAllPet(user_id)
            if item != []:
                if len(item) < 12:
                    ShowCarouselItem(event, item)
                else:
                    call_send_liff(event=event, text="目前資料庫超過十二樣，請您到以下網頁查看", url="https://liff.line.me/1657798815-vRKaEGrn")
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "目前沒有寵物資訊"))
        elif '新增狗狗基本資料' in receive_text:
            call_send_liff(event=event, text="新增狗狗基本資料", url="https://liff.line.me/1657798815-ExLXzO2y")
        elif '附近寵物美容' in receive_text:
            call_open_link(event, '附近寵物美容', web+"/petStore")
        elif '附近動物收容所' in receive_text:
            call_open_link(event, '附近動物收容所', web+"/shelter")
        elif '附近動物醫院' in receive_text:
            call_open_link(event, '附近動物醫院', web+"/hospital")
        elif '狗狗百科' in receive_text:
            call_open_link(event, '狗狗百科', web+"/dic")
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="無法辨識的指令，請重新輸入..."))

def is_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)