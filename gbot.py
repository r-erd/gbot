#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from telegram.ext import Updater
from bs4 import BeautifulSoup
import time
import telegram
import schedule
import logging
import traceback
from datetime import datetime
from soup import get_data, get_hash
from telegram.ext import CommandHandler


TOKEN = "enter your telegram bot token here"
CHATID = "enter your chatid here"
INTERVAL = 15  #in minutes, time between autochecks
USERNAME = "enter your username here"
PASSWORD = "enter your password here"

oldhash = "hey"
newhash = "hey"
latest_info =""
tmstamp = ""
previous_timestamp = ""
chromedriver = '/usr/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
url = "https://friedolin.uni-jena.de/qisserver/rds?state=user&type=0&topitem="


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def check(update, context):
    global tmstamp
    flag = check_grades()
    if (flag == 1):
        context.bot.send_message(chat_id=update.effective_chat.id, text=latest_info)

    elif (flag == 0):
        msg = "unchanged, last check : " + previous_timestamp
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

check_handler = CommandHandler('check', check)
dispatcher.add_handler(check_handler)
    
##########################

def get_html():
    ##################
    #sign in and get the correct html page
    try:
        browser = webdriver.Chrome(executable_path=chromedriver, options=options)
        browser.get(url)
        name = browser.find_element_by_id('asdf')
        password = browser.find_element_by_id('fdsa')
        login = browser.find_element_by_name('submit')

        name.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        login.click()

        link_notenspiegel = browser.find_element_by_link_text("Notenspiegel")
        link_notenspiegel.click() 

        checkbox_belehrung = browser.find_element_by_id("checkbox")
        checkbox_belehrung.click()

        weiter_button = browser.find_element_by_name("cont")
        weiter_button.click()

        hut_icon = browser.find_element_by_xpath("//img[@title='Leistungen anzeigen für Abschluss 82 Bachelor of Science ']")
        hut_icon.click()

        source = browser.page_source

        link_abmelden = browser.find_element_by_link_text("Abmelden")
        link_abmelden.click()
        browser.close
    except Exception:
        traceback.print_exc()
        print()
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(chat_id=CHATID, text="an error occurred while getting the html")

    return source
#work with the html code from the website
def check_grades():
    try:
        global newhash
        global oldhash
        global latest_info
        global tmstamp
        global previous_timestamp
        soup = BeautifulSoup(get_html(), 'html5lib')
        subjects = get_data(soup)
        
        oldhash = newhash
        newhash = get_hash(subjects)
        strtosend = ""
        for subject in subjects:
            for entry in subject:
                strtosend += entry
                strtosend += "\n"

            strtosend += "\n"

        strtosend = strtosend.replace("[", "", -1)
        strtosend = strtosend.replace("]", "", -1)
        strtosend = strtosend.replace("'", "", -1)

        datetimeobject = datetime.now()
        previous_timestamp = tmstamp
        tmstamp = datetimeobject.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        latest_info = strtosend
    except Exception:
        traceback.print_exc()
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(chat_id=CHATID, text="an error occurred while parsing the html")
        return 2

    if (newhash != oldhash):
        
        return 1
    else:
        return 0

def auto_check():
  bot = telegram.Bot(token=TOKEN)
  if (check_grades() == 1):
    bot.send_message(chat_id=CHATID, text=latest_info)

def debug_check():
    check_grades()
    print(latest_info)
    print("Finished")


def start():
    updater.start_polling()
    schedule.every(INTERVAL).minutes.do(auto_check)

    while True:
        schedule.run_pending()
        time.sleep(1)

start()



