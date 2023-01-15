from flask import Flask, request
from pytube import Playlist, YouTube
from flask_cors import CORS
from pathlib import Path

app = Flask(__name__)
CORS(app)
home_path = Path.home()
SAVE_PATH = home_path.as_posix() + '/Downloads'


@app.route('/')
def hello():
    return "Hello from server"


@app.route('/download', methods=['GET', 'POST'])
def download():
    data = request.json

    # get video url
    url = data.get('url')

    # get requested video url
    resolution = data.get('resolution')

    # check if it's a playlist
    is_playlist = data.get('isplaylist')

    if is_playlist:
        yt_playlist = Playlist(url)
        title = yt_playlist.title

        # download the playlist
        print(f'Downloading the playlist : {yt_playlist.title}')
        for index, yt_url in enumerate(yt_playlist.video_urls):
            yt_video_prefix = f'{index+1}_'
            yt_video = YouTube(yt_url)
            download_video(yt_video, resolution, SAVE_PATH, yt_video_prefix)

    else:
        yt_video = YouTube(url)
        title = yt_video.title
        title.replace('/', '')

        # download the video
        download_video(yt_video, resolution, SAVE_PATH)

    return {
        # return video title and author
        "title": title,
    }


def download_video(yt_video, resolution, SAVE_PATH, yt_video_prefix=None):
    yt_video_title = yt_video.title
    # remove '/' and '\' from title
    yt_video_title = yt_video_title.replace("/", "")
    yt_video_title = yt_video_title.replace("\\", "")
    print(yt_video_title)

    # get youtube video object by resolution
    yt_video_object = yt_video.streams.get_by_resolution(resolution)

    # if not available the reqd resolution => get the highest resolution
    if (yt_video_object is None):
        yt_video_object = yt_video.streams.get_highest_resolution()

    try:
        saved_path = yt_video_object.download(
            SAVE_PATH, yt_video_title, yt_video_prefix)
        print("video saved in : " + saved_path)
    except:
        print("Error downloading the file...")
        raise Exception('Error downloading the video file')


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
