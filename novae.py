import urllib2
from bs4 import BeautifulSoup
import re

class MenuCache:
    def __init__(self):
        self.update()
    def update(self):
        self.menu_fr = CernMenu(in_english = False)
        self.menu_en = CernMenu(in_english = True)

class CernMenu:
    def __init__(self, in_english = False):
        if (in_english):
            content = urllib2.urlopen('http://www.novae-restauration.ch/menus/?x=ad3f8f75fe1e353b972afcce8e375d6e&y=81dc9bdb52d04dc20036dbd8313ed055&z=135&lang=en').read()
        else:
            content = urllib2.urlopen('http://www.novae-restauration.ch/menus/?x=ad3f8f75fe1e353b972afcce8e375d6e&y=81dc9bdb52d04dc20036dbd8313ed055&z=135').read()
        soup = BeautifulSoup(content, 'lxml')
        self.menu_types = soup.find_all(class_='typeMenu')
        self.dow = soup.find_all(class_='EnteteMenu')
        self.all_menus = soup.find_all('span')

    def day_menu(self, downum):
        string = ""
        day = self.dow[downum]
        string += '<i>'+day.string+'</i>\n\n'
        for i in range(0,10):
            string += '<b>- '+self.menu_types[i].string+' -</b>\n'+re.sub('( [ \n])+', '', self.all_menus[10*downum+i].string)+'\n\n'
        return string

    def week_menu(self):
        string = ""
        for day in range(0,5):
            string += self.day_menu(day)+'__________________\n\n'
        return string