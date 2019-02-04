from glob import glob
import json
import os


class Petitions:
    """
    Usage
    -----
            >>> from petitions_dataset import Petitions

            >>> petitions = Petitions()
            >>> petitions.set_keys('category', 'title', 'content')
            >>> for category, title, content in petitions:
            >>>    # do something
    """

    def __init__(self, data_dir=None, begin_yymm='2017-08', end_yymm='2018-08'):
        if data_dir is None:
            data_dir = './'
        data_dir = os.path.abspath(data_dir)

        def match(path):
            yymm = path.split('/')[-1].split('_')[-1]
            return begin_yymm <= yymm <= end_yymm

        paths = sorted(glob('{}/petitions_*'.format(data_dir)))
        paths = [p for p in paths if match(p)]
        if not paths:
            print('Not founded matched petitions in {} ({} - {})'.format(
                data_dir, begin_yymm, end_yymm))
            print('check directory or use fetch()')

        self.paths = paths
        self.set_keys()

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

        keys = [key for key in sorted(keys)]
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

        for path in self.paths:
            with open(path, encoding='utf-8') as f:
                for line in f:
                    petition = json.loads(line.strip())
                    if isinstance(keys, str):
                        yield petition[keys]
                    else:
                        yield tuple(petition[k] for k in keys)
