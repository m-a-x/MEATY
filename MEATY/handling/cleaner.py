from MEATY.shared.tools import *
import pandas as pd
import numpy as np
import datetime as dt
from pytesseract import image_to_string
from PIL import Image
from itertools import combinations as combos
import imagehash as ihash



def get_date(x): return x.date()
def get_dayofweek(x): return x.dayofweek


# In[ ]:


def hash_img(post_id, group_folder):
    """ creates a wavelet image hash to find duplicate
    or similar posted imgs"""
    img_fn = group_folder + '/imgs/' + post_id + '.jpg'
    img = Image.open(img_fn)
    return (post_id, str(ihash.whash(img, hash_size=16)))


# In[ ]:


def hash_imgs_in_group(group_name='cornell', save_csv=True):
    """ hashes all of the images from the given school's posts """
    group_folder = '../' + group_name
    backward_scrape_exists = os.path.exists(
        group_folder + '/temp_memedata_backward.csv')
    forward_scrape_exists = os.path.exists(
        group_folder + '/temp_memedata_forward.csv')
    if backward_scrape_exists:
        dfb = pd.read_csv(group_folder + '/temp_memedata_backward.csv')
    if forward_scrape_exists:
        dff = pd.read_csv(group_folder + '/temp_memedata_forward.csv')
    if forward_scrape_exists and backward_scrape_exists:
        print('--> Found both backward and forward files.')
        df = pd.concat([dfb, dff])
    elif forward_scrape_exists:
        print('--> Found only a forward file.')
        df = dff
    elif backward_scrape_exists:
        print('--> Found only a backward file.')
        df = dfb
    else:
        print('ERROR: Cannot find files!')
        return
    list_ids = df['id'].values
    imhash = [hash_img(post_id, group_folder) for post_id in list_ids]
    df['post_time'] = pd.DatetimeIndex(df['post_time'])
    df['post_date'] = df['post_time'].apply(get_date)
    df['post_hour'] = df['post_time'].apply(lambda x: x.hour)
    df.sort_values(by='post_time', inplace=True)
    hash_df = pd.DataFrame(imhash, columns=['id', 'img_hash'])
    df_hashed = pd.merge(df, hash_df)
    df_hashed = dedupe_raw_hashed(df_hashed)
    if save_csv:
        df_hashed.to_csv(
            group_folder + '/raw_memedata_hashed.csv', index=False)
    return df_hashed


# In[ ]:


def process_raw_posts(list_of_groups=['cornell', 'harvard', 'yale', 'princeton',
                                      'columbia', 'dartmouth', 'penn', 'brown'],
                      save_csv=True):
    """ preprocess many groups' post data in ~parallel~ """
    df_list = threads(8, list_of_groups, hash_imgs_in_group)
    df_all = pd.concat(df_list)
    df_all.set_index('id', inplace=True)
    if save_csv:
        df_all.to_csv('../all_memedata_dedupe.csv')
    return df_all


# In[ ]:


def aggregate_member_data(list_of_groups=['cornell', 'harvard', 'yale', 'princeton',
                                          'columbia', 'dartmouth', 'penn', 'brown'],
                          save_csv=True):
    """ aggregates the output from multiple groups' member data """
    
    def strp_date(x): return datetime.datetime.strptime(x, '%B %d, %Y').date()
    df_list = []
    for group_name in list_of_groups:
        member_data_path = '../' + group_name + '/memberdata.csv'
        df = pd.read_csv(member_data_path, parse_dates=['date'])
        df['group'] = group_name
        df.sort_values('date', inplace=True)
        df_list.append(df)
    df_all = pd.concat(df_list)
    df_all['date'].loc[df_all['date'].str.contains('about', na=False)] = '2017-10-30'
    df_all['date'].loc[df_all['date'] == 'February 4, 2017'] = '2017-02-04'
    df_all['date'] = pd.DatetimeIndex(df_all['date'])
    if save_csv:
        df_all.to_csv('../all_member_data.csv')
    return df_all


# In[ ]:


def dedupe_raw_hashed(df):
    """ deduplicates posts based on img hash, post time, poster name, and post url """
    df_dedupe = df.drop_duplicates(
        ['img_hash', 'post_time', 'poster_name', 'url'], keep='first')
    return df_dedupe

