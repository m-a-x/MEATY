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


def save_meme_scrape(df, fn):  # will extend to database in future
    if os.path.exists(fn):
        df.to_csv(fn,
                  mode='a',
                  header=False,
                  index=False)
    else:
        df.to_csv(fn,
                  mode='w',
                  index=False)


def escape_popup(browser):
    base_page = browser.find_element_by_xpath('//html')
    base_page.send_keys(Keys.ESCAPE)
    
    
def download_img(browser, puid, group_name):
    img = browser.find_element_by_class_name('spotlight')
    img_src = img.get_attribute('src')
    img_fn = group_name + '/imgs/' + puid + '.jpg'
    img_data = requests.get(img_src).content
    with open(img_fn, 'wb') as handler:
        handler.write(img_data)


def download_html(browser, puid, page_type, group_name):
    source = browser.page_source
    html_fn = group_name + '/html-' + page_type +'/' + puid + '.html'
    with open(html_fn, 'w', encoding='utf-8') as handler:
        handler.write(source)


def switch_tabs(browser, desired_tab):
    tabs = browser.window_handles
    browser.switch_to.window(browser.window_handles[desired_tab])
    while browser.current_window_handle != tabs[desired_tab]:
        time.sleep(.1)
        browser.switch_to.window(browser.window_handles[desired_tab])
    return browser


def find_next_button(browser, time_direction):
    arrows = browser.find_elements_by_class_name('snowliftPager')
    if time_direction == 'forward':
        next_post_button = arrows[0]
    else:
        next_post_button = arrows[1]
    return next_post_button


def process_poster_name(browser):
    poster_name = browser.find_element_by_class_name('_hli')
    poster_name = poster_name.text
    return poster_name


def process_caption(browser):
    try:
        caption = browser.find_element_by_class_name('_5pbx')
        caption = ' '.join(caption.text.split('\n'))
    except:
        caption = None
    return caption


def process_title(browser):
    try:
        title = browser.find_element_by_class_name('_l53').text
    except:
        print('no title')
        title = None
    return title


def process_price(browser):
    try:
        price = browser.find_element_by_class_name('_l57').text
    except:
        print('no price')
        price = None
    return price


def process_caption(browser):
    try:
        caption = browser.find_element_by_class_name('_5pbx')
        caption = ' '.join(caption.text.split('\n'))
    except:
        caption = None
    return caption

def process_timestamp(browser):
    post_time = browser.find_elements_by_class_name('_39g5')
    while len(post_time) == 0:
        post_time = browser.find_elements_by_class_name('_39g5')
    post_time = post_time[::-1]
    while True:
        for pt in post_time:
            try:
                ptime = pt.find_element_by_css_selector('abbr')
                ptime = ptime.get_attribute('title')
                return ptime
            except:
                continue
        post_time = browser.find_elements_by_class_name('_39g5')


