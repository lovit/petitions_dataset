import argparse
import json
from glob import glob
import os
import zipfile


def read_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def json_to_strf(json_obj):
    return json.dumps(json_obj, ensure_ascii=False)

def write(output_directory, fname, temps):
    path = '{}/petitions_{}'.format(output_directory, fname)
    with open(path, 'w', encoding='utf-8') as f:
        for row in temps:
            f.write('{}\n'.format(row))
    print('created {}'.format(fname))
    return path

def compress_and_delete(source):
    zippath = source + '.zip'
    zip_instance = zipfile.ZipFile(zippath, 'w')
    zip_instance.write(source, compress_type=zipfile.ZIP_DEFLATED)
    print('compressed {}'.format(source))
    os.remove(source)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_directory', type=str, default='../petitions_scraper/output', help='JSON storage directory')
    parser.add_argument('--output_directory', type=str, default='../petitions_archive/', help='Petitions archive directory')
    parser.add_argument('--begin_yymm', type=str, default='2018-09', help='JSON storage directory')
    parser.add_argument('--end_yymm', type=str, default='2018-08', help='JSON storage directory')
    parser.add_argument('--compress', dest='compress', action='store_true')

    args = parser.parse_args()
    json_directory = args.json_directory
    output_directory = args.output_directory
    begin_yymm = args.begin_yymm
    end_yymm = args.end_yymm
    compress = args.compress

    paths = glob('{}/*.json'.format(json_directory))
    paths = sorted(paths, key=lambda x:int(x.split('/')[-1][:-5]))

    n = len(paths)
    print('{} files are found'.format(n))

    fname = ''
    temps = []

    for i, path in enumerate(paths):
        if i % 10000 == 0:
            print('sorting json files {} / {} ...'.format(i, n))

        # read json
        json_obj = read_json(path)

        # date
        begin = json_obj['begin']
        yymm = begin[:7]
        if yymm < begin_yymm:
            continue
        if yymm > end_yymm:
            break

        # check status
        status = json_obj['status']
        if status == '청원진행중':
            continue

        # strf format
        del json_obj['crawled_at']
        json_strf = json_to_strf(json_obj)

        # write dump data
        if fname != yymm and temps:
            source = write(output_directory, fname, temps)
            if compress:
                compress_and_delete(source)
            temps = []

        fname = yymm
        temps.append(json_strf)

    print('sorting {} json files have been done.'.format(n))

    if temps:
        source = write(output_directory, fname, temps)
        if compress:
            compress_and_delete(source)

    files = glob('{}/petitions_*'.format(output_directory))
    files = sorted([p.split('/')[-1] for p in files])
    if compress:
        files = [p for p in files if p[-4:] == '.zip']
    else:
        files = [p for p in files if p[-4:] != '.zip']
    with open('{}/files'.format(output_directory), 'w', encoding='utf-8') as f:
        for p in files:
            f.write('{}\n'.format(p))


if __name__ == '__main__':
    main()