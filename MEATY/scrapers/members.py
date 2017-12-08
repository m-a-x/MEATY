from MEATY.shared.tools import *
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
import time
import re
import pandas as pd
import numpy as np



def process_profile_html(profile_block):
    member_data = {}
    name, fb_id = process_name_fbid(profile_block)
    member_data['name'] = name
    member_data['fb_id'] = fb_id
    ref, date = process_member_add_data(profile_block)
    member_data['ref'] = ref
    member_data['date'] = date
    affil = profile_block.find(attrs={'class': '_17tq'}).text
    member_data['affil'] = affil
    return member_data


def process_name_fbid(block):
    name_id_block = block.find_all('a')
    for elem in name_id_block:
        name = elem.text
        if name != '':
            fb_id = str(name_id_block).split('id=')[1].split('&amp;')[0]
            break
    return name, int(fb_id)


def process_member_add_data(profile_block):
    today = datetime.date.today()
    try:
        added_by = profile_block.find(string=re.compile('Added by'))[9:]
    except:
        added_by = None
        try:
            date_added = profile_block.find(class_='timestampContent').text
        except:
            date_added = profile_block.find(class_='fsm fwn fcg').text
            if 'Created group on December 5, 2016':
                # datetime.date(2016, 12, 5)
                date_added = ' '.join(date_added.split(' ')[-3:])
                added_by = 'GROUP CREATOR'
            else:
                date_added = None
                added_by = None
                print('<< PROBLEMATIC >>\n', profile_block.prettify())
            return added_by, date_added
        if 'Joined about' in date_added:
            timedelta = int(date_added.split(' ')[2])
            if 'months' in date_added:
                date_added = today - time_ago(months=+timedelta)
            elif 'years' in date_added:
                date_added = today - time_ago(years=+timedelta)
            return None, date_added
        elif '201' not in date_added:
            date_added = date_added + ", 2017"
        date_added = datetime.datetime.strptime(date_added, '%B %d, %Y').date()
        return added_by, date_added
    if '2016' in added_by              or '2017' in added_by              or '2015' in added_by              or '2014' in added_by:
        added_by, date_added = added_by.split(' on ')
        date_added = datetime.datetime.strptime(date_added, '%B %d, %Y').date()
    elif ' Today' in added_by:
        added_by = added_by.rstrip(' Today')
        date_added = today
    elif ' Yesterday' in added_by:
        added_by = added_by.rstrip(' Yesterday')
        date_added = today - time_ago(days=+1)
    else:
        print('added_by/date_added: Cant parse', added_by)
        added_by = '~~' + added_by
        date_added = added_by
    return added_by, date_added


# In[9]:


def html_to_df(soup=None, html_path='../../cbsm.html', save_csv=True):
    if soup is None:
        with open(html_path) as f:
            soup = BS(f, 'lxml')
    ppl = soup.find_all(attrs={'class': "_6a _5u5j _6b"})
    member_data = []
    for memester in ppl:
        member_data.append(process_profile_html(memester))
    member_df = pd.DataFrame(member_data).set_index('fb_id')
    if save_csv:
        member_df.to_csv('columbia-member_data.csv')
    return member_df


# In[8]:


#   NEED TO FIX for case where no old df
def update_members(fb_email_or_phone=None, fb_pass=None, old_df=None, save_csv=True):
    browser = login_to_fb(fb_email_or_phone, fb_pass)
    soup = BS(browser.page_source, 'lxml')
    ppl = soup.find_all(attrs={'data-name': "GroupProfileGridItem"})
    last_on_page = ppl[-1]
    name, fb_id = process_name_fbid(last_on_page)
    new_people = old_df[old_df.fb_id == fb_id].shape[0] == 0
    i = 1
    time.sleep(1.5)
    while new_people:
        print(i)
        i += 1
        try:
            load_more = browser.find_element_by_class_name(
                'uiMorePagerPrimary')
        except:
            time.sleep(1)
            load_more.click()
        load_more.click()
        soup = BS(browser.page_source, 'lxml')
        ppl = soup.find_all(attrs={'data-name': "GroupProfileGridItem"})
        last_on_page = ppl[-1]
        name, fb_id = process_name_fbid(last_on_page)
        new_people = old_df[old_df.fb_id == fb_id].shape[0] == 0
        time.sleep(1.5)
    new_ppl_df = html_to_df(soup, save_csv=False)
    new_ppl_ids = np.array(list(set(new_ppl_df.index) - set(old_df.fb_id)))
    new_ppl_df = new_ppl_df.loc[new_ppl_ids].reset_index()
    new_df = pd.concat([new_ppl_df, old_df])
    if save_csv:
        fn_str = 'member_data_' + datetime.datetime.today().strftime('%m-%d-%Y_%H-%M') + '.csv'
        new_df.set_index('fb_id').to_csv(fn_str)
    return new_df


# In[5]:


def load_more_members(browser, group_name='cornell'):
    i = 0
    print("+++++++   FRESH START   +++++++")
    while True:
        print(i)
        i += 1
        try:
            load_more = browser.find_element_by_class_name(
                'uiMorePagerPrimary')
            load_more.click()
        except:
            time.sleep(1)
            try:
                load_more = browser.find_element_by_class_name(
                    'uiMorePagerPrimary')
                load_more.click()
            except:
                time.sleep(4)
                try:
                    load_more = browser.find_element_by_class_name(
                        'uiMorePagerPrimary')
                    load_more.click()
                except:
                    print('-------   DONE   -------')
                    alt_html = browser.execute_script(
                        "return document.body.innerHTML")
                    soup_alt = BS(alt_html, 'lxml')
                    indf = html_to_df(soup_alt, save_csv=False)
                    indf.to_csv(group_name + '-html_alt.csv')
                    html = browser.page_source
                    soup = BS(html, 'lxml')
                    df = html_to_df(soup, save_csv=False)
                    df.to_csv(group_name + '-html.csv')
                    return browser, df, indf



#
#browser = login_to_fb('https://www.facebook.com/groups/makecornellmemeagain/members/?order=date')
#b, df, indf = load_more_members(browser)
#
