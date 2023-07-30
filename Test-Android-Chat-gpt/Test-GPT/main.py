import sys
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import asyncio
from functools import partial


class Container(GridLayout):
    server_ip = "94.241.40.84"
    server_port = 80

    label_w = ObjectProperty()
    text_input_w = ObjectProperty()
    button_send_w = ObjectProperty()

    def on_text_change(self, text):
        self.button_send_w.disabled = not text.strip()

    def send_message_async(self, *args):
        message = self.text_input_w.text
        self.text_input_w.text = ""

        if not message.strip():
            self.update_response("Ошибка: Пустой текст сообщения")
            return

        loading_popup = Popup(title="ЗАГРУЗКА", content=ProgressBar(max=10), size_hint=(0.3, 0.1),
                              background_color=(0, 0, 0))
        loading_popup.open()

        Window.disabled = True

        async def send_message_async_wrap():
            try:
                reader, writer = await asyncio.open_connection(self.server_ip, self.server_port)
                writer.write(message.encode())
                await writer.drain()
                response = await reader.read(4096)
                self.update_response(response.decode())
                writer.close()

            except OSError as e:
                self.update_response("Ошибка при подключении к серверу: " + str(e))

            loading_popup.dismiss()
            Window.disabled = False

        asyncio.create_task(send_message_async_wrap())

    def update_response(self, response):
        self.label_w.text = response


class ClientApp(MDApp):
    def build(self):
        return Container()


if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)
    ClientApp().run()
