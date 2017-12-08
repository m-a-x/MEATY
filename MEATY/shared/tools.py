from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
import time
import re
import datetime
from dateutil.relativedelta import relativedelta as time_ago
from dateutil.parser import parser
import pandas as pd
import numpy as np
import threading
import requests
import getpass
import string
import random
import queue
import os


def make_folder(fn):
    """
    Creates a folder fn if it doesn't exist
    """
    if not os.path.exists(fn):
        os.makedirs(fn)


def threads(num_threads, data, cb_run, *args, **kwargs):
    """
    Threads any function with any data with as many threads as you want (be careful)
    param num_threads: How many threads you want to Run
    type num_threads: int
    param data: The data that you want to parse through
    type data: list
    param cb_run: the function you want to use to parse the data
    type cb_run: function
    """
    q = queue.Queue()
    item_list = []
    def _thread_run():
        while True:
            item = q.get()
            try:
                item_list.append(cb_run(item, *args, **kwargs))
            except Exception:
                pass
            q.task_done()

    for i in range(num_threads):
        t = threading.Thread(target=_thread_run)
        t.daemon = True
        t.start()

    # Fill the Queue with the data to process
    for item in data:
        q.put(item)

    # Start processing the data
    q.join()
    return item_list
        
    
def make_nested_folders(folder_structure=None):
    if folder_structure is not None:
        for parent_folder, children in folder_structure.items():
            make_folder(parent_folder)
            for child_folder in children:
                make_folder(parent_folder + '/' + child_folder)
                

def get_login_credentials(fb_email_or_phone=None, fb_pass=None):
    if not fb_email_or_phone:
        fb_email_or_phone = input('facebook email or phone:  ')
    if not fb_pass:
        fb_pass = getpass.getpass('facebook password:  ')
    return fb_email_or_phone, fb_pass


def login_to_fb(start_url='https://www.facebook.com/photo.php?fbid=923222194492878&set=g.333018410387920&type=1&theater&ifg=10',
                fb_email_or_phone=None, fb_pass=None,
                path_to_chromedriver=None):
    if not path_to_chromedriver:
        path_to_chromedriver = os.path.abspath('chromedriver')
    fb_email_or_phone, fb_pass = get_login_credentials(fb_email_or_phone=fb_email_or_phone,
                                                       fb_pass=fb_pass)
    browser_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    browser_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(path_to_chromedriver,
                               chrome_options=browser_options)
    browser.get(start_url)
    email_phone_inp, pass_inp = browser.find_elements_by_class_name('inputtext')[:2]
    email_phone_inp.click()
    email_phone_inp.send_keys(fb_email_or_phone)
    pass_inp.click()
    pass_inp.send_keys(fb_pass)
    pass_inp.send_keys(Keys.ENTER)
    return browser

        
def generate_puid(n=12):
    """
    Generates a simple n-character uuid with no weird characters or non unicode bullshit
    """
    chars = list(string.ascii_lowercase) + list(string.ascii_uppercase) \
                + [str(i) for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    puid = ""
    for i in range(n):
        puid += random.choice(chars)
    return puid




def escape_popup(browser):
    base_page = browser.find_element_by_xpath('//html')
    base_page.send_keys(Keys.ESCAPE)
    



def find_next_button(browser, time_direction):
    arrows = browser.find_elements_by_class_name('snowliftPager')
    if time_direction == 'forward':
        next_post_button = arrows[0]
    else:
        next_post_button = arrows[1]
    return next_post_button


