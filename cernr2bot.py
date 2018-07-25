# coding=utf-8
import sys
import time
import datetime
import telepot
import schedule
from telepot.namedtuple import ReplyKeyboardMarkup,KeyboardButton
from telepot.loop import MessageLoop
from novae import MenuCache

today = datetime.datetime.today().weekday()

def send_day_selector(chat_id):
    keyboard = ReplyKeyboardMarkup(keyboard=[
                   [KeyboardButton(text='Today')],
                   [KeyboardButton(text='Tomorrow')],
                   [KeyboardButton(text='Friday')],
                   [KeyboardButton(text='All week')],
                   [KeyboardButton(text='Je parle français')],
               ])
    bot.sendMessage(chat_id, 'I can tell you the menu for CERN Restaurant 2. Tell me the day.', reply_markup=keyboard)

def send_day_selector_fr(chat_id):
    keyboard = ReplyKeyboardMarkup(keyboard=[
                   [KeyboardButton(text='Aujourd\'hui')],
                   [KeyboardButton(text='Demain')],
                   [KeyboardButton(text='Vendredi')],
                   [KeyboardButton(text='Toute la semaine')],
                   [KeyboardButton(text='I speak English')],
               ])
    bot.sendMessage(chat_id, 'Je peux vous dire le menu au CERN Restaurant 2. Dites-moi le jour.', reply_markup=keyboard)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        command = msg['text'].lower()
        if command == 'all week':
            bot.sendMessage(chat_id, menus.menu_en.week_menu(), parse_mode='HTML')
        elif command == 'today':
            bot.sendMessage(chat_id, menus.menu_en.day_menu(today), parse_mode='HTML')
        elif command == 'tomorrow':
            bot.sendMessage(chat_id, menus.menu_en.day_menu(today+1), parse_mode='HTML')
        elif command == 'monday':
            bot.sendMessage(chat_id, menus.menu_en.day_menu(0), parse_mode='HTML')
        elif command == 'tuesday':
            bot.sendMessage(chat_id, menus.menu_en.day_menu(1), parse_mode='HTML')
        elif command == 'wednesday':
            bot.sendMessage(chat_id, menus.menu_en.day_menu(2), parse_mode='HTML')
        elif command == 'thursday':
            bot.sendMessage(chat_id, menus.menu_en.day_menu(3), parse_mode='HTML')
        elif command == 'friday':
            bot.sendMessage(chat_id, menus.menu_en.day_menu(4), parse_mode='HTML')
        elif command == 'toute la semaine':
            bot.sendMessage(chat_id, menus.menu_fr.week_menu(), parse_mode='HTML')
        elif command == 'aujourd\'hui':
            bot.sendMessage(chat_id, menus.menu_fr.day_menu(today), parse_mode='HTML')
        elif command == 'demain':
            bot.sendMessage(chat_id, menus.menu_fr.day_menu(today+1), parse_mode='HTML')
        elif command == 'lundi':
            bot.sendMessage(chat_id, menus.menu_fr.day_menu(0), parse_mode='HTML')
        elif command == 'mardi':
            bot.sendMessage(chat_id, menus.menu_fr.day_menu(1), parse_mode='HTML')
        elif command == 'mercredi':
            bot.sendMessage(chat_id, menus.menu_fr.day_menu(0), parse_mode='HTML')
        elif command == 'jeudi':
            bot.sendMessage(chat_id, menus.menu_fr.day_menu(0), parse_mode='HTML')
        elif command == 'vendredi':
            bot.sendMessage(chat_id, menus.menu_fr.day_menu(0), parse_mode='HTML')
        elif command == u'je parle français':
            send_day_selector_fr(chat_id)
        else:
            send_day_selector(chat_id)
    else:
        send_day_selector(chat_id)

# Update from novae website every day
menus = MenuCache()
schedule.every().day.at("10:30").do(menus.update)

# Configure bot
TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    today = datetime.datetime.today().weekday()
    schedule.run_pending()
    time.sleep(10)