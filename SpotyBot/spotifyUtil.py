from SpotyBot.config import CLIENTID, CLIENTSECRET
import requests, json
from urllib.parse import urlencode

grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}
url = 'https://accounts.spotify.com/api/token'

def getToken():
    response = requests.post(url, data=body_params, auth = (CLIENTID, CLIENTSECRET)) 
    tokenRaw = json.loads(response.text)
    return tokenRaw['access_token']

def searchMusic(keyword):
    queryDict = {
                'q': keyword,
                'type': 'track',
                'limit': 1,
                'offset': 0,
            }
    query = urlencode(queryDict)
    endpoint = 'https://api.spotify.com/v1/search?'
    url = endpoint+query
    authToken = getToken()

    response = requests.get(url,headers={'Authorization' : 'Bearer '+authToken}) 

    parsed = json.loads(response.content.decode('utf-8'))
    parsed = parsed.get('tracks').get('items')[0]
    parsed.get('album').pop('available_markets')

    dataDict = {
            'trackURL' : parsed.get('external_urls').get('spotify'),
            'previewURL' : parsed.get('preview_url'),
            'trackTitle' : parsed.get('name'),
            'trackArtist' : parsed.get('artists')[0].get('name'),
            'trackImg' : parsed.get('album').get('images'),
            'trackAlbum' : parsed.get('album')
            }

    return dataDict
    
if __name__ == '__main__':
    result = searchMusic(input("Search Music: "))
