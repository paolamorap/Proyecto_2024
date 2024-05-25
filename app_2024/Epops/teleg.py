import telebot

# Token del bot de Telegram
TOKEN = '6719870472:AAFerw5_cbcI1w_3kMqfqw963cwQYTIrcP8' 

# ID del chat donde se enviaran los mensajes
chat_id = -4179209636

bot = telebot.TeleBot(TOKEN)

# Función para enviar mensaje
def enviar_mensaje(message):
    """
    Envia mensajes a un chat especifico a través de un bot de telegram

    Parameters:
    message(str):   Mensaje que se enviará

    Return:
    None

    """
    try:
        bot.send_message(chat_id, message)
        print("Mensaje enviado exitosamente.")
    except Exception as e:
        print("Ocurrió un error al enviar el mensaje:", e)

