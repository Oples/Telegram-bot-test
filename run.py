import os
import getpass

if (os.name == 'posix'):
    print('Initializing the Installation')
    passwd = getpass.getpass('ho bisogno di essere root!\npasswd:\033[7m\033[5m\033[0m')
    
    if (os.system('pip3 >> /dev/null') == 0):
        print("[\033[32mok\033[0m] pip3")
        
    else:
        print('[\033[31mFail\033[0m] pip3')
        print('\ndevi installare pip3')
        print('Lo installo io?')
        print('\nInstallando ..')
        os.system('''echo -e "'''+passwd+'''\n" | sudo -S apt-get install python3-pip''')
        
    print('[installando le librerie]')
    if (os.system('''echo -e "'''+passwd+'''\n" | sudo -SH pip3 install Cleverbot --upgrade >> /dev/null''') == 0):
        print("[\033[32mok\033[0m] Cleverbot")
    else:
         print('[\033[31mFail\033[0m] Cleverbot')
            
    if (os.system('''echo -e "'''+passwd+'''\n" | sudo -SH pip3 install python-telegram-bot --upgrade >> /dev/null''') == 0):
        print("[\033[32mok\033[0m] python-telegram-bot")
    else:
         print('[\033[31mFail\033[0m] python-telegram-bot')
            
    if (os.system('''echo -e "'''+passwd+'''\n" | sudo -SH pip3 install youtube-dl --upgrade >> /dev/null''') == 0):
        print("[\033[32mok\033[0m] youtube-dl")
    else:
         print('[\033[31mFail\033[0m] youtube-dl')
            
    print('\nDone!')
    print('all librarys installed now starting the bot!')