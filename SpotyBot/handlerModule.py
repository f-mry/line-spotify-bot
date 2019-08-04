from linebot import LineBotApi, WebhookParser, WebhookHandler 
from linebot.exceptions import LineBotApiError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, 
                            AudioSendMessage, ImageSendMessage, BubbleContainer,
                            BoxComponent, TextComponent, ImageComponent, SpacerComponent,
                            URIAction, ButtonComponent,SeparatorComponent, FlexSendMessage,
                            FollowEvent
                           )
from SpotyBot import lineBotApi, handler
from SpotyBot.spotifyUtil import searchMusic

def getTrackData(keyword):
    data = searchMusic(keyword)
    return (data,data.get('trackURL'),data.get('previewURL'),data.get('trackTitle'),
            data.get('trackArtist'),data.get('trackImg'),data.get('trackAlbum')
            )

def prepareFlexMessage(data):
    heroImage = data.get('trackImg')[0].get('url')
    artistText = data.get('trackArtist')
    titleText = data.get('trackTitle')
    trackURL = data.get('trackURL')
    album = data.get('trackAlbum')

    if album.get('album_type') == 'album':
        albumText = album.get('name')
    else:
        albumText = 'single'


    bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url=heroImage,
                size='full',
                aspect_ratio='4:3',
                aspect_mode='cover',
                action=URIAction(label='album Image',uri=heroImage)
                ), #end hero
            body=BoxComponent(
                layout='vertical',
                contents=[
                    #Track Title
                    TextComponent(text=titleText,size='xl',weight='bold',wrap=True),
                    BoxComponent(
                        layout='vertical',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='xs',
                                contents=[
                                    TextComponent(text='Artist',size='sm',color='#aaaaaa',flex=1),
                                    TextComponent(text=artistText,size='sm',wrap=True,flex=5)
                                    ]
                                ),
                            BoxComponent(
                                layout='baseline',
                                spacing='xs',
                                contents=[
                                    TextComponent(text='Album',size='sm',color='#aaaaaa',flex=1),
                                    TextComponent(text=albumText,size='sm',wrap=True,flex=5)
                                    ]
                                )
                            ]
                        )
                    ]
                ), #end body
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        height='sm',
                        action=URIAction(label='Open in Spotify',uri=trackURL)
                        )
                    ]
                ) # end footer
            ) #end buble
    # print(bubble)
    return bubble

@handler.add(MessageEvent, message=TextMessage)
def textHandler(event):
    userId = event.source.user_id

    data, trackURL, previewURL, title, artist, img, album = getTrackData(event.message.text)
    print("\n\n\n")
    print(data)
    print("\n\n\n")

    flexMessage = prepareFlexMessage(data)

    lineBotApi.reply_message(
            event.reply_token,FlexSendMessage(alt_text="Here is your search result", contents=flexMessage)
            )

    if previewURL != None:
        lineBotApi.push_message(userId,AudioSendMessage(previewURL,30000))
    else:
        lineBotApi.push_message(userId,TextSendMessage(text='No Audio Preview Available'))

@handler.add(FollowEvent)
def followHandler(event):
    userId = event.source.user_id
    # try:
    #     lineBotApi.get_profile(userId)
    # except LineBotApi
    userProfile = lineBotApi.get_profile(userId)


    

