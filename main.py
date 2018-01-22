import pafy
import yaml
from googleapiclient.discovery import build

#Autheniticating the developer keys
envconfig = 'C:\Users\Ronak Shah\Google Drive\Documents/config_YT.yml'
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

def collect_urls(get_playlist_items):
    local_lists = []
    for items in get_playlist_items['items']:
        local_lists.append(items['snippet']['resourceId']['videoId'])

    return local_lists

def channels_list_by_channel_playlist(service):
    #Get the upload_id first
    get_all_videos = service.channels().list(part='snippet,contentDetails',
                                           id='channel_id').execute()
    upload_id = get_all_videos['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    #Get all the videos uploaded by that id
    url_lists = []
    get_playlist_items = service.playlistItems().list(part='snippet,contentDetails',
                                                     maxResults=50,
                                                     playlistId=upload_id).execute()

    url_lists.extend(collect_urls(get_playlist_items))
    #To get results from the next page get the next page token from each request
    while('nextPageToken' in get_playlist_items.keys()) :
        get_playlist_items = service.playlistItems().list(part='snippet,contentDetails',
                                                        maxResults=50,
                                                        playlistId=upload_id,
                                                        pageToken = get_playlist_items['nextPageToken']).execute()

        url_lists.extend(collect_urls(get_playlist_items))

    return  url_lists

if __name__ == '__main__' :
    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY, cache_discovery=False)
    url_lists = channels_list_by_channel_playlist(service)
    download_videos(url_lists)
