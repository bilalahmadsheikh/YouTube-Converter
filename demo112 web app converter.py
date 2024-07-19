from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube, Playlist
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['youtube_url']
        download_type = request.form['download_type']
        try:
            if download_type == 'mp4':
                download_mp4(url)
            elif download_type == 'mp3':
                download_mp3(url)
            elif download_type == 'playlist':
                download_playlist(url)
        except Exception as e:
            flash(f"An error occurred: {e}", 'error')
        return redirect(url_for('index'))
    return render_template('web.html')

def download_mp4(url):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path='downloads')
    flash(f"Downloaded: {yt.title} (MP4)", 'success')

def download_mp3(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    out_file = stream.download(output_path='downloads')
    base, ext = os.path.splitext(out_file)
    new_file = os.path.join('downloads', f"{yt.title}.mp3")
    os.rename(out_file, new_file)
    flash(f"Downloaded: {yt.title} (MP3)", 'success')

def download_playlist(url):
    playlist = Playlist(url)
    for video in playlist.videos:
        stream = video.streams.get_highest_resolution()
        stream.download(output_path='downloads')
    flash(f"Downloaded: {playlist.title} (Playlist)", 'success')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
