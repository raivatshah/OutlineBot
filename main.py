""" 
Simple Telegram Bot to automate the process of obtaining Outline.com links. 

Created by Raivat Shah in 2019. Updated in 2020
"""
# Imports
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Command Handlers. Usually take two arguments: bot and update. 
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome! Pls send '/read + url of the article' to obtain Outline.com link")

def read(update, context):
    # Processing Outline
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(driver_path="../chromedriver", chrome_options=chrome_options, 
    service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    browser.get('https://www.outline.com')
    linkbar = browser.find_element_by_id('source')
    linkbar.send_keys(context.args) # pass in the link from the argument
    linkbar.send_keys(Keys.ENTER)
    time.sleep(10)
    # send the link back
    context.bot.send_message(chat_id=update.message.chat_id, text=browser.current_url)
    
def main():
    # Create updater and pass in Bot's auth key. 
    updater = Updater(token='your_bot_auth_key_here', use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher
    # answer commands
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('read', read))
    # start the bot
    updater.start_polling()
    # Stop
    updater.idle()

if __name__ == '__main__':
    main()
