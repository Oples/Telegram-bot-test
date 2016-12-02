import os
import sys
import time
import getpass

if (os.name == 'posix'):
    print('Initializing the Installation\n')
    print('Ciao ' + os.environ.get('USER') + '!')
    print('propietario di '+os.popen('cat /etc/hostname').read())
    while True:
        passwd = getpass.getpass('ho bisogno di essere root!\npasswd:\033[7m\033[5m\033[0m')
        if passwd or os.environ.get('USER') == 'pi':
            break
    
    if (os.system('pip3 >> /dev/null') == 0):
        print("\n[\033[32mok\033[0m] pip3")
        
    else:
        print('[\033[31mFail\033[0m] pip3')
        print('\ndevi installare pip3')
        print('Lo installo io?')
        print('\nInstallando ..')
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
            
    if (os.system('''echo -e "'''+passwd+'''\n" | sudo -SH pip3 install youtube-dl >> /dev/null''') == 0):
        print("[\033[32mok\033[0m] youtube-dl")
    else:
         print('[\033[31mFail\033[0m] youtube-dl')
            
    if (os.system('''wget https://raw.githubusercontent.com/terryyin/google-translate-python/master/translate.py -o translate.py >> /dev/null''') == 0):
        print("[\033[32mok\033[0m] translate")
    else:
         print('[\033[31mFail\033[0m] translate')
            
    print('Done!\n')
    print('all libraries installed now')
    print('starting the bot!')
    print('\033[32mctr+z to stop\033[0m\n')
    time.sleep(7)
    while True:
        try:
            open('TelegramShy.py','r')
            os.system('python3 TelegramShy.py')
        except FileNotFoundError:
            print('File non trovato!')
            print('Lo scarico :3')
            count = 3
            while ( (not(os.system('wget https://raw.githubusercontent.com/Oples/Telegram-bot-test/master/TelegramShy.py') == 0)) and (count > 0)):
                time.sleep(1)
                print('Retrying ...')
                count -= 1
            print('Errore nel scaricare il file!')
            sys.exit(1)
else:
    print('Windows coming soon ...')

