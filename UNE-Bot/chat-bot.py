import json
import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# API Key de Hugging Face (reemplaza con tu clave)
HUGGINGFACE_API_KEY = "TU_API_KEY"

# Modelo a usar en Hugging Face
HUGGINGFACE_MODEL = "mistralai/Mistral-7B"

# Cargar la base de datos solo con municipios de La Habana
with open("datos_electricos.json", "r", encoding="utf-8") as f:
    datos_db = json.load(f)

# Lista de municipios de La Habana
municipios_habana = [municipio.lower() for municipio in datos_db.keys()]

# Verifica si la consulta es válida (relacionada con apagones en La Habana)
def es_consulta_valida(consulta):
    palabras_clave = ["apagón", "corte", "déficit", "electricidad", "afectación", "energía"]
    return any(palabra in consulta.lower() for palabra in palabras_clave) or \
           any(municipio in consulta.lower() for municipio in municipios_habana)

# Obtiene datos del municipio si está en la base de datos
def obtener_datos_relevantes(consulta):
    for municipio, info in datos_db.items():
        if municipio.lower() in consulta.lower():
            return f"Municipio: {municipio}\nDéficit actual: {info['déficit']}\nEstado de apagones: {info['apagones']}"
    return None

# Consulta la API de Hugging Face para generar respuestas
def consulta_huggingface(mensaje):
    url = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    data = {"inputs": mensaje}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return "Error al obtener respuesta de la IA."

# Comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bienvenido al asistente eléctrico de La Habana. Pregunta sobre apagones o déficit en cualquier municipio.")

# Manejo de mensajes
def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text

    if not es_consulta_valida(user_text):
        update.message.reply_text("Solo tengo información sobre apagones y déficit eléctrico en los municipios de La Habana.")
        return

    datos_relevantes = obtener_datos_relevantes(user_text)
    if datos_relevantes is None:
        update.message.reply_text("No tengo información sobre ese municipio en La Habana.")
        return

    # Construcción del mensaje para la IA
    prompt = f"Basándote solo en esta información, responde de forma clara y concisa:\n\n{datos_relevantes}"
    respuesta = consulta_huggingface(prompt)

    update.message.reply_text(respuesta)

# Función principal para iniciar el bot
def main():
    updater = Updater("TU_TOKEN_DE_TELEGRAM", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
