import copy
from datetime import datetime, timedelta
import os
import requests
from glob import glob


installpath = os.path.dirname(os.path.realpath(__file__))
wget_headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
remote_url = 'https://raw.githubusercontent.com/lovit/petitions_archive/master/'
    
def fetch(data_dir=None):
    """
    Argument
    --------
    data_dir : str
        Data storage directory
    """

    action = None
    while action is None:
        message = input("It needs about 0.65 GB storage. Continue to download? ([Y]es, [N]o)\n")
        message = message.lower()
        if message == 'no' or message == 'n':
            action = 'no'
        if message == 'yes' or message == 'y':
            action = 'yes'
        else:
            print("Insert yes or no")

    if action == 'no':
        print("Stop downloading")
        return

    if data_dir is None:
        data_dir = '{}/data/'.format(installpath)
    paths = glob('{}/petitions_*'.format(data_dir))
    local_lists = {name.split('/')[-1] for name in paths}
    remote_lists = download_as_str('{}/files'.format(remote_url))
    remote_lists = {name.strip() for name in remote_lists.split('\n') if name.strip()}
    remote_lists = {name for name in remote_lists
        if not (name in local_lists)}

    if not remote_lists:
        print('All data are downloaded')
        return

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for name in sorted(remote_lists):
        source = '{}/{}'.format(remote_url, name)
        dest = '{}/{}'.format(data_dir, name)
        download_a_file(source, dest)
        print('downloaded {}'.format(name))

def download_as_str(url):
    try:
        r = requests.get(url, stream=True, headers=wget_headers)
        docs = ''.join([chunk.decode('utf-8') for chunk in r.iter_content(chunk_size=1024)])
        return docs
    except Exception as e:
        print('Failed to download version file')
        return ''

def download_a_file(url, fname):
    """
    Arguments
    --------
    url : str
        URL address of file to be downloaded
    fname : str
        Download file address
    Returns
    -------
    flag : Boolean
        It return True if downloading success else return False
    """

    fname = os.path.abspath(fname)
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    try:
        r = requests.get(url, stream=True, headers=wget_headers)
        with open(fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(e)
        return False

def convert_str_date_to_datetime(string_date):
    try:
        return datetime.strptime(string_date, '%Y-%m-%d')
    except Exception as e:
        raise ValueError('Failed to Convert String to Datetime %s' % str(e))

def is_first_day_of_a_month(date):
    d = copy.deepcopy(date)
    d -= timedelta(days=1)
    return d.month != date.month

def is_last_day_of_a_month(date):
    d = copy.deepcopy(date)
    d += timedelta(days=1)
    return d.month != date.month
