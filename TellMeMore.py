import os
import telebot
import asyncio
from cfg import *
from cleverbot import Cleverbot

bot = telebot.AsyncTeleBot(TOKEN)
mind = Cleverbot()
task = bot.get_me()
loop = asyncio.get_event_loop()
future = asyncio.Future()

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

   @bot.message_handler(func=lambda message: True)
   def echo_all(message):
      if message.chat.type == 'private':
         try:
            bot.send_message(message.chat.id, mind.ask(message.text))
         except:
            print('cleverbot fail')
      elif message.text.startswith('Hello'):
         bot.reply_to(message, 'Hi :3')

except:
   pass

# Do some other operations...
a = 0
for a in range(100):
    a += 10
    print(a)


def okidoky():
    print('ok')


bot.polling()


result = task.wait() # Get the result of the execution
