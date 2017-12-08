from MEATY.shared.tools import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np


    
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


def scrape_memes(start_url=None, fb_email_or_phone=None, fb_pass=None,
                 group_name='noname', time_direction='forward',
                 path_to_chromedriver=None):
    meme_data = []
    if not path_to_chromedriver:
        path_to_chromedriver = os.path.abspath('chromedriver')
    group_folder = '../' + group_name
    make_nested_folders({group_folder: ['imgs', 'html-posts', 'html-reacts']})
    fn = group_folder + '/temp_memedata_' + time_direction + '.csv'
    already_started_scrape = os.path.exists(fn)
    if already_started_scrape:
        df = pd.read_csv(fn)
        start_url = df['url'].iloc[-1]
    browser = login_to_fb(start_url, fb_email_or_phone,
                          fb_pass, path_to_chromedriver)
    time.sleep(3)
    browser.get(start_url)
    time.sleep(2)
    next_post_button = find_next_button(browser, time_direction)
    if already_started_scrape:
        next_post_button.click()
        time.sleep(.2)
        next_post_button = find_next_button(browser, time_direction)
    i = 0
    while True:
        i += 1
        try:
            last_url = process_meme(browser, meme_data, group_folder=group_folder,
                                    time_direction=time_direction)
            if not last_url:
                return browser
            print('=' * 8, i, '=' * 8)
            print('\n'.join([str(s) for s in meme_data[-1].items()]))
            next_post_button.click()
        except Exception as e:
            print('1 -- ERROR -- 1:  ', e)
            try:
                time.sleep(.2)
                tabs = browser.window_handles
                while len(tabs) > 1:
                    i = len(tabs) - 1
                    tabs[i].close()
                browser = switch_tabs(browser, 0)
                next_post_button = find_next_button(browser, time_direction)
                browser.get(last_url)
                last_url = process_meme(browser, meme_data, group_folder=group_folder,
                                        time_direction=time_direction)
                if not last_url:
                    return browser
                next_post_button.click()
            except Exception as e:
                print('2 -- ERROR --2:  ', e)
                return browser


# In[ ]:


def process_reacts(browser):
    """Make album/loop detection/bugfix"""
    reacts = browser.find_elements_by_class_name(' _ipp')
    post_reacts = {'Like': 0,
                   'Love': 0,
                   'Haha': 0,
                   'Wow': 0,
                   'Sad': 0,
                   'Angry': 0,
                   'Pride': 0,
                   'Thankful': 0}
    if reacts == []:
        num_reacts = 0
        return num_reacts, post_reacts, None
    reacts_element = reacts[0].find_element_by_class_name('_2x4v')
    reacts_url = reacts_element.get_attribute('href')
    reacts_element.send_keys(Keys.ENTER)  # click()
    tab_post_reacts = browser.find_elements_by_class_name('_21ab')
    while tab_post_reacts == []:
        time.sleep(.2)
        tab_post_reacts = browser.find_elements_by_class_name('_21ab')
    tab_post_reacts = tab_post_reacts[0].find_elements_by_class_name('_3m1v')
    for react_type in tab_post_reacts:
        react_tab = react_type.find_elements_by_tag_name('span')[1]
        react_hovertext = react_tab.get_attribute('aria-label')
        text_split = react_hovertext.split()
        if 'reacted with' in react_hovertext:
            count_react, react_type = text_split[0], text_split[-1]
        elif 'reacted to this post' in react_hovertext:
            count_react, react_type = text_split[0], 'num_reacts'
        if 'K' in count_react:
            try:
                count_react = int(float(count_react.replace('K', '')) * 1000)
            except:
                pass
        else:
            count_react = int(count_react)
        if react_type != 'num_reacts':
            post_reacts[react_type] = count_react
        else:
            num_reacts = count_react
    if len(tab_post_reacts) == 1:
        num_reacts = post_reacts[list(post_reacts.keys())[0]]
    return num_reacts, post_reacts, reacts_url


# In[ ]:


def process_meme(browser, meme_data, group_folder, time_direction):
    puid = generate_puid(12)
    carousel_url = browser.current_url
    browser.execute_script("window.open('" + carousel_url + "', 'new_window')")
    browser = switch_tabs(browser, 1)
    post_time = process_timestamp(browser)
    poster_name = process_poster_name(browser)
    download_img(browser, puid, group_folder)
    escape_popup(browser)
    download_html(browser, puid, 'posts', group_folder)
    price = process_price(browser)
    post_title = process_title(browser)
    caption = process_caption(browser)
    num_reacts, post_reacts, reacts_url = process_reacts(browser)
    download_html(browser, puid, 'reacts', group_folder)
    browser.close()
    browser = switch_tabs(browser, 0)
    meme_data.append({
        'num_reacts': num_reacts,
        'likes': post_reacts['Like'],
        'loves': post_reacts['Love'],
        'hahas': post_reacts['Haha'],
        'wows': post_reacts['Wow'],
        'sads': post_reacts['Sad'],
        'angrys': post_reacts['Angry'],
        'thankfuls': post_reacts['Thankful'],
        'prides': post_reacts['Pride'],
        'title': post_title,
        'caption': caption,
        'price': price,
        'post_time': post_time,
        'poster_name': poster_name,
        'url': carousel_url,
        'reacts_url': reacts_url,
        'id': puid
    })
    temp_df = pd.DataFrame(meme_data[-1:])
    other_time_direction = list(
        set(['forward', 'backward']) - set([time_direction]))[0]
    other_time_data_path = group_folder +         '/temp_memedata_' + other_time_direction + '.csv'
    if os.path.exists(other_time_data_path):
        other_df = pd.read_csv(other_time_data_path)
        if meme_data[-1]['post_time'] in other_df['post_time'].values[-1:]                  and other_df.shape[0] > 5                  and poster_name in other_df['poster_name'].values[-1:]                  and num_reacts in other_df['num_reacts'].values[-1]:
            print('DONE')
            return False
        elif poster_name == meme_data[0]['poster_name']                  and post_time == meme_data[0]['post_time']:
            print('DONE')
            return False
    fn = group_folder + '/temp_memedata_' + time_direction + '.csv'
    save_meme_scrape(temp_df, fn)
    return carousel_url


# ### The first input of scrape_memes is the photo (as accessed by the group sidebar) url. Does not need to be correct if scrape already started; will pick up where left off.
# #### Scrape is best run across two terminals running separate jupyter notebooks with one going 'forward' in time and one going 'backward'. 
#   - to achieve this, open 2 terminals and type jupyter notebook on each
#   - duplicate MEATY.ipynb and change one of their time_direction args so one is 'forward' and the other 'backward'
#   - may crash after some time, restart and run kernel is safe
#   
# #### Scrape _should_ stop automatically once it loops on itself (approx) or when it overlaps with the opposite time_direction

# In[ ]:

#
#browser, meme_data = scrape_memes('https://www.facebook.com/photo.php?fbid=1506285966134413&set=g.1006815496091821&type=1&theater&ifg=1',
#                                  group_name='columbia', time_direction='backward')
#
