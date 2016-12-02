#!/usr/bin/python3
import os
import sys
import time
import getpass
import urllib.request

# Only unix like systems
if (os.name == 'posix'):
    print('Initializing the Installation\n')
    # user name
    print('Ciao ' + os.environ.get('USER') + '!')
    # hostname
    print('propietario di '+os.popen('cat /etc/hostname').read())
    
    # richesta password
    while True:
        # prendi la password
        passwd = getpass.getpass('ho bisogno di essere root!\npasswd:\033[7m\033[5m\033[0m')
        # controlla la password
        if os.system('echo -e "' +passwd+ '\n" | sudo -S echo') == 0:
            break
        else:
            print('come on m8!')
    
    # controlla se pip è installato
    if (os.system('pip3 >> /dev/null') == 0):
        print("\n[\033[32mok\033[0m] pip3")
        
    else:
        print('[\033[31mFail\033[0m] pip3')
        print('\ndevi installare pip3')
        print('Lo installo io?')
        print('\nInstallando ..')
        # download and install pip3
        os.system('wget https://bootstrap.pypa.io/get-pip.py')
        if (os.system('''echo -e "'''+passwd+'''\n" | sudo -S python3 get-pip.py >> /dev/null''') == 0 ):
            print('[\033[32mInstalled\033[0m] pip3')
        else:
            print('[\033[31mFatal\033[0m] pip3')
        os.system('rm get-pip.py')
        
    print('\n[installando le librerie]')
    if (os.system('''echo -e "'''+passwd+'''\n" | sudo -SH pip3 install Cleverbot >> /dev/null''') == 0):
        print("[\033[32mok\033[0m] Cleverbot")
    else:
         print('[\033[31mFail\033[0m] Cleverbot')
            
    if (os.system('''echo -e "'''+passwd+'''\n" | sudo -SH pip3 install python-telegram-bot >> /dev/null''') == 0):
        print("[\033[32mok\033[0m] python-telegram-bot")
    else:
         print('[\033[31mFail\033[0m] python-telegram-bot')
            
    try:
        with open('translate.py','w') as file:
            file.write(str(urllib.request.urlopen("https://raw.githubusercontent.com/terryyin/google-translate-python/master/translate.py").read()))
            print("[\033[32mok\033[0m] youtube-dl")
    except Exception as e:
         print('[\033[31mFail\033[0m] youtube-dl\n' + str(e))
            
    if (os.system('''curl https://raw.githubusercontent.com/terryyin/google-translate-python/master/translate.py >> translate.py''') == 0):
        print("[\033[32mok\033[0m] translate")
    else:
         print('[\033[31mFail\033[0m] translate')
            
    print('Done!\n')
    print('all libraries installed')
    try:
        with open('cfg.py','r') as f:
            if (str(f.read()).startswith('TOKEN =')):
                print('[\033[32mok\033[0m] token')
            else:
                print('[\033[31m\033[0m] token')
                os.system('rm cfg.py')
                raise FileNotFoundError('File is corrupted')
    except FileNotFoundError:
        token = input('Please insert your bot Token here: ')
        chat_id = input('(If you don\'t know it go to @Oples_bot and send /info)\n Please insert your Telegram chat_id here: ')
        with open('cfg.py','w') as w:
            w.write('TOKEN = \'\'\''+token+'\'\'\'\n' + 'OWNER_ID = \'\'\''+chat_id+'\'\'\'\n')
    
    print('\nstarting the bot!')
    # ctrl+z per fermare!
    print('\033[32mctr+z\033[0m to stop\n')
    time.sleep(7)
    while True:
        try:
            open('TelegramShy.py','r')
            os.system('python3 TelegramShy.py')
        except FileNotFoundError:
            print('File non trovato!')
            print('I\'ll download it for you :3')
            count = 3
            while ( (not(os.system('wget https://raw.githubusercontent.com/Oples/Telegram-bot-test/master/TelegramShy.py') == 0)) and (count > 0)):
                time.sleep(1)
                print('Retrying ...')
                count -= 1
            if (count == 0):
                print('Errore nel scaricare il file!')
                sys.exit(1)
else:
    print('Windows coming soon ...')

