import telebot
import os
import logging
import requests
from dotenv import load_dotenv
from gtts import gTTS
import edge_tts
import asyncio
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup

os.makedirs('voices',exist_ok=True)
os.makedirs('voices2',exist_ok=True)

load_dotenv()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

API_TOKEN=os.getenv('API_TOKEN')


bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send(message):

    markup = InlineKeyboardMarkup()
    language_fa = InlineKeyboardButton('فارسی',callback_data='فارسی')
    language_en = InlineKeyboardButton('انگلیسی',callback_data='انگلیسی')

    markup.add(language_fa,language_en)

    bot.send_message(message.chat.id , 'انتخاب کنید' ,reply_markup=markup)
    

@bot.callback_query_handler(func= lambda call : True)
def send_speach(call):
    if call.data == 'انگلیسی':
        msg =bot.send_message(chat_id=call.message.chat.id , text='ارسال کنید')
        bot.register_next_step_handler(msg, speach_en)

    elif call.data == 'فارسی':
        msg = bot.send_message(chat_id=call.message.chat.id , text='ارسال کنید')
        bot.register_next_step_handler(msg , speach_fa)
    else :
         pass
    

@bot.message_handler(func= lambda message : True )
def speach_en(message):
    bot.send_message(message.chat.id , 'لطقا شکیبا باشید درحال پردازش...')
    text = message.text
    file = f"voices/{message.chat.id}.mp3"
    voice = gTTS(text=text , lang='en' , tld='com.au' , slow=False)
    voice.save(file)
    bot.send_voice(chat_id=message.chat.id , voice=open(file,'rb'))
    os.remove(file)

    markup = InlineKeyboardMarkup()
    language_fa = InlineKeyboardButton('فارسی',callback_data='فارسی')

    language_en = InlineKeyboardButton('انگلیسی',callback_data='انگلیسی')
    
    markup.add(language_fa,language_en)
    bot.send_message(chat_id=message.chat.id, text='انتخاب کنید')

@bot.message_handler(func= lambda message: True )
def speach_fa(message):
    bot.send_message(chat_id=message.chat.id , text='لطقا شکیبا باشید درحال پردازش...')
    text = message.text
    file = f"voices2/{message.chat.id}.mp3"
    async def fa_speacher(text , voice="fa-IR-DilaraNeural" , output =file):
        communicate = edge_tts.Communicate(text=text , voice=voice)
        await communicate.save(output)
    asyncio.run(fa_speacher(text))
    bot.send_voice(chat_id=message.chat.id , voice=open(file,'rb'))
    os.remove(file)

    markup = InlineKeyboardMarkup()
    language_fa = InlineKeyboardButton('فارسی',callback_data='فارسی')

    language_en = InlineKeyboardButton('انگلیسی',callback_data='انگلیسی')
    
    markup.add(language_fa,language_en)
    bot.send_message(chat_id=message.chat.id, text='انتخاب کنید' , reply_markup=markup)

print('Bot is running...')
bot.infinity_polling(skip_pending=True)