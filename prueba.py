from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os
from dotenv import load_dotenv
from transformers import pipeline

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Verificar que el TOKEN esté definido
if not TOKEN:
    raise ValueError("El TOKEN del bot no está definido en el archivo .env")

# Cargar modelo de lenguaje de manera diferida
def generar_respuesta(prompt):
    chatbot_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")
    respuesta = chatbot_model(prompt, max_length=100, do_sample=True)
    return respuesta[0]['generated_text']

# Función para leer JSON
def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

# Función para /deficit con LM
async def deficit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        fecha_parcial = context.args[0]
    except IndexError:
        await update.message.reply_text("Por favor, proporciona una fecha válida. Ejemplo: /deficit 2025-02 o /deficit 2025-02-16")
        return

    datos = cargar_json("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/data_deficit.json")
    if datos is None:
        await update.message.reply_text("No se pudo cargar el archivo de déficit.")
        return

    chat_id = update.effective_chat.id
    coincidencias = {fecha: valor for fecha, valor in datos.items() if fecha_parcial in fecha}

    if coincidencias:
        for fecha, valor in coincidencias.items():
            prompt = f"Genera un mensaje informativo sobre el déficit eléctrico para la fecha {fecha}. El déficit registrado fue de {valor}MW."
            mensaje = generar_respuesta(prompt)
            await context.bot.send_message(chat_id=chat_id, text=mensaje)
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"No hay información de déficit para la fecha {fecha_parcial}.")

# Función para /ultimas_notas con LM
async def ultimas_notas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        x = int(context.args[0])
        if x <= 0:
            raise ValueError()
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido de notas. Ejemplo: /ultimas_notas 5")
        return

    datos = cargar_json("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/data_deficit.json")
    if datos is None:
        await update.message.reply_text("No se pudo cargar el archivo de notas informativas.")
        return

    chat_id = update.effective_chat.id
    notas = list(datos.items())[:x]

    if not notas:
        await context.bot.send_message(chat_id=chat_id, text="No hay notas informativas disponibles.")
        return

    for fecha, nota in notas:
        prompt = f"Genera un mensaje informativo basado en la siguiente nota: {nota}. La fecha es {fecha}."
        mensaje = generar_respuesta(prompt)
        await context.bot.send_message(chat_id=chat_id, text=mensaje)

# Función principal para iniciar el bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("deficit", deficit))
    application.add_handler(CommandHandler("ultimas_notas", ultimas_notas))

    print("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling(timeout=10)

if __name__ == "__main__":
    main()







###########################################################################################vvv







from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os
from dotenv import load_dotenv
from transformers import pipeline

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Cargar modelo de lenguaje
chatbot_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Función para generar respuesta con el LM
def generar_respuesta(prompt):
    respuesta = chatbot_model(prompt, max_length=100, do_sample=True)
    return respuesta[0]['generated_text']

# Función para cargar JSON
def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Clasificación de intención con LM
def clasificar_intencion(mensaje):
    prompt = f"¿Qué tipo de solicitud es esta? Clasifícala como: 'horario_apagon', 'facturacion', 'reportar_falla', 'deficit' o 'desconocido'. Mensaje: {mensaje}"
    respuesta = chatbot_model(prompt, max_length=20, do_sample=True)
    return respuesta[0]['generated_text'].strip().lower()

# Función para /deficit con LM
async def deficit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        fecha_parcial = context.args[0]
    except IndexError:
        await update.message.reply_text("Por favor, proporciona una fecha válida. Ejemplo: /deficit 2025-02 o /deficit 2025-02-16")
        return

    datos = cargar_json("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/data_deficit.json")
    if datos is None:
        await update.message.reply_text("No se pudo cargar el archivo de déficit.")
        return

    chat_id = update.effective_chat.id
    coincidencias = {fecha: valor for fecha, valor in datos.items() if fecha_parcial in fecha}

    if coincidencias:
        for fecha, valor in coincidencias.items():
            prompt = f"Genera un mensaje informativo sobre el déficit eléctrico para la fecha {fecha}. El déficit registrado fue de {valor}MW."
            mensaje = generar_respuesta(prompt)
            await context.bot.send_message(chat_id=chat_id, text=mensaje)
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"No hay información de déficit para la fecha {fecha_parcial}.")

# Función para /ultimas_notas con LM
async def ultimas_notas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        x = int(context.args[0])
        if x <= 0:
            raise ValueError()
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido de notas. Ejemplo: /ultimas_notas 5")
        return

    datos = cargar_json("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/data_deficit.json")
    if datos is None:
        await update.message.reply_text("No se pudo cargar el archivo de notas informativas.")
        return

    chat_id = update.effective_chat.id
    notas = list(datos.items())[:x]

    if not notas:
        await context.bot.send_message(chat_id=chat_id, text="No hay notas informativas disponibles.")
        return

    for fecha, nota in notas:
        prompt = f"Genera un mensaje informativo basado en la siguiente nota: {nota}. La fecha es {fecha}."
        mensaje = generar_respuesta(prompt)
        await context.bot.send_message(chat_id=chat_id, text=mensaje)

# Función para procesar mensajes de texto y detectar intención
async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text
    intencion = clasificar_intencion(mensaje_usuario)

    if "horario_apagon" in intencion:
        await update.message.reply_text("La consulta sobre horarios de apagón está en desarrollo.")
    elif "facturacion" in intencion:
        await update.message.reply_text("La consulta sobre facturación está en desarrollo.")
    elif "reportar_falla" in intencion:
        await update.message.reply_text("Para reportar una falla eléctrica, comuníquese con la empresa.")
    elif "deficit" in intencion:
        await deficit(update, context)
    else:
        await update.message.reply_text("No entiendo tu pregunta. Escribe /help para ver opciones.")

# Función principal para iniciar el bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("deficit", deficit))
    application.add_handler(CommandHandler("ultimas_notas", ultimas_notas))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))

    print("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling(timeout=10)

if __name__ == "__main__":
    main()



###########################################################################################vvv
def clasificar_intencion(mensaje):
    prompt = f"¿Qué tipo de solicitud es esta? Clasifícala como: 'horario_apagon', 'facturacion', 'reportar_falla', 'deficit' o 'desconocido'. Mensaje: {mensaje}"
    respuesta = chatbot_model(prompt, max_length=20, do_sample=True)
    return respuesta[0]['generated_text'].strip().lower()

async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text
    intencion = clasificar_intencion(mensaje_usuario)

    if "horario_apagon" in intencion:
        await horario_apagon(update, context)
    elif "facturacion" in intencion:
        await facturacion(update, context)
    elif "reportar_falla" in intencion:
        await reportar_falla(update, context)
    elif "deficit" in intencion:
        await deficit(update, context)
    else:
        await update.message.reply_text("No entiendo tu pregunta. Escribe /help para ver opciones.")

# Registrar el manejador
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))
