# coding=utf-8
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from bs4 import BeautifulSoup
import re
import logging

class MenuCache:
    def __init__(self):
        self.update()
    def update(self):
        logging.info("Updating menu from Novae website...")
        self.menu_fr = CernMenu(in_english = False)
        self.menu_en = CernMenu(in_english = True)
        logging.info("Menu update done.")

class CernMenu:
    def __init__(self, in_english = False):
        if (in_english):
            self.lang = 'en'
            content = urlopen('http://www.novae-restauration.ch/menus/menu-week/cern/21?lang=en').read()
        else:
            self.lang = 'fr'
            content = urlopen('http://www.novae-restauration.ch/menus/menu-week/cern/21').read()
        soup = BeautifulSoup(content, 'lxml')
        self.menu_types = soup.find_all(class_='typeMenu')
        self.num_menus = len(self.menu_types)
        self.dow = soup.find_all(class_='EnteteMenu')
        self.all_menus = soup.find_all('span')

    def day_menu(self, downum):
        if not (0 <= downum < len(self.dow)):
            if self.lang == 'en':
                return "The restaurant is closed"
            else:
                return "Le restaurant est fermé"
        string = ""
        day = self.dow[downum]
        string += '<i>'+day.string+'</i>\n\n'
        for i in range(0,self.num_menus):
            string += '<b>- '+self.menu_types[i].string+' -</b>\n'+re.sub('( [ \n])+', '', self.all_menus[self.num_menus*downum+i].string)+'\n\n'
        return string

    def week_menu(self):
        string = ""
        for day in range(0,len(self.dow)):
            string += self.day_menu(day)+'__________________\n\n'
        return string
