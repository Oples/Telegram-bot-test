import os
import sys
# cfg.py where the bot token is hidden :D
from cfg import *
# TODO: Make async work :T
import asyncio 
import logging
import youtube_dl
from telegram import *
from telegram.ext import *
from cleverbot import Cleverbot
from translate import translator

try:
   updater = Updater(token=TOKEN) # Hidden bot token

   dispatcher = updater.dispatcher
   mind = Cleverbot()

   logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

   class MyLogger(object):    # Youtube-dl
       def debug(self, msg):
           pass

       def warning(self, msg):
           pass

       def error(self, msg):
           print(msg)


   def my_hook(d):            # again Youtube-dl
       if d['status'] == 'finished':
           print('Done downloading, now converting ...')

   ydl_opts1= {
       'format': 'bestaudio/best',
       'postprocessors': [{
           'key': 'FFmpegExtactAudio',
           'preferredcodec': 'mp4',
       }],
   }
   ydl_opts = {               # OPTIONS youtube-dl :T
       'format': 'bestaudio/best',
       'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'mp3',
           'preferredquality': '192',
       }],
       'logger': MyLogger(),
       'progress_hooks': [my_hook],
   }


   def start(bot, update):
      bot.sendMessage(chat_id=update.message.chat_id, text="I'm a beautiful pone, please talk to me m8!")
      
      
   def reboot(bot, update):
      bot.sendMessage(chat_id=update.message.chat_id, text="Rebooting..")
      os.system("git pull origin master")
      os.system("python3.5 TelegramShy.py")
      sys.exit(0)

   def echo(bot, update):
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


   def ping(bot, update):
      bot.sendMessage(chat_id=update.message.chat_id, text="Pong!")

   def ts(bot, update):
      msg = translator('en', 'zh-TW' , update.message.text)
      bot.sendMessage(chat_id=update.message.chat_id, text=msg)

   def files(bot, update):
      if str(30954744) == str(update.message.chat_id):
           bot.sendDocument(chat_id=update.message.chat_id, document=open('TelegramShy.py', 'rb'))
           print('        Sending file telegramShy.py')

   def cmd(bot, update):
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
      msgbox += '\n'
      msgbox += '       Clever bot will answer to normal chat\n'
      msgbox += 'If you post links she will automaticaly download mp3\n'
      bot.sendMessage(chat_id=update.message.chat_id, text=msgbox)

except HTTPError:
   pass
except:
   pass

# TODO: FIX THIS PLZ ;___;
#
#@asyncio.coroutine
#def EchoTest:
#   def okidoky:
#  print('ok')
#  dispatcher.add_handler(MessageHandler([Filters.text],okidoki))  #all messages a part commands
	

#Messages handler!
start_handler = CommandHandler('start', start)        #/start
dispatcher.add_handler(start_handler)
ping_handler = CommandHandler('ping', ping)           #/ping
dispatcher.add_handler(ping_handler)
pong_handler = CommandHandler('pong', pong)           #/pong
dispatcher.add_handler(pong_handler)
halp_handler = CommandHandler('help', halp)           #/help
dispatcher.add_handler(halp_handler)

dispatcher.add_handler(CommandHandler('cmd', cmd)) #/cmd <- probable a fancy code

dispatcher.add_handler(CommandHandler('ts', ts))

dispatcher.add_handler(CommandHandler('sudo', sudo)) #/cmd <- probable a fancy code

dispatcher.add_handler(CommandHandler('file', files))  #/file

dispatcher.add_handler(CommandHandler('reboot', reboot))  #/reboot

rainbow_handler = CommandHandler('rainbows', rainbow) #/rainbows
dispatcher.add_handler(rainbow_handler)

dispatcher.add_handler(MessageHandler([Filters.text],echo))  #all messages a part commands

loop = asyncio.get_event_loop()
future = asyncio.Future()

#asyncio.async(EchoTest)

try:
       loop.run_forever()
finally:
       loop.close()

updater.start_polling()
