import os

import requests
from flask import Flask, render_template, request
import cloudmusic


app = Flask(__name__, template_folder=os.path.abspath('.'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    searchtype=request.form["search_type"]
    keyword = request.form['keyword']
    count=request.form['count']
    songs = cloudmusic.search(keyword,count)
    if searchtype=='user':
        username = request.form['keyword']
        user_ids = getUserId(username)
        playlists = []
        for user_id in user_ids:
            User = cloudmusic.getUser(user_id)
            playlist = User.getPlaylist()

        return render_template('user.html', playlists=playlist)
    if searchtype=='song':
        return render_template('search_results.html', songs=songs)



@app.route('/play', methods=['POST'])
def play():
    song_url = request.form['song_url']
    artist = request.form['artist']
    album = request.form['album']
    picUrl = request.form['picUrl']
    song_id=request.form['song_id']
    music=cloudmusic.getMusic(song_id)
    lyric=None
    comment=music.getComments(20)
    try:
        lyric = music.getLyrics()
    except Exception as e:
        lyric = "纯音乐,暂无歌词"



    song = {
        "url": song_url,
        "artist": artist,
        "album": album,
        "picUrl": picUrl,
        "lyric": lyric,
        "Comment": comment
    }

    return render_template('play.html', song=song)


def getUserId(username):
    user_ids = []
    search_url = "https://music.163.com/api/search/get/web"
    params = {
        's': username,
        'type': 1002,
        'offset': 0,
        'limit': 10
    }
    response = requests.get(search_url, params=params)
    data = response.json()

    if "userprofiles" in data["result"]:
        profiles = data["result"]["userprofiles"]
        for profile in profiles:
            user_id = profile["userId"]
            user_ids.append(user_id)

    return user_ids[:5]


@app.route('/user/playList', methods=['POST'])
def userList():
    playlistId = request.form['playlistId']
    playlist = cloudmusic.getPlaylist(playlistId)
    print(type(playlist))
    return render_template('search_results.html', songs=playlist)


if __name__ == '__main__':
    app.run()
