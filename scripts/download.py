import requests
import json
import os


URLS_FILE = '../configs/urls.json'
DOWNLOAD_PATH = '../dataset/original/'


def downloadVideo(obj, resolution):
    url = obj[resolution]
    chunk_size = 256
    r = requests.get(url, stream=True)
    filename = DOWNLOAD_PATH+obj['word'].lower().replace(' ', '-').replace('(', '').replace(')', '')+'.mp4'
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)

def downloadAllVideos(resolution):
    if not os.path.isdir(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    links = json.load(open(URLS_FILE))
    for link in links['links']:
        print('Downloading "' + link['word'] + '"')
        downloadVideo(link, resolution)
        

downloadAllVideos('480')