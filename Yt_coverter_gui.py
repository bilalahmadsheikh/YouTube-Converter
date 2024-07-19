import tkinter as tk
import tkinter.messagebox as tmsg
from pytube import YouTube, Playlist
import os
from tkinter import ttk
from ttkthemes import ThemedStyle

class YtDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("720x600")
        self.maxsize(1080, 720)
        self.minsize(720, 600)
        self.title("YT Downloader")

        # Themed style
        style = ThemedStyle(self)
        style.set_theme("blue")  # Choosing a theme (e.g., "arc", "equilux", "plastik")

        # Main frame with background color
        self.main_frame = ttk.Frame(self, padding=(30, 20), style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Decorative shapes and colors
        self.create_shapes()

        # Header Section
        subtitle_label = ttk.Label(self.main_frame, text="Enter the YouTube link below:", font=("Helvetica", 16), style="Subtitle.TLabel")
        subtitle_label.pack(pady=20)

        # Input Section
        self.y = tk.StringVar()
        entry = ttk.Entry(self.main_frame, textvariable=self.y, font=("Helvetica", 14), width=50)
        entry.pack(ipady=8, pady=10)

        # Button Section
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        mp4_button = ttk.Button(button_frame, text="Download MP4", command=self.download_mp4, style="MP4.TButton")
        mp4_button.pack(side=tk.LEFT, padx=10)

        mp3_button = ttk.Button(button_frame, text="Download MP3", command=self.download_mp3, style="MP3.TButton")
        mp3_button.pack(side=tk.LEFT, padx=10)

        playlist_button = ttk.Button(button_frame, text="Download Playlist", command=self.download_playlist, style="Playlist.TButton")
        playlist_button.pack(side=tk.LEFT, padx=10)

    def create_shapes(self):
        self.canvas = tk.Canvas(self.main_frame, width=720, height=150)
        self.canvas.pack(fill=tk.BOTH, pady=(0, 20))  # Fill horizontally and give some bottom padding

        # Draw a filled rectangle to cover the canvas
        self.rect = self.canvas.create_rectangle(0, 0, 1080, 150, fill="#f9BF45", outline="")

        # Draw an oval
        self.oval = self.canvas.create_oval(100, 20, 620, 120, fill="#e74c3c")

        # Add YT Downloader label in the middle of the oval
        self.label = self.canvas.create_text(360, 70, text="YT Downloader", font=("Helvetica", 30, "bold"), fill="white")

        # Bind the <Configure> event to resize shapes
        self.canvas.bind("<Configure>", self.resize_shapes)

    def resize_shapes(self, event):
        canvas_width = event.width
        canvas_height = event.height

        # Resize the rectangle to cover the entire canvas
        self.canvas.coords(self.rect, 0, 0, canvas_width, 150)

        # Resize the oval
        self.canvas.coords(self.oval, canvas_width * 0.1, 20, canvas_width * 0.9, 120)

        # Calculate the center coordinates for the label
        oval_center_x = (canvas_width * 0.1 + canvas_width * 0.9) / 2
        oval_center_y = (20 + 120) / 2

        # Move the label to the center of the oval
        self.canvas.coords(self.label, oval_center_x, oval_center_y)

    def download_mp4(self):
        url = self.y.get()
        if url:
            try:
                yt = YouTube(url)
                stream = yt.streams.get_highest_resolution()
                stream.download()
                tmsg.showinfo("Success", f"Downloaded: {yt.title} (MP4)")
            except Exception as e:
                tmsg.showerror("Error", f"An error occurred: {e}")
        else:
            tmsg.showwarning("Warning", "Please enter a URL")

    def download_mp3(self):
        url = self.y.get()
        if url:
            try:
                yt = YouTube(url)
                stream = yt.streams.filter(only_audio=True).first()
                out_file = stream.download()
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                tmsg.showinfo("Success", f"Downloaded: {yt.title} (MP3)")
            except Exception as e:
                tmsg.showerror("Error", f"An error occurred: {e}")
        else:
            tmsg.showwarning("Warning", "Please enter a URL")

    def download_playlist(self):
        url = self.y.get()
        if url:
            try:
                playlist = Playlist(url)
                for video in playlist.videos:
                    stream = video.streams.get_highest_resolution()
                    stream.download()
                tmsg.showinfo("Success", f"Downloaded: {playlist.title} (Playlist)")
            except Exception as e:
                tmsg.showerror("Error", f"An error occurred: {e}")
        else:
            tmsg.showwarning("Warning", "Please enter a URL")

if __name__ == "__main__":
    app = YtDownloader()
    app.mainloop()
