# 04 - Chat server (versione semplice)
# Ogni messaggio ricevuto da un client viene inoltrato a tutti gli altri.

import asyncio
import random

led_status = False

async def gestisci_client(reader, writer):
    ip, porta = writer.get_extra_info("peername")
    nome = f"{ip}:{porta}"
    print(nome, "è entrato")

    try:
        while True:
            dati = await reader.readline()
            if not dati:
                break

            comando = dati.decode().strip()
            temp = round(random.uniform(18.0, 26.0), 1)
            umidita = round(random.uniform(40.0, 65.0), 1)

            if comando == "TEMP":
                risposta = f"OK {temp} C\n"

            elif comando == "UMIDITA":
                risposta = f"OK {umidita} C\n"

            elif comando == "LED ON":
                led_status = True

            elif comando == "LED OFF":
                led_status = False

            elif comando == "STATO":
                risposta = f"OK, Temperatura: {temp}, Umidità: {umidita}, Led_Status: {led_status} C\n"

            elif comando == "QUIT":
                break
    except ConnectionError:
        pass                                 # il client è caduto all'improvviso
    finally:
        print(nome, "è uscito")
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(gestisci_client, "127.0.0.1", 8888)
    print("Chat in ascolto sulla porta 8888")
    async with server:
        await server.serve_forever()


asyncio.run(main())