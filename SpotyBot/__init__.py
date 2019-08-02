from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from SpotyBot.config import channel_access_token,channel_secret


app = Flask(__name__)

lineBotApi = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    # app.logger.info("Request Body: "+body)

    try:
        events = parser.parse(body,signature)
    except InvalidSignatureError as e:
        abort(400)

    print("--------------")
    # for event in events:
    #     print(type(event))
    #     print('\n\n\n')
    #     print(event.__dict__)
    #     print(event.reply_token)

    for event in events:
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                lineBotApi.reply_message(event.reply_token,TextSendMessage(text="Hai"))


    # for event in events:
    #     if not isinstance(event, MessageEvent):
    #         app.logger.info("Events: \n"+events)
    #     if not isinstance(event.message, TextMessage):
    #         continue

    #     lineBotApi.reply_message(
    #             event.reply_token,
    #             TextSendMessage(text=event.message.text)
    #             )
    return 'OK'



