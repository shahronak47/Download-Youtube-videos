import pafy
import pdb
import yaml
from googleapiclient.discovery import build

#Autheniticating the developer keys
envconfig = 'C:\Users\Ronak Shah\Google Drive\Download Youtube videos/config_YT.yml'
with open(envconfig, 'r') as f:
    doc = yaml.load(f)

DEVELOPER_KEY = doc['YT']['api_key']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search_by_term(service, keyword):

    search_response = service.search().list(
        q=keyword,
        part="id",
        maxResults=20
    ).execute()

    url_lists = []

    for item in search_response['items'] :
        try:
            url_lists.append(item['id']['videoId'])
        except :
            pass


    return url_lists

def download_videos(url_lists) :
    prefix = "https://www.youtube.com/watch?v="
    updated_url_lists = [prefix + s for s in url_lists]
    for url in updated_url_lists:
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")
        filename = best.download(quiet=False)

def channels_list_by_channel_playlist(service):
    get_playlist_items = service.playlistItems().list(part='snippet,contentDetails',
    maxResults=50,
    playlistId='your_playlist_ID').execute()

    url_lists = []
    for items in get_playlist_items['items'] :
        url_lists.append(items['snippet']['resourceId']['videoId'])

    return  url_lists

if __name__ == '__main__' :
    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY, cache_discovery=False)
    url_lists = channels_list_by_channel_playlist(service)
    download_videos(url_lists)
