import os
import io

from telebot import TeleBot
import dotenv
from PIL import Image

from Operation import Operation

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = TeleBot(TOKEN)

operation = Operation()

def get_image(file_path):
    return Image.open(io.BytesIO(bot.download_file(file_path)))

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Please send the image you would like to be posterized.')

@bot.message_handler(content_types=['photo'])
def image(message):
    operation.image = get_image(bot.get_file(message.photo[-1].file_id)
                                .file_path)
    operation.image_id = message.id
    operation.color_num = None

    bot.reply_to(message, 'Please specify the desired number of colors in the posterized image.')
    
        
@bot.message_handler(content_types=['text'])
def color_num(message):
    if operation.image is None:
        bot.reply_to(message, 'Please send image first.')
        return
    try:
        operation.color_num = message.text
    except ValueError as e:
        bot.reply_to(message, str(e))
        return

    buffer = io.BytesIO()
    posterized_image, original_image_id = operation.posterize_image()
    posterized_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    bot.send_photo(message.chat.id, reply_to_message_id=original_image_id, photo=buffer)

        
bot.infinity_polling()