import asyncio
import openai

server_ip = "192.168.1.106"
server_port = 1234

openai.api_key = "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"

async def handle_client(reader, writer):
    try:
        message = (await reader.read(2048)).decode()
        addr = writer.get_extra_info('peername')
        print(f"Сообщение от клиента {addr}: {message}")

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=2048
        )

        model_response = response.choices[0].text.strip()
        print("Ответ от OpenAI:", model_response)

        writer.write(model_response.encode())
        await writer.drain()

    finally:
        writer.close()

async def start_server():
    server = await asyncio.start_server(handle_client, server_ip, server_port)
    print("Сервер слушает на {}:{}".format(server_ip, server_port))

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_server())
