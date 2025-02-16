import os
import sys
import yt_dlp
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window

class YtDownloader(App):
    def build(self):
        self.title = "YouTube to MP3 Downloader"
        self.configure_window()

        root_layout = AnchorLayout()

        # Use relative path for image
        image_path = os.path.join(self.get_base_path(), "logo.jpg")
        backdrop = Image(source=image_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        root_layout.add_widget(backdrop)

        # Box Layout for UI Elements
        content_layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20, size_hint=(0.8, 0.6))

        # Input Field
        self.label = Label(text="Enter the YouTube link below:", font_size='24sp', size_hint_y=None, height=40)
        content_layout.add_widget(self.label)

        self.url_input = TextInput(font_size='18sp', size_hint_y=None, height=50, multiline=False)
        content_layout.add_widget(self.url_input)

        # Download Buttons
        button_layout = BoxLayout(padding=10, spacing=10, size_hint_y=None, height=60)

        self.mp3_button = Button(text="Download MP3", font_size='16sp', size_hint=(0.5, 1), background_color=(0.2, 0.6, 0.8, 1))
        self.mp3_button.bind(on_press=self.download_mp3)
        button_layout.add_widget(self.mp3_button)

        self.playlist_button = Button(text="Download Playlist", font_size='16sp', size_hint=(0.5, 1), background_color=(0.2, 0.6, 0.8, 1))
        self.playlist_button.bind(on_press=self.download_playlist)
        button_layout.add_widget(self.playlist_button)

        content_layout.add_widget(button_layout)

        # Set Default Download Path
        base_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        self.download_path = os.path.join(base_downloads, "MP3 Converter Downloads")

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)  # Create folder if it doesn't exist

        root_layout.add_widget(content_layout)
        return root_layout

    def configure_window(self):
        Window.size = (800, 800)
        Window.minimum_width = 400
        Window.minimum_height = 700

    def get_base_path(self):
        """ Get correct path whether running as script or packaged EXE """
        if getattr(sys, 'frozen', False):  # Running as an EXE
            return sys._MEIPASS
        return os.path.dirname(__file__)

    def get_ffmpeg_path(self):
        """ Get correct ffmpeg path for both script and packaged EXE """
        return os.path.join(self.get_base_path(), "ffmpeg.exe")

    def download_mp3(self, _):
        url = self.url_input.text.strip()
        if not url:
            self.show_popup("Error", "Please enter a YouTube URL")
            return

        self.show_popup("Downloading", "Downloading MP3... Please wait.")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s').replace("\\", "/"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': self.get_ffmpeg_path(),
            'ignoreerrors': True,
            'postprocessor_args': ['-loglevel', 'error'],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                
                if 'requested_downloads' in info_dict:
                    file_path = info_dict['requested_downloads'][0]['filepath']
                else:
                    file_path = ydl.prepare_filename(info_dict)

                # Convert to MP3 or fallback to original file
                mp3_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")
                if os.path.exists(mp3_path):
                    self.show_popup("Success", f"Download completed!\nSaved to: {mp3_path}")
                else:
                    self.show_popup("Warning", f"MP3 conversion failed!\nSaved as: {file_path}")

        except Exception as e:
            self.show_popup("Error", f"Download failed!\n{str(e)}")

    def download_playlist(self, _):
        url = self.url_input.text.strip()
        if not url:
            self.show_popup("Error", "Please enter a YouTube Playlist URL")
            return

        self.show_popup("Downloading", "Downloading Playlist... Please wait.")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': self.get_ffmpeg_path(),
            'ignoreerrors': True,
            'postprocessor_args': ['-loglevel', 'error'],
            'yes_playlist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)

                downloaded_files = []
                for entry in info_dict.get("entries", []):
                    if entry:
                        if 'requested_downloads' in entry:
                            file_path = entry['requested_downloads'][0]['filepath']
                        else:
                            file_path = ydl.prepare_filename(entry)
                        
                        mp3_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")
                        downloaded_files.append(mp3_path if os.path.exists(mp3_path) else file_path)

                if downloaded_files:
                    file_list = "\n".join(downloaded_files[:5])  # Show first 5 files
                    self.show_popup("Success", f"Playlist downloaded successfully!\nSaved files:\n{file_list}")
                else:
                    self.show_popup("Error", "No files were downloaded.")

        except Exception as e:
            self.show_popup("Error", f"Download failed!\n{str(e)}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, font_size='16sp'), size_hint=(None, None), size=(400, 250))
        popup.open()

if __name__ == "__main__":
    YtDownloader().run()
