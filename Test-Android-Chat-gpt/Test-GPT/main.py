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
    
    
    #  значения идут из сlient.kv
    # values are going from сlient.kv
    label_w = ObjectProperty()
    text_input_w = ObjectProperty()
    button_send_w = ObjectProperty()
    # text_input_readonly_w = ObjectProperty()



   

    
    

     # checking for empty message
    def on_text_change(self, text):
        if len(text.strip()) == 0 or text.isspace():
            self.button_send_w.disabled = True
        else:
            self.button_send_w.disabled = False


    # func for send message to server
    def send_message_async(self, *args):


        message = self.text_input_w.text
        self.text_input_w.text = ""

         # Проверка на пустой текст сообщения
        if not message.strip():
            self.update_response("Ошибка: Пустой текст сообщения")
            return

        # Здесь нужно указать IP-адрес и порт сервера
        server_ip = "94.241.40.84"
        server_port = 80

        # Отображение модального окна с индикатором загрузки
        loading_popup = Popup(title="ЗАГРУЗКА", content=ProgressBar(max=10), size_hint=(0.3, 0.1),
                              background_color=(0,0,0))
        loading_popup.open()

        # Отключение пользовательского ввода
        Window.disabled = True

        # Обертка функции async в обычную функцию
        def send_message_sync(*args):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Обертка send_message_async для работы с новым event loop
            async def send_message_async_wrap():
                try:
                    reader, writer = await asyncio.open_connection(server_ip, server_port)
                    writer.write(message.encode())
                    await writer.drain()

                    response = await reader.read(1024)
                    self.update_response(response.decode())

                    writer.close()

                except OSError as e:
                    self.update_response("Ошибка при подключении к серверу: " + str(e))

                # Закрытие модального окна и включение пользовательского ввода
                loading_popup.dismiss()
                Window.disabled = False

            loop.run_until_complete(send_message_async_wrap())
            loop.close()

        # Запуск обернутой функции async через Clock
        Clock.schedule_once(partial(send_message_sync), 0)

    def update_response(self, response):
        self.label_w.text = response
        


class ClientApp(MDApp):
    def build(self):
        return Container()


if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)  # Цвет фона окна
    ClientApp().run()
