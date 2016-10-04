import os
import sys
# cfg.py where the bot token is hidden :D
from cfg import *
# TODO: Make async work :T
import asyncio 
import logging
import datetime
import youtube_dl
from telegram import *
from telegram.ext import *
from cleverbot import Cleverbot
from translate import translator

# Inizializyng the asyncronous classes
loop = asyncio.get_event_loop()
future = asyncio.Future()

try:
   updater = Updater(token=TOKEN) # Hidden bot token
   print('booting'+ datetime.time())               # The token is needed for the bot to log in to an account
   dispatcher = updater.dispatcher
   mind = Cleverbot()             # Cleverbot functions

   logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
                                  # Default staff

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

   ydl_opts1= {              # Options for webm/video download
       'format': 'bestaudio/best',
       'postprocessors': [{
           'key': 'FFmpegVideoConvertor',
           'preferedformat': 'webm',
       }],
       'logger': MyLogger(),
       'progress_hooks': [my_hook],
   }
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


   def start(bot, update):      # Wellcome message
      bot.sendMessage(chat_id=update.message.chat_id, text="I'm a beautiful pone, please talk to me m8!")
        
   def ytdwl(bot, update):     # /yt command
        msg = update.message.text
        msg = msg.replace('/yt ','')
        msg = msg.replace(' ','')
        print(msg)
        try:
           with youtube_dl.YoutubeDL(ydl_opts1) as ydl:
               info_dict = ydl.extract_info(msg, download=False)
               bot.sendMessage(chat_id=update.message.chat_id, text='Downloading ...')
               ydl.download([msg])
               video_title = info_dict.get('title', None)
               video_title = video_title.replace('|','_')
               video_title = video_title.replace('?','')
               print(video_title+'-'+info_dict['id']+'.webm')
               bot.sendDocument(chat_id=update.message.chat_id, document=open(video_title+'-'+info_dict['id']+'.webm', 'rb'), filename=video_title+'.webm')
               #except DownloadError(message, exc_info):
               #bot.sendMessage (message.channel,'Bad Link')
        except:
           bot.sendMessage(chat_id=update.message.chat_id, text='Bad link :T \n\nGive me audio/video sites')
	
   # TODO: FIX THIS PLZ ;___;
    
   def okidoky(bot, update):
       print('Text: ')
       echo(bot, update)
        
   def echo(bot, update):      # EVERY MESSAGE THAT IS NOT A COMMAND GOES HERE!
         msg = update.message.text
         if (msg.find('http://') != -1 or msg.find('https://') != -1 ):
           try:
              with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                  info_dict = ydl.extract_info(msg, download=False)
                  bot.sendMessage(chat_id=update.message.chat_id, text='Downloading ...')
                  ydl.download([msg])
                  video_title = info_dict.get('title', None)
                  video_title = video_title.replace('|','_')
                  print(video_title+'-'+info_dict['id']+'.mp3')
                  bot.sendDocument(chat_id=update.message.chat_id, document=open(video_title+'-'+info_dict['id']+'.mp3', 'rb'), filename=video_title+'.mp3')
                  #except DownloadError(message, exc_info):
                  #bot.sendMessage (message.channel,'Bad Link')
           except:
              bot.sendMessage(chat_id=update.message.chat_id, text='Bad link :T \n\nGive me audio/video sites')
         else:
           bot.sendMessage(chat_id=update.message.chat_id, text=mind.ask(update.message.text))
           print(update.message.text)

   def ping(bot, update):         # ez peasy test response
      bot.sendMessage(chat_id=update.message.chat_id, text="Pong!")

   
   def ts(bot, update):          # TODO: fix this translator
      msg = translator('en', 'zh-TW' , update.message.text)
      bot.sendMessage(chat_id=update.message.chat_id, text=msg)

   def files(bot, update):       # Send source file
      if str(30954744) == str(update.message.chat_id):
           bot.sendDocument(chat_id=update.message.chat_id, document=open('TelegramShy.py', 'rb'))
           print('        Sending file telegramShy.py')

   def cmd(bot, update):        # AWARE OF THE RISK
      msg = update.message.text
      msg = msg.replace('/cmd ', '') 
      print(msg)
      with open('file.txt','w') as f: # re-write file
         f.close()
      with open('file.txt','r') as f: # read the output of the bash
         os.system(msg+' >> file.txt')
         bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
         f.close()
         os.system('rm file.txt')     # dirty reset(Not really needed) write the file does replace the content with nothing already

   def sudo(bot, update):
      if str(30954744) == str(update.message.chat_id):
         msg = update.message.text
         msg = msg.replace('/sudo ', 'echo -e "pon3\\n" | sudo -S ') # my sudo passwd
         print(msg)
         with open('file.txt','w') as f:
            f.close()
         with open('file.txt','r') as f:
            os.system(msg+' >> file.txt')
            bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
            f.close()
            os.system('rm file.txt')

   def pong(bot, update): # next time I'll be more savage
      bot.sendMessage(chat_id=update.message.chat_id, text="No!")
      bot.sendSticker(chat_id=update.message.chat_id, sticker=open("./sticker.webp", 'rb'))
      print(update.message.chat_id)
      #reply_keyboard = ['ping']
      #update.message.reply_text('',)
      #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


   def rainbow(bot, update):
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
      bot.sendMessage(chat_id=update.message.chat_id, text=msg)


   def halp(bot, update):
      msgbox  = '/help                -This :T\n'
      msgbox += '/ping                -Server test\n'
      msgbox += '/rainbows       -Fancy poem\n'
      msgbox += '/yt                  -dwload mp4\n'
      msgbox += 'Clever bot will answer to normal chat\n'
      msgbox += 'If you post links she will automaticaly download mp3\n'
      bot.sendMessage(chat_id=update.message.chat_id, text=msgbox)

except ConnectionError:
   Commands()
except SystemExit:
   print('*blushes*')
except:
   print('\n  ERROR\n')

#away from the exceptions
def Commands():
     updater.stop()
     os.system('sh ~/telebot.sh')

def reboot(bot, update):
   bot.sendMessage(chat_id=update.message.chat_id, text="Rebooting..")
   Commands()
#this 2 reboots the sys


dispatcher.add_handler(MessageHandler([Filters.text],okidoky))  #async all messages a part commands

#Messages handler!
dispatcher.add_handler(CommandHandler('start', start))     # /start Telegram force the user to use this command before chatting

ping_handler = CommandHandler('ping', ping)                # /ping
dispatcher.add_handler(ping_handler)

dispatcher.add_handler(CommandHandler('pong', pong))       # /pong SHHH secret

dispatcher.add_handler(CommandHandler('help', halp))       # /help

dispatcher.add_handler(CommandHandler('cmd', cmd))         # /cmd  <- probable a fancy code

dispatcher.add_handler(CommandHandler('yt', ytdwl))

dispatcher.add_handler(CommandHandler('sudo', sudo))       # /sudo <- probable a fancy code

dispatcher.add_handler(CommandHandler('file', files))      # /file

dispatcher.add_handler(CommandHandler('reboot', reboot))   # /reboot

dispatcher.add_handler(CommandHandler('rainbows', rainbow))# /rainbows

#dispatcher.add_handler(MessageHandler([Filters.text],echo))# all messages a part commands

@asyncio.coroutine
def AutoRE():
     while True:
       yield from asyncio.sleep(1200)
       Commands()
       sys.exit(0)

asyncio.async(AutoRE())

returns = False
print('updating...')
while(returns == False):
   returns = updater.start_polling()
   updater.start_polling()
   if (returns):
       print('\n\n\n\all ok  Bot IS UP!')
   else:
       print('Check the connection & bot plz fix :C')
       time.sleep(0.5)

try:
       loop.run_forever()
finally:
       loop.close()


