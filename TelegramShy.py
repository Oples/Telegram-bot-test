import os
import sys
import glob
# cfg.py where the bot token is hidden :D
from cfg import *
# ASYNC IN THIS THING LEL
from telegram.ext.dispatcher import run_async
# Not this
import asyncio 
import logging
import datetime
import youtube_dl
import time as ronf
from telegram import *
from telegram.ext import *
from telegram.error import *
from cleverbot import Cleverbot
# https://github.com/terryyin/google-translate-python 
from translate import Translator

# Inizializyng the asyncronous classes
loop = asyncio.get_event_loop()
future = asyncio.Future()
right_now = str(datetime.datetime.now().time())
right_now = right_now.split('.')
mypath = str(os.path.expanduser("~"))
mypath = mypath.replace('\\','/')
mypath = mypath + "/Music/"

try:
   #variable assingment
   updater = Updater(token=TOKEN) # Hidden bot token
   bot = Bot(TOKEN)
   print('\033[037m\033[2J\033[Hbooting  '+str(right_now[0])+'\033[0m')               # The token is needed for the bot to log in to an account
   
   try:
      update_id = bot.getUpdates()[0].update_id
   except IndexError:
      update_id = None
   
   
   bot.sendMessage(chat_id=OWNER_ID, text='BACK FROM THE DEAD')
       
       
   dispatcher = updater.dispatcher
   mind = Cleverbot()             # Cleverbot functions
   working=0

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

   """ydl_opts1= {              # Options for webm/video download
       'format': 'bestaudio/best',
       'postprocessors': [{
           'key': 'FFmpegVideoConvertor',
           'preferedformat': 'mkv',
       }],
       'logger': MyLogger(),
       'progress_hooks': [my_hook],
   }"""
   
   ydl_opts1= {
        'format': 'bestaudio/best',
        #'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
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

   @run_async
   def start(bot, update):      # Wellcome message
      bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bit bot, please talk to me m8!")
   
   @run_async     
   def ytdwl(bot, update):     # /yt command
        msg = update.message.text
        msg = msg.replace('/yt ','')
        print(msg)
        try:
           # get youtube downoader and search for the song
           with youtube_dl.YoutubeDL(ydl_opts1) as ydl:
               # get entries
               info_dict = ydl.extract_info(msg, download=False)
               # for the async reboot now useless
               # TODO: remove it
               working=1
               # Text if the search was succesfull
               bot.sendMessage(chat_id=update.message.chat_id, text='Downloading ...')
               # start downloading
               with youtube_dl.YoutubeDL(ydl_opts) as yadl:
                   yadl.download([info_dict['entries'][0]['webpage_url']])
               # Issue for title names need fix
               video_title = str(info_dict['entries'][0]['title'])
               video_title = video_title.replace('|','_')
               video_title = video_title.replace('"','')
               video_title = video_title.replace('?','')
               # debug
               print(video_title+'-'+str(info_dict['entries'][0]['id'])+'.mp3')
               # send file by name
               bot.sendDocument(chat_id=update.message.chat_id, document=open(video_title+'-'+info_dict['entries'][0]['id']+'.mp3', 'rb'), filename=video_title+'.mp3')
               # move it to music dir
               os.system("mv ./*.mp3 ~/Music/")
               # done working set to 0
               working = 0
        except Exception as w:
           # on error
           bot.sendMessage(chat_id=update.message.chat_id, text='Bad link :T \n\nGive me audio/video sites\n'+str(w))
           working=0

   def undo(bot,update): # /unblacklist
         """ delete previus user that do not want
             to be in the blacklist anymore :3 """
         try:
            foo = open("blacklist.txt","r")
            msg = str(foo.read())

            if (msg.find(str(update.message.chat_id))!=-1): # if the chat is not listed yet add it
               msg = msg.replace(str(update.message.chat_id)+"\n","")
               foo.close()
               foo = open("blacklist.txt","w")
               foo.write(msg)
               foo.close()
               bot.sendMessage(chat_id=update.message.chat_id, text='Undo blacklist')
            else:
               bot.sendMessage(chat_id=update.message.chat_id, text='This chat is not listed!')
         except Exception as e:
            # as written the file was not found or is un readable
            print("Possible file not found"+str(e))
            foo = open("blacklist.txt","w")
            foo.close()
            bot.sendMessage(chat_id=update.message.chat_id, text='This chat is not listed!')

   @run_async
   def blacklisting(bot,update): # /blacklist
         try:
            foo = open("blacklist.txt","r")
            msg = str(foo.read())
            foo.close()
            if (msg.find(str(update.message.chat_id))==-1):
               foo = open("blacklist.txt","a")
               foo.write(str(update.message.chat_id)+"\n")
               bot.sendMessage(chat_id=update.message.chat_id, text='BOOM blacklisted!')
            else:
               bot.sendMessage(chat_id=update.message.chat_id, text='This chat is already Blacklisted!')
         except Exception as e:
            print("Possible file not found"+str(e))
            foo = open("blacklist.txt","w")
            foo.write(str(update.message.chat_id))
            foo.close()

   @run_async
   def echo(bot, update):      # EVERY MESSAGE THAT IS NOT A COMMAND GOES HERE!
         # get blacklist file
         try:
            foo = open("blacklist.txt","r")
         except Exception as e:
            print("Possible file not found"+str(e))
            foo = open("blacklist.txt","w")
            foo.close()
         fi = str(foo.read())
         # search if chat is listed in blacklist
         if (fi.find(str(update.message.chat_id))==-1):
            # text in a string var
            msg = str(update.message.text)

            foo.close()
            # automatic download on given link
            if (msg.startswith('http://') or msg.startswith('https://')):
              try:
                 with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                 
                    info_dict = ydl.extract_info(msg, download=False)
                    bot.sendMessage(chat_id=update.message.chat_id, text='Downloading ...')
                    ydl.download([msg])
                    video_title = info_dict.get('title', None)
                    video_title = video_title.replace('|','_')
                    bot.sendMessage(chat_id=update.message.chat_id, text='hold tight')
                    move_up = str('mv "./'+video_title+'-'+info_dict['id']+'.mp3" "./'+video_title+'.mp3"')
                    print(move_up)
                    os.system(move_up)
                    bot.sendDocument(chat_id=update.message.chat_id, document=open(video_title+'.mp3', 'rb'), filename=video_title+'.mp3')
                    os.system("mv ./*.mp3 ~/Music/")
                    
              except:
                 bot.sendMessage(chat_id=update.message.chat_id, text='Bad link :T')
                 
            yes_no = msg.lower()
            # evil staff
            if (yes_no == 'no'):
               bot.sendMessage(chat_id=update.message.chat_id, text='Yes')
          
            elif (yes_no == 'yes' or yes_no == 'si'):
               bot.sendMessage(chat_id=update.message.chat_id, text='No')
            
            elif (update.message.chat.type =='private'):
               bot.sendMessage(chat_id=update.message.chat_id, text=mind.ask(msg))
               print(msg)

   @run_async
   def ping(bot, update):         # ez peasy test response
      bot.sendMessage(chat_id=update.message.chat_id, text="Pong!")
   
   @run_async
   def info(bot, update):         # info on message
      uptime = right_now[0].split(':')
      downtime = str(datetime.datetime.now().time())
      downtime = downtime.split(':')
      msg  = 'Uptime:       '+right_now[0]+'\n'
      # not needed anymore
      # msg += 'rebooting:  '+str(((int(uptime[1])+20)-int(downtime[1])))+'\n'
      msg += 'Chat id:       '+str(update.message.chat_id)+'\n'
      msg += 'Type:           '+str(update.message.chat.type)+'\n'
      msg += 'user name: '+str(update.message.from_user.username)+'\n'
      #msg += 'Last name:  '+update.message.user.last_name
      bot.sendMessage(chat_id=update.message.chat_id, text=msg)

   @run_async
   def direc(bot, update):
      msg = glob.glob(mypath+"*.mp3")
      i = 0
      directories = ['','']
      t = 0
      try:
         for i in range(len(msg)):
             directories[t] += '['+str(i)+'] '+ msg[i]+'\n'
             # telegram accepts only 90 lines of message
             if (i==80):
                 t += 1
         for g in range(len(directories)):
             directories[g] = directories[g].replace(mypath,'')
         print(directories)
         for h in range(len(directories)):
             bot.sendMessage(chat_id=update.message.chat_id, text=directories[h])
      except Exception as w:
         print('Array error '+str(w))
         raise

   def ts(bot, update): # link above to import for more info
      mess = str(update.message.text)
      mess = mess.replace('/ts ','')
      try:
           translator = Translator(to_lang="it")
           msg = translator.translate(mess)
           ronf.sleep(0.4)
           bot.sendMessage(chat_id=update.message.chat_id, text=msg)
      except Exception as e:
           bot.sendMessage(chat_id=update.message.chat_id, text="I can't read this thing!\n"+str(e))

   @run_async
   def files(bot, update):       # Send source file
      msg = str(update.message.text)
      msg = msg.replace('/file ','')
      if str(OWNER_ID) == str(update.message.chat_id):
           bot.sendDocument(chat_id=update.message.chat_id, document=open(msg, 'rb'))
           print('        Sending file '+msg)

   @run_async
   def test(bot, update):
      with open('file.txt','w') as f: # re-write file
         f.close()
      with open('file.txt','r') as f: # read the output of the bash
         os.system('ping -c 1 google.com >> file.txt')
         bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
         f.close()
         os.system('rm file.txt')     # dirty reset(Not really needed) write the file does replace the content with nothing already

   @run_async
   def cmd(bot, update):        # AWARE OF THE RISK
      msg = update.message.text
      msg = msg.replace('/cmd ', '')
      print(msg)
      if ( msg.find('rm') == -1):
          with open('file.txt','w') as f: # re-write file
             f.close()
          with open('file.txt','r') as f: # read the output of the bash
             os.system(msg+' >> file.txt')
             bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
             f.close()
             os.system('rm file.txt')     # dirty reset(Not really needed) write the file does replace the content with nothing already
      else:
          bot.sendMessage(chat_id=update.message.chat_id, text='Nope')
          
   @run_async
   def sudo(bot, update):
      if str(OWNER_ID) == str(update.message.chat_id):
          msg = update.message.text
          msg = msg.replace('/sudo ', 'echo -e "pon3\n" | sudo -S ') # my sudo passwd
          print(msg)
          with open('file.txt','w') as f:
             f.close()
          with open('file.txt','r') as f:
             os.system(msg+' >> file.txt')
             bot.sendMessage(chat_id=update.message.chat_id, text=f.read())
             f.close()
             os.system('rm file.txt')

   @run_async
   def pong(bot, update): # next time I'll be more savage
      bot.sendMessage(chat_id=update.message.chat_id, text="No!")
      bot.sendSticker(chat_id=update.message.chat_id, sticker=open("facepalm.webp", 'rb'))
      print(update.message.chat_id)
      # coming soon
      #reply_keyboard = ['ping']
      #update.message.reply_text('',)
      #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

   @run_async
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

   @run_async
   def halp(bot, update):
      msgbox  = '/help                -This :T\n'
      msgbox += '/ping                -Server test\n'
      msgbox += '/rainbows       -Fancy poem\n'
      msgbox += '/yt                  -dwload mp4\n'
      msgbox += '/info                -chat/bot info\n'
      msgbox += 'Clever bot will answer to normal chat\n'
      msgbox += 'If you post links she will automaticaly download mp3\n'
      bot.sendMessage(chat_id=update.message.chat_id, text=msgbox)

except ConnectionError:
   Commands()
except SystemExit:
   print('*blushes*')
   updater.stop()
except KeyboardInterrupt:
   print('*blushes*')
   updater.stop()
   sys.exit(0)
except Exception as w:
   # send error do chat
   print('\n  ERROR\n'+ str(w) )
   bot.sendMessage(chat_id=OWNER_ID, text='HALP!\n'+str(w))
   os.system('sh ~/telebot.sh')

#away from the exceptions
def Commands():
     updater.stop()
     os.system('sh ~/telebot.sh')

def reboot(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Rebooting..")
    Commands()

#this 2 reboots the sys

dispatcher.add_handler(MessageHandler([Filters.text],echo))  #async all messages a part commands

#dispatcher.run_async()

#Messages handler!
dispatcher.add_handler(CommandHandler('start', start))     # /start Telegram force the user to use this command before chatting

ping_handler = CommandHandler('ping', ping)                # /ping
dispatcher.add_handler(ping_handler)

dispatcher.add_handler(CommandHandler('pong', pong))       # /pong SHHH secret

dispatcher.add_handler(CommandHandler('help', halp))       # /help

dispatcher.add_handler(CommandHandler('info', info))       # /info basic staff

dispatcher.add_handler(CommandHandler('cmd', cmd))         # /cmd  <- probable a fancy code

dispatcher.add_handler(CommandHandler('lant', test))         # /cmd  <- ping an ip if is alive

dispatcher.add_handler(CommandHandler('ts', ts))         # /ts   <- still doesn't support idiot lenguage

dispatcher.add_handler(CommandHandler('blacklist',blacklisting)) # ripperino blacklist

dispatcher.add_handler(CommandHandler('unblacklist',undo)) # ripperino undo blacklist

dispatcher.add_handler(CommandHandler('yt', ytdwl))

dispatcher.add_handler(CommandHandler('sudo', sudo))       # /sudo <- probable a fancy code

dispatcher.add_handler(CommandHandler('file', files))      # /file

dispatcher.add_handler(CommandHandler('reboot', reboot))   # /reboot

dispatcher.add_handler(CommandHandler('dir', direc))   # /reboot

dispatcher.add_handler(CommandHandler('rainbows', rainbow))# /rainbows


@asyncio.coroutine         # Async for the reboot after 20 minutes
def AutoRE():
     while True:
       yield from asyncio.sleep(3600)
       if (working==0):
          Commands()
          sys.exit(0)
       
asyncio.async(AutoRE())    # Start the async


returns = False

while(returns == False):   # Start the bot if it returns False the the bot Can't log-in
   returns = updater.start_polling()
   updater.start_polling()
   # Updater.start_polling returns true if succesfull
   if (returns):
       print('\n\n\nall ok  Bot IS UP!')
       updater.idle()
   else:
       print('Check the connection & bot plz fix :C')
       time.sleep(2)

try:
       loop.run_forever()
finally:
       loop.close()

