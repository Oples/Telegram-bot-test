import os
import telebot
import asyncio
import youtube_dl
from cfg import *
from cleverbot import Cleverbot

bot = telebot.AsyncTeleBot(TOKEN)
mind = Cleverbot()
task = bot.get_me()
loop = asyncio.get_event_loop()
future = asyncio.Future()


class MyLogger(object):    # Youtube-dl info on errors/warning
   def debug(self, msg):
       pass

   def warning(self, msg):
       print(msg)

   def error(self, msg):
       print(msg)

def my_hook(d):            # again Youtube-dl
   if d['status'] == 'finished':
       print('Done downloading, now converting ...')


ydl_opts = {               # OPTIONS youtube-dl mp3 :T
   'format': 'bestaudio/best',
   'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
   }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

try:
   @bot.message_handler(commands=['info'])
   def send_info(message):
      bot.reply_to(message, str(message.chat.id) +'\n'+ str(message.from_user.first_name))

   @bot.message_handler(commands=['ping'])
   def test_ping(message):
      bot.send_message(message.chat.id, 'Pong!')

   @bot.message_handler(commands=['start', 'help'])
   def send_welcome(message):
      if message.chat.type == 'private':
         bot.reply_to(message, "Howdy, how are you doing?")

   @bot.message_handler(commands=['rainbows'])
   def rainbow(message):
      msg=""" Now a rainbow's tale isn't quite as nice
As the story we knew of sugar and spice
But a rainbow's easy once you get to know it
With the help of the magic of a pegasus device
Let's delve deeper into rainbow philosophy
Far beyond that of Cloudsdale's mythology
It's easy to misjudge that floating city
With its alluring decor and social psychology
But with all great things comes a great responsibility
That of Cloudsdale's being weather stability
How, you ask, are they up to the task
To which the answer is in a simple facility
In the Rainbow Factory, where your fears and horrors come true
In the Rainbow Factory, where not a single soul gets through
Source: Aurora Dawn """
      bot.send_message(message.chat.id, msg)
   
   @bot.message_handler(func=lambda message: True)
   def echo_all(message):
       msg = message.text
       if (msg.find('http://') != -1 or msg.find('https://') != -1 ):
          try:
             with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                 info_dict = ydl.extract_info(msg, download=False)
                 bot.send_message(message.chat.id, 'downloading ...')
                 ydl.download([msg])
                 video_title = info_dict.get('title', None)
                 video_title = video_title.replace('|','_')
                 os.system('mv ./'+video_title+'-'+info_dict['id']+'.mp3 ./'+ video_title+'.mp3')
                 bot.send_document(message.chat.id, open(video_title+'.mp3', 'rb'))
                 os.system("mv ./*.mp3 ~/Music/")
                 #except DownloadError(message, exc_info):
                 #bot.sendMessage (message.channel,'Bad Link')
          except:
             bot.send_message(message.chat.id, 'Bad link :T \n\nGive me audio/video sites')
       if message.chat.type == 'private':
          try:
             bot.send_message(message.chat.id, mind.ask(message.text))
          except:
             print('cleverbot fail')
       elif message.text.startswith('Hello'):
          bot.reply_to(message, 'Hi :3')

   result = task.wait() # Get the result of the execution

   bot.polling()
   
except:
   pass

# api link: https://github.com/eternnoir/pyTelegramBotAPI
