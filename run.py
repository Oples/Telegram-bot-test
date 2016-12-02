import os
import getpass

if (os.name == 'posix'):
    print('Initializing the Installation')
    
    if (os.system('pip3 >> /dev/null') == 0):
        print("[\033[32mok\033[0m] pip3")
        passwd = getpass.getpass('ho bisogno di essere root per installare le librerie\npasswd: ')
        
    else:
        print('[\033[31mFail\033[0m] pip3')
        print('\ndevi installare pip3')
        print('\nScrivi: sudo apt-get install python3-pip')
        passwd = getpass.getpass('\no inserisci la password di sudo per installarlo: ')
        print('\nInstallando ..')
        os.system('echo -e "'+passwd+'\n" | sudo -S apt-get install python3-pip')
        
    print('[installando le librerie]')
    os.system('echo -e "'+passwd+'\n" | sudo -SH pip3 install Cleverbot --upgrade')
    os.system('echo -e "'+passwd+'\n" | sudo -SH pip3 install python-telegram-bot --upgrade')
    os.system('echo -e "'+passwd+'\n" | sudo -SH pip3 install youtube-dl --upgrade')
    print('\nDone!')
    print('all librarys installed now starting the bot!')
