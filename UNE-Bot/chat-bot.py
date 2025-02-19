from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

# Token del bot
TOKEN = "7340871190:AAHHCJgbak61ui7ypZSnEhd63DN_Q07q5qg"

# Función para /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido al chatbot de la Empresa Eléctrica de La H! Escribe /help para ver las opciones disponibles.")

# Función para /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    Comandos disponibles:
    /start - Iniciar el bot
    /help - Mostrar esta ayuda
    /horario_apagon - Consultar horarios de apagón programado
    /reportar_falla - Reportar una falla eléctrica
    /facturacion - Información sobre facturación y pagos
    /sumar_uno [número] - Enviar un número y recibir ese número + 1
    /ultimas_notas [número] - Obtener las últimas X notas informativas
    /deficit [fecha] - Obtener el deficit de la fecha 
    """)

# Función para /horario_apagon
async def horario_apagon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los horarios de apagón programado varían según la región. Consulta el sitio web oficial de la UNE.")

# Función para /reportar_falla
async def reportar_falla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Para reportar una falla eléctrica, llama al número de emergencia 188 o visita el sitio web de la UNE.")

# Función para /facturacion
async def facturacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Puedes pagar tu factura en las oficinas de la UNE, bancos autorizados o mediante aplicaciones móviles.")

# Función para /sumar_uno
async def sumar_uno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        numero = float(context.args[0])  # Obtener el número ingresado después del comando
        resultado = numero + 1
        await update.message.reply_text(f"El número que me enviaste es: {numero}. Si le sumo 1, el resultado es: {resultado}")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido. Ejemplo: /sumar_uno 5")

# Función para /ultimas_notas
async def deficit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        x = int(context.args[0])  # Obtener el número de notas desde los argumentos del comando
        if x <= 0:
            raise ValueError()
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido de notas. Ejemplo: /ultimas_notas 5")
        return

    # Cargar el archivo JSON
    try:
        with open("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/data_nota_informativa.json", "r", encoding="utf-8") as file:
            datos = json.load(file)
    except FileNotFoundError:
        await update.message.reply_text("No se encontró el archivo de notas informativas.")
        return
    except json.JSONDecodeError:
        await update.message.reply_text("El archivo de notas informativas no tiene un formato válido.")
        return

    # Tomar las últimas X notas
    ultimas = list(datos.items())[:x]
    
    # Obtener chat_id
    chat_id = update.message.chat_id

    # Enviar cada nota como un mensaje separado
    for fecha, nota in ultimas:
        mensaje = f"- {fecha}: {nota[0]}" if nota else f"- {fecha}: (Sin información)"
        await context.bot.send_message(chat_id=chat_id, text=mensaje)
        
# Función para /ultimas_notas
async def ultimas_notas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        x = int(context.args[0])  # Obtener el número de notas desde los argumentos del comando
        if x <= 0:
            raise ValueError()
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido de notas. Ejemplo: /ultimas_notas 5")
        return

    # Cargar el archivo JSON
    try:
        with open("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/data_nota_informativa.json", "r", encoding="utf-8") as file:
            datos = json.load(file)
    except FileNotFoundError:
        await update.message.reply_text("No se encontró el archivo de notas informativas.")
        return
    except json.JSONDecodeError:
        await update.message.reply_text("El archivo de notas informativas no tiene un formato válido.")
        return

    # Tomar las últimas X notas
    ultimas = list(datos.items())[:x]
    
    # Obtener chat_id
    chat_id = update.message.chat_id

    # Enviar cada nota como un mensaje separado
    for fecha, nota in ultimas:
        mensaje = f"- {fecha}: {nota[0]}" if nota else f"- {fecha}: (Sin información)"
        await context.bot.send_message(chat_id=chat_id, text=mensaje)

# Función para mensajes desconocidos
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Lo siento, no entiendo ese comando. Escribe /help para ver las opciones disponibles.")

# Función principal para iniciar el bot
def main():
    # Crear la aplicación y pasarle el token
    application = Application.builder().token(TOKEN).build()

    # Registrar manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("horario_apagon", horario_apagon))
    application.add_handler(CommandHandler("reportar_falla", reportar_falla))
    application.add_handler(CommandHandler("facturacion", facturacion))
    application.add_handler(CommandHandler("sumar_uno", sumar_uno))
    application.add_handler(CommandHandler("ultimas_notas", ultimas_notas))

    # Registrar manejador para mensajes no reconocidos
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Iniciar el bot
    print("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling(timeout=10)

if __name__ == "__main__":
    main()
