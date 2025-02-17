
import re
from telethon.sync import TelegramClient
import json
from datetime import datetime

# API de Telegram (reemplaza con tus credenciales)
api_id = 28690849  
api_hash = '31a5c394f60b37681f07e11599186516'  

# Nombre del canal
channel = 'electricamayabeque'

# Diccionario para almacenar los mensajes
json_ofice = {}

async def scrape_text_messages_only():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Obtener los mensajes del canal
        messages = await client.get_messages(channel, limit=None)  # Ajusta el límite según sea necesario

        # Iterar sobre los mensajes y filtrar solo texto
        for message in messages:
            if message.text and message.media is None:  # Solo texto sin multimedia
                msg_id = message.id
                texto_mensaje = message.text.strip()  # Elimina espacios en blanco extra
                print(texto_mensaje)  # 
                print(message.text)
                if re.search(r"Nota Informativa", message.text, re.IGNORECASE):  
                    patrones = [r"máxima afectación fue de (\d+[\.,]?\d*)",   
                               r"afectación máxima de (\d+[\.,]?\d*)"]
                    for patron in patrones:
                        match = re.search(patron, message.text,re.IGNORECASE)
                        if match:   # Extrae solo el número
                            json_ofice[msg_id] = {
                        "fecha": message.date.strftime('%Y-%m-%d %H:%M:%S'),  # Fecha en formato legible
                        "texto": match.group(1)
                         }

        with open('data_afectacion.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_ofice, json_file, indent=4, ensure_ascii=False)

# Ejecutar la función asíncrona
import asyncio
asyncio.run(scrape_text_messages_only())

print("✅ Datos guardados en 'data.json'")
