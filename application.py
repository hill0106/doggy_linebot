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
import os
import dynamoDB
import uuid
from werkzeug.utils import secure_filename
import line_bot
import azure_blob


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config["UPLOAD_FOLDER"] = "static/images/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#TODO change ngrok
web = "https://5ca2-114-43-33-129.ngrok.io" 

line_bot_api = LineBotApi('lGZbce+6yAPMFRFC8CzxljUBQhIh5xZUplA+ATJEx110zqLszDEVNlotC/LzdcMP9jHa5xu0o/5kxxfpYUufmEmwLeoo8CWJRYc62APITkW2M2lpkeZQHXUmk9WE7LRAnc4wfWCKSPGZIIF8y1Nt1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5bcba98158a399ea72911c72162da036')

@app.route("/dic", methods=['POST', 'GET'])
def dic():
    item = dynamoDB.ShowAll()
    for i in item:
        info = i['info'].split('\n')
        i['info'] = info
    return render_template('dic.html', item = item)

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
    

@app.route("/allDog", methods=['POST', 'GET']) 
def allDog():
    userId = request.args.get('userId')
    session['userId'] = userId
    item = dynamoDB.ShowAllPet(userId)
    for i in item:
        if i['sex']=='male':
            i['sex']='男生'
        elif i['sex']=='female':
            i['sex']='女生'
        else:
            i['sex']='未知'
        petId = i['id']
        editUrl = "https://liff.line.me/1657798815-EoY1x9KN?itemId={}?userId={}".format(petId, userId)
        i['editUrl']=editUrl
    return render_template('all_dog_info.html', item=item)

@app.route("/webDelete", methods=['POST', 'GET']) 
def webDelete():
    petId = request.form.get('id')
    user_id = session.get('userId', None)
    app.logger.info(user_id)
    app.logger.info(petId)
    dynamoDB.deletePet(user_id, petId)
    item = dynamoDB.ShowAllPet(user_id)
    for i in item:
        if i['sex']=='male':
            i['sex']='男生'
        elif i['sex']=='female':
            i['sex']='女生'
        else:
            i['sex']='未知'
        petId = i['id']
        editUrl = "https://liff.line.me/1657798815-EoY1x9KN?itemId={}?userId={}".format(petId, user_id)
        i['editUrl']=editUrl
    return render_template('all_dog_info.html', item=item)


@app.route('/liff', methods = ['POST'])
def liff():
    session['userId'] = request.form.get('userId')
    return render_template('add_pet.html') 



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
        if birthDate=="" or type=="" or petNumber=="":
            birthDate=" "
            type=" "
            petNumber=" "
        if file and is_allowed_file(file.filename):
            filename = _id + '.jpeg'
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
        imgUrl = azure_blob.uploadImage(path, filename)
        pet = [userId, _id, name, birthDate, sex, petNumber, type, imgUrl] # save to DB
        app.logger.info(pet)
        dynamoDB.insertPet(pet)
        session.clear()
    return '<h1 style="display: flex; justify-content: center; align-items: center; font-size: 3rem">已新增資料，您可以關閉畫面了</h1>'

@app.route('/receiveParams', methods=['POST'])
def receiveParams():
    user_id = request.form.get('userId')
    item_id = request.form.get('itemId')

    session['userId'] = user_id
    session['itemId'] = item_id

    item = dynamoDB.ShowPet(user_id, item_id)

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
        if file.filename!='' and is_allowed_file(file.filename):
            filename = _id + '.jpeg'
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            imgUrl = azure_blob.uploadImage(path, filename)
            azure_blob.deleteImage(oldid)
        else:
            imgUrl = "https://1111ainutrition.blob.core.windows.net/dog/" + oldid + ".jpeg"
        pet = [userId, oldid, name, birthDate, sex, petNumber, type, imgUrl] # save to DB
        
        dynamoDB.updatePet(pet)
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
        app.logger.info(postback_data.get('petId'))
        if dynamoDB.deletePet(user_id, postback_data.get('petId')):
            azure_blob.deleteImage(postback_data.get('petId'))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "刪除成功"))

        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "無法刪除，請稍後再試"))
    elif postback_data.get('action')=='passDelete':
        petId = postback_data.get('petId')
        petName = postback_data.get('petName')
        line_bot.DeleteConfirm(event, petId, petName)
    elif postback_data.get('action')=='passEdit':
        petId = postback_data.get('petId')
        petName = postback_data.get('petName')
        app.logger.info(petId, petName)
        line_bot.call_send_liff(event, _id=petId, userId=user_id, text="編輯"+petName, url="https://liff.line.me/1657798815-EoY1x9KN?itemId={}?userId={}".format(petId, user_id))

@handler.add(MessageEvent)
def handle_something(event):
    user_id = event.source.user_id
    if event.message.type=='text':
        receive_text=event.message.text
        if '狗狗基本資訊' in receive_text:
            line_bot.show_pet_info(event)
        elif '查詢狗狗基本資料' in receive_text:
            item = dynamoDB.ShowAllPet(user_id)
            if item != []:
                # ShowCarouselItem(event, item)
                if len(item) < 12:
                    line_bot.ShowCarouselItem(event, item)
                else:
                    line_bot.call_send_liff(event=event, text="完整狗狗資訊", url=web+"/allDog?userId={}".format(user_id))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "目前沒有寵物資訊"))
        elif '新增狗狗基本資料' in receive_text:
            line_bot.call_send_liff(event=event, text="新增狗狗基本資料", url="https://liff.line.me/1657798815-ExLXzO2y")
        elif '附近寵物美容' in receive_text:
            line_bot.call_open_link(event, '附近寵物美容', web+"/petStore")
        elif '附近動物收容所' in receive_text:
            line_bot.call_open_link(event, '附近動物收容所', web+"/shelter")
        elif '附近動物醫院' in receive_text:
            line_bot.call_open_link(event, '附近動物醫院', web+"/hospital")
        elif '狗狗百科' in receive_text:
            line_bot.call_open_link(event, '狗狗百科', web+"/dic")
        elif '辨識狗狗品種' in receive_text:
            line_bot.call_open_link(event, '辨識狗狗品種', web+"/type")
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="無法辨識的指令，請重新輸入..."))

def is_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)