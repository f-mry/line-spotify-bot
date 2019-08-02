from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from SpotyBot import lineBotApi, handler

@handler.add(MessageEvent)
def textHandler(event):
    lineBotApi.reply_message(
            event.reply_token,
            TextSendMessage(text="Ini percobaan dari handler")
            )
