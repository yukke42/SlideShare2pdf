import argparse
import os
import subprocess
import sys
import time
import urllib

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

DL_INTERVAL = 0.5
DL_DIR = '~/Downloads'
TMP_DIR = 'tmp'


def main(slideshare_url: str):
    try:
        resp = requests.get(slideshare_url)
        resp.raise_for_status()
    except Exception as e:
        sys.exit('Could not download {}: {}'.format(slideshare_url, e))

    soup = BeautifulSoup(resp.text, 'lxml')
    images = soup.find_all('img', attrs={'class': 'slide_image'})
    slide_title = soup.find('span', attrs={'class': 'j-title-breadcrumb'}).text.strip()

    if not images:
        sys.exit('Could not find slides.')

    # download images
    image_filepath_list = []
    url_basename = os.path.basename(slideshare_url)
    os.makedirs(TMP_DIR, exist_ok=True)
    print('It takes about {} sec to download images of slide.'.format(int(DL_INTERVAL * len(images))))
    for i, image in enumerate(tqdm(images), start=1):
        image_url = image['data-full']
        image_filename = '{}-{}.jpg'.format(url_basename, i)
        image_filepath = os.path.join('tmp', image_filename)

        if not os.path.exists(image_filepath):
            urllib.request.urlretrieve(image_url, filename=image_filepath)
            time.sleep(DL_INTERVAL)

        image_filepath_list.append(image_filepath)

    # convert images to pdf
    image_filepaths_str = ' '.join(sorted(image_filepath_list))
    output_pdf_filepath = os.path.join(DL_DIR, slide_title + '.pdf')
    cmd = 'convert {} -quality 100 {}'.format(image_filepaths_str, output_pdf_filepath)
    print('Converting downloaded images to pdf ...')
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        sys.exit('Could not convert slides to PDF: {}'.format(e))

    subprocess.run('rm -f {}/{}*.jpg'.format(TMP_DIR, url_basename), shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A python script to help you back up your SlideShare presentations to PDF.')
    parser.add_argument('-i', '--input',
                        help='SlideShare URL to be processed,')
    args = parser.parse_args()
    main(args.input)
