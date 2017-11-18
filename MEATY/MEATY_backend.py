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
import requests
import getpass
import string
import random
import os


def make_folder(fn):
    """
    Creates a folder fn if it doesn't exist
    """
    if not os.path.exists(fn):
        os.makedirs(fn)

        
def make_nested_folders(folder_structure=None, up_one_dir=True):
    if folder_structure is not None:
        for parent, children in folder_structure.items():
            if up_one_dir:
                parent_folder = '../' + parent
            else:
                parent_folder = parent
            make_folder(parent_folder)
            for child_folder in children:
                make_folder(parent_folder + '/' + child_folder)
                

def get_login_credentials(fb_email_or_phone=None, fb_pass=None):
    if not fb_email_or_phone:
        fb_email_or_phone = input('facebook email or phone:  ')
    if not fb_pass:
        fb_pass = getpass.getpass('facebook password:  ')
    return fb_email_or_phone, fb_pass

        
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


def process_profile_html(profile_block):
    member_data = {}
    name, fb_id = process_name_fbid(profile_block)
    member_data['name'] = name
    member_data['fb_id'] = fb_id
    ref, date = process_member_add_data(profile_block)
    member_data['ref'] = ref
    member_data['date'] = date
    affil = profile_block.find(attrs={'class':'_17tq'}).text
    member_data['affil'] = affil
    return member_data


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


