import os
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

import yt_dlp


class Downloader(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=20,
            spacing=12,
            **kwargs
        )

        self.app_folder = App.get_running_app().user_data_dir
        self.download_folder = os.path.join(
            self.app_folder,
            "downloads"
        )

        os.makedirs(self.download_folder, exist_ok=True)

        self.url = TextInput(
            hint_text="لینک ویدئو",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.url)

        self.quality = Spinner(
            text="360p",
            values=("360p", "480p", "720p"),
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.quality)

        self.download_button = Button(
            text="دانلود",
            size_hint_y=None,
            height=50
        )
        self.download_button.bind(
            on_press=self.start_download
        )
        self.add_widget(self.download_button)

        self.delete_button = Button(
            text="حذف فایل‌های دانلودشده",
            size_hint_y=None,
            height=50
        )
        self.delete_button.bind(
            on_press=self.delete_downloads
        )
        self.add_widget(self.delete_button)

        self.status = Label(
            text="آماده",
            halign="center"
        )
        self.add_widget(self.status)

    def set_status(self, text):
        Clock.schedule_once(
            lambda dt: setattr(self.status, "text", text)
        )

    def start_download(self, instance):

        url = self.url.text.strip()

        if not url:
            self.status.text = "لطفاً لینک را وارد کنید."
            return

        self.download_button.disabled = True
        self.status.text = "در حال دانلود..."

        threading.Thread(
            target=self.download_video,
            args=(url, self.quality.text),
            daemon=True
        ).start()

    def download_video(self, url, quality):

        formats = {
            "360p":
                "bestvideo[height<=360]+bestaudio/"
                "best[height<=360]",

            "480p":
                "bestvideo[height<=480]+bestaudio/"
                "best[height<=480]",

            "720p":
                "bestvideo[height<=720]+bestaudio/"
                "best[height<=720]"
        }

        options = {
            "format": formats[quality],

            "outtmpl": os.path.join(
                self.download_folder,
                "%(title)s.%(ext)s"
            ),

            "merge_output_format": "mp4",

            "noplaylist": True
        }

        try:

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])

            self.set_status(
                "دانلود شد و در پوشه خصوصی برنامه قرار گرفت."
            )

        except Exception as e:

            self.set_status(
                "خطا در دانلود"
            )

        finally:

            Clock.schedule_once(
                lambda dt: setattr(
                    self.download_button,
                    "disabled",
                    False
                )
            )

    def delete_downloads(self, instance):

        deleted = 0

        for filename in os.listdir(self.download_folder):

            path = os.path.join(
                self.download_folder,
                filename
            )

            if os.path.isfile(path):

                try:
                    os.remove(path)
                    deleted += 1

                except OSError:
                    pass

        self.status.text = (
            f"{deleted} فایل حذف شد."
        )


class VideoDownloaderApp(App):

    def build(self):
        return Downloader()


if __name__ == "__main__":
    VideoDownloaderApp().run()