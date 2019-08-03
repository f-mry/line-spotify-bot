from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from SpotyBot.config import channel_access_token,channel_secret


app = Flask(__name__)

lineBotApi = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)

from SpotyBot import handlerModule


@app.route('/')
def index():
    return 'Hello world'

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("\nRequest Body: "+body)

    try:
        # events = parser.parse(body,signature)
        handler.handle(body,signature)
    except InvalidSignatureError as e:
        abort(400)

    # for event in events:
    #     if isinstance(event, MessageEvent):
    #         if isinstance(event.message, TextMessage):
    #             lineBotApi.reply_message(event.reply_token,TextSendMessage(text="Hai"))
                
    return 'OK'




