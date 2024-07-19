#add your own path for backdrop
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.modalview import ModalView
from kivy.utils import get_color_from_hex
from pytube import YouTube, Playlist
import os

class YtDownloader(App):
    def build(self):
        self.title = "YT Downloader"
        self.configure_window()

        # Root layout with an image as the background
        root_layout = AnchorLayout()

        # Image as backdrop
        backdrop = Image(source="C:/Users/bilaa/Downloads/logo.jpg", size_hint=(1, 1),allow_stretch=True, keep_ratio=False)
        root_layout.add_widget(backdrop)

        # BoxLayout for content
        content_layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, 0.6))

        # Interface components
        self.label = Label(text="Enter the YouTube link below:", font_size=24, size_hint_y=None, height=40)
        content_layout.add_widget(self.label)

        self.url_input = TextInput(font_size=18, size_hint_y=None, height=50, multiline=False)
        content_layout.add_widget(self.url_input)

        self.path_button = Button(text="Select Download Path", font_size=16, size_hint_y=None, height=50,
                                  background_color=get_color_from_hex('#FFD700'))
        self.path_button.bind(on_press=self.open_file_chooser)
        content_layout.add_widget(self.path_button)

        button_layout = BoxLayout(padding=10, spacing=10, size_hint_y=None, height=60)

        self.mp4_button = Button(text="Download MP4", font_size=16, size_hint=(None, None), size=(120, 50),
                                 background_color=get_color_from_hex('#FF6347'))
        self.mp4_button.bind(on_press=self.download_mp4)
        button_layout.add_widget(self.mp4_button)

        self.mp3_button = Button(text="Download MP3", font_size=16, size_hint=(None, None), size=(120, 50),
                                 background_color=get_color_from_hex('#32CD32'))
        self.mp3_button.bind(on_press=self.download_mp3)
        button_layout.add_widget(self.mp3_button)

        self.playlist_button = Button(text="Download Playlist", font_size=14, size_hint=(None, None), size=(120, 50),
                                      background_color=get_color_from_hex('#1E90FF'))
        self.playlist_button.bind(on_press=self.download_playlist)
        button_layout.add_widget(self.playlist_button)

        content_layout.add_widget(button_layout)

        # Set default download path to the user's home directory
        home_dir = os.path.expanduser("~")
        self.download_path = os.path.join(home_dir, "YT_downloads")
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        self.path_button.text = f"Path: {self.download_path}"

        # Add the content layout to the root layout with centered position
        root_layout.add_widget(content_layout)

        return root_layout

    def configure_window(self):
        Window.size = (800, 800)
        Window.minimum_width = 400
        Window.minimum_height = 700

    def open_file_chooser(self, instance):
        self.file_chooser_view = ModalView(size_hint=(0.8, 0.8))
        file_chooser = FileChooserListView(path=self.download_path, filters=['*'], dirselect=True)
        file_chooser.bind(on_selection=self.select_path)
        box = BoxLayout(orientation='vertical')
        box.add_widget(file_chooser)
        box.add_widget(Button(text='Select', size_hint_y=None, height=50, on_press=self.file_chooser_view.dismiss))
        self.file_chooser_view.add_widget(box)
        self.file_chooser_view.open()

    def select_path(self, filechooser, selection):
        if selection:
            self.download_path = selection[0]
            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path)
            self.path_button.text = f"Path: {self.download_path}"

    def download_mp4(self, instance):
        url = self.url_input.text.strip()
        if url and self.download_path:
            try:
                yt = YouTube(url)
                stream = yt.streams.get_highest_resolution()
                stream.download(output_path=self.download_path)
                self.show_popup("Success", f"Downloaded:\n{yt.title} (MP4)")
            except Exception as e:
                self.show_popup("Error", f"An error occurred: {e}")
        else:
            self.show_popup("Warning", "Please enter both a URL and select a download path")

    def download_mp3(self, instance):
        url = self.url_input.text.strip()
        if url and self.download_path:
            try:
                yt = YouTube(url)
                stream = yt.streams.filter(only_audio=True).first()
                out_file = stream.download(output_path=self.download_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                self.show_popup("Success", f"Downloaded:\n{yt.title} (MP3)")
            except Exception as e:
                self.show_popup("Error", f"An error occurred: {e}")
        else:
            self.show_popup("Warning", "Please enter both a URL and select a download path")

    def download_playlist(self, instance):
        url = self.url_input.text.strip()
        if url and self.download_path:
            try:
                playlist = Playlist(url)
                for video in playlist.videos:
                    stream = video.streams.get_highest_resolution()
                    stream.download(output_path=self.download_path)
                self.show_popup("Success", f"Downloaded: \n{playlist.title} (Playlist)")
            except Exception as e:
                self.show_popup("Error", f"An error occurred: {e}")
        else:
            self.show_popup("Warning", "Please enter both a URL and select a download path")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, font_size=16), size_hint=(None, None), size=(300, 200))
        popup.open()

if __name__ == "__main__":
    YtDownloader().run()
