from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

# Función para manejar el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido al chatbot de la Empresa Eléctrica de La H! Escribe /help para ver las opciones disponibles.")

# Función para manejar el comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    Comandos disponibles:
    /start - Iniciar el bot
    /help - Mostrar esta ayuda
    /horario_apagon - Consultar horarios de apagón programado
    /reportar_falla - Reportar una falla eléctrica
    /facturacion - Información sobre facturación y pagos
    /sumar_uno - Enviar un número y recibir ese número + 1
    /ultimas_notas - Obtener las últimas X notas informativas (envía un número después del comando)
    """)

# Función para manejar el comando /horario_apagon
async def horario_apagon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los horarios de apagón programado varían según la región. Consulta el sitio web oficial de la UNE.")

# Función para manejar el comando /reportar_falla
async def reportar_falla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Para reportar una falla eléctrica, llama al número de emergencia 188 o visita el sitio web de la UNE.")

# Función para manejar el comando /facturacion
async def facturacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Puedes pagar tu factura en las oficinas de la UNE, bancos autorizados o mediante aplicaciones móviles.")

# Función para manejar mensajes de texto no reconocidos
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Lo siento, no entiendo ese comando. Escribe /help para ver las opciones disponibles.")

# Función para manejar el comando /sumar_uno
async def sumar_uno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pedir al usuario que envíe un número
    await update.message.reply_text("Por favor, envíame un número y te devolveré ese número + 1.")
    # Guardar el estado para esperar la respuesta del usuario
    context.user_data['esperando_numero'] = True

# Función para manejar la respuesta del usuario
async def handle_numero_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('esperando_numero'):
        try:
            # Intentar convertir el mensaje del usuario a un número
            user_input = update.message.text
            numero = float(user_input)  # Convertir a número decimal
            resultado = numero + 1  # Sumar 1 al número
            await update.message.reply_text(f"El número que me enviaste es: {numero}. Si le sumo 1, el resultado es: {resultado}")
        except ValueError:
            # Si el usuario no envió un número válido
            await update.message.reply_text("Lo siento, eso no es un número válido. Por favor, intenta de nuevo.")
        finally:
            # Limpiar el estado
            context.user_data['esperando_numero'] = False
    else:
        # Si el usuario envía un mensaje sin estar en el estado 'esperando_numero'
        await update.message.reply_text("Lo siento, no entiendo ese comando. Escribe /help para ver las opciones disponibles.")

# Función para manejar el comando /ultimas_notas
async def ultimas_notas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verificar si el usuario proporcionó un argumento (número de notas)
    try:
        x = int(context.args[0])  # Obtener el número de notas desde los argumentos del comando
        if x <= 0:
            raise ValueError()
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, proporciona un número válido de notas. Ejemplo: /ultimas_notas 5")
        return

    # Cargar el archivo JSON
    try:
        with open("./datos/data_nota_informativa.json", "r", encoding="utf-8") as file:
            datos = json.load(file)
    except FileNotFoundError:
        await update.message.reply_text("No se encontró el archivo de notas informativas.")
        return
    except json.JSONDecodeError:
        await update.message.reply_text("El archivo de notas informativas no tiene un formato válido.")
        return

    # Validar que los datos sean una lista
    count=x
    ultimas_notas=[]
    mensaje = "Últimas notas informativas:\n"
    for fecha,nota in datos.items():
        count-=1
        
        mensaje += f"- {fecha}: {nota}\n"
    # Formatear las notas como un mensaje

    # Enviar las notas al usuario
    await update.message.reply_text(mensaje)

# Función principal para iniciar el bot
def main():
    # Reemplaza 'TU_TOKEN_AQUI' con el token que obtuviste de BotFather
    token = "7340871190:AAHHCJgbak61ui7ypZSnEhd63DN_Q07q5qg"
    
    # Crear la aplicación y pasarle el token
    application = Application.builder().token(token).build()
    
    # Registrar manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("horario_apagon", horario_apagon))
    application.add_handler(CommandHandler("reportar_falla", reportar_falla))
    application.add_handler(CommandHandler("facturacion", facturacion))
    application.add_handler(CommandHandler("sumar_uno", sumar_uno))  # Nuevo comando /sumar_uno
    application.add_handler(CommandHandler("ultimas_notas", ultimas_notas))  # Nuevo comando /ultimas_notas
    
    # Registrar manejador para mensajes de texto no reconocidos
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numero_response))
    
    # Iniciar el bot
    print("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling()

if __name__ == "__main__":
    main()