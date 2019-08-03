from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioSendMessage, ImageSendMessage
from SpotyBot import lineBotApi, handler
from SpotyBot.spotifyUtil import searchMusic

def getTrackData(keyword):
    data = searchMusic(keyword)
    return (data.get('trackURL'),data.get('previewURL'),data.get('trackName'),
            data.get('artist'),data.get('trackImg'),data.get('album')
            )
    

@handler.add(MessageEvent, message=TextMessage)
def textHandler(event):
    userId = event.source.user_id
    lineBotApi.reply_message(
            event.reply_token,
            TextSendMessage(text='Searching for: '+event.message.text)
            )
    lineBotApi.push_message(userId,TextSendMessage(text='Testing Push'))
    trackURL, previewURL, trackName, artist, trackImg, album = getTrackData(event.message.text)

    lineBotApi.push_message(userId,TextSendMessage(text=f'''
Artist : {artist}
Title : {trackName}
Open Song : {trackURL}
        '''))
    if previewURL != None:
        lineBotApi.push_message(userId,AudioSendMessage(previewURL,30000))
    else:
        print("\nNo Preview Available\n")
    print(trackImg)

    lineBotApi.push_message(userId, ImageSendMessage(trackImg[0].get('url'), trackImg[0].get('url')))
    

