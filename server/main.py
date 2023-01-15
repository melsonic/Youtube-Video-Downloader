from flask import Flask, request
from pytube import YouTube
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

    ytvideo = YouTube(url)
    title = ytvideo.title

    # get youtube video object by resolution
    ytvideoObject = ytvideo.streams.get_by_resolution(resolution)

    # if not available the requested resolution => get the highest resolution
    if (ytvideoObject == None):
        ytvideoObject = ytvideo.streams.get_highest_resolution()


    # download the file
    try:
        saved_path = ytvideoObject.download(SAVE_PATH, title)
        print('video saved in : ' + saved_path)
    except:
        print("Error downloading the file...")

    return {
        # return video title, thumbnail url and author
        "title": ytvideo.title,
        "thumbnail": ytvideo.thumbnail_url,
        "author": ytvideo.author,
    }


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
