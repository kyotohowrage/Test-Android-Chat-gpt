from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import asyncio
from functools import partial


class ClientApp(App):
    def build(self):
        layout = GridLayout(cols=1)

        question_label = Label(text="ChatGPT - OpenAI", size_hint=(0.5, None))
        layout.add_widget(question_label)

        self.message_input = TextInput()
        self.message_input.hint_text = "Задайте свой вопрос:"  # Добавленная надпись
        layout.add_widget(self.message_input)

        send_button = Button(text="ОТПРАВИТЬ", on_press=self.send_message_async,
                             background_color=(0.3, 0.9, 0.3, 1),
                             background_normal='',
                             size_hint=(0.5, None))
        layout.add_widget(send_button)

        self.response_input = TextInput(readonly=True)
        self.response_input.hint_text = "ChatGPT:"  # Добавленная надпись
        layout.add_widget(self.response_input)

        return layout


    def send_message_async(self, *args):
        message = self.message_input.text
        self.message_input.text = ""

        # Здесь нужно указать IP-адрес и порт сервера
        server_ip = "94.241.40.84"
        server_port = 80

        # Обертка функции async в обычную функцию
        def send_message_sync(*args):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Обертка send_message_async для работы с новым event loop
            async def send_message_async_wrap():
                reader, writer = await asyncio.open_connection(server_ip, server_port)
                writer.write(message.encode())
                await writer.drain()

                response = await reader.read(1024)
                self.update_response(response.decode())

                writer.close()

            loop.run_until_complete(send_message_async_wrap())
            loop.close()

        # Запуск обернутой функции async через Clock
        Clock.schedule_once(partial(send_message_sync), 0)

    def update_response(self, response):
        self.response_input.text = response


if __name__ == "__main__":
    ClientApp().run()