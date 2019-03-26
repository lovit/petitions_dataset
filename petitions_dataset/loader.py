import copy
from datetime import datetime, timedelta
from glob import glob
import json
import os
from .utils import convert_str_date_to_datetime
from .utils import is_first_day_of_a_month
from .utils import is_last_day_of_a_month
from .utils import installpath


class Petitions:
    """
    Usage
    -----
            >>> from petitions_dataset import Petitions

            >>> petitions = Petitions() # defaul period
            >>> petitions = Petitions(begin_date='2017-08-01', end_date='2018-12-31') # set specific period
            >>> petitions.set_keys('category', 'title', 'content')
            >>> for category, title, content in petitions:
            >>>    # do something
    """

    def __init__(self, data_dir=None, begin_date='2017-08-01', end_date='2018-12-31'):
        if data_dir is None:
            data_dir = '{}/data/'.format(installpath)
        data_dir = os.path.abspath(data_dir)

        self.begin = convert_str_date_to_datetime(begin_date)
        self.end = convert_str_date_to_datetime(end_date)
        self.skip_date_check = False

        if is_first_day_of_a_month(self.begin) and is_last_day_of_a_month(self.end):
            self.skip_date_check = True

        date = copy.deepcopy(self.begin)
        filenames = set()
        while date <= self.end:
            yymm = '{}-{:02}'.format(date.year, date.month)
            filenames.add('petitions_{}'.format(yymm))
            date += timedelta(days=1)

        paths = ['{}/{}'.format(data_dir, name) for name in sorted(filenames)]
        if not paths:
            print('Not founded matched petitions in {} ({} - {})'.format(
                data_dir, begin_yymm, end_yymm))
            print('check directory or use fetch()')

        self.paths = paths
        self.set_keys()
        self._len = 0 # initialize length

    def _check_keys(self, keys):
        availables = {
            'category', 'begin', 'end', 'content',
            'num_agree', 'petition_idx', 'status',
            'title', 'replies'
        }
        for key in keys:
            if not (key in availables):
                return False
        return True

    def set_keys(self, *keys):
        """
        Arguments
        ---------
        keys : str [str, ...]

            Available keys = [
                'category', 'begin', 'end', 'content',
                'num_agree', 'petition_idx', 'status',
                'title', 'replies'
            ]

        Usage
        -----
            >>> petittions = Petitions()
            >>> petitions.set_keys('category', 'title')
        """

        if not keys:
            keys = 'content'
        if isinstance(keys, str):
            keys = [keys]

        if not self._check_keys(keys):
            raise ValueError('Check keys')
        if len(keys) == 1:
            keys = keys[0]

        self.keys = keys
        
    def __iter__(self):
        """
        Yields
        ------
        Selected values

        Usage
        -----

            petitions = Petitions()
            for petition in petitions:
                # do something
        """
        keys = self.keys
        do_break = False

        for path in self.paths:
            if do_break:
                break
            with open(path, encoding='utf-8') as f:
                for line in f:
                    petition = json.loads(line.strip())
                    if not self.skip_date_check and not self._date_match(petition):
                        continue
                    if isinstance(keys, str):
                        yield petition[keys]
                    else:
                        yield tuple(petition[k] for k in keys)

    def __len__(self):
        """
        It returns number of petitions
        """
        if self._len > 0:
            return self._len

        num = 0
        do_break = False
        for path in self.paths:
            if do_break:
                break

            with open(path, encoding='utf-8') as f:
                for line in f:
                    if self.skip_date_check:
                        num += 1
                        continue
                    petition = json.loads(line.strip())
                    if not self._date_match(petition):
                        continue
                    num += 1

        self._len = num
        return self._len

    def _date_match(self, petition):
        date_strf = petition['begin']
        date = convert_str_date_to_datetime(date_strf)
        return self.begin <= date <= self.end
