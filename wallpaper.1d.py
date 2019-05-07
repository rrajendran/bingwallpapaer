#!/usr/local/bin/python3
# <bitbar.title>Bing Wallapaper</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Ramesh Rajendran</bitbar.author>
# <bitbar.author.github>rrajendran</bitbar.author.github>
# <bitbar.desc>Set desktop wallpaper from bing wallpapers</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/rrajendran/bingwallpapaer/master/bing.png</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/rrajendran/bingwallpapaer</bitbar.abouturl>
import datetime
import json
import os
import sys

import pySmartDL
from slugify import slugify
import urllib3

bing_icon="iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAABMUlEQVR4nK3UPy9EQRQF8N8+KyqlUEhI7CYi8Q20KCSi0IhEaBQiovExNAqVWjQbBRWFUiVKsSJWIxHRqBD/ir0vnrV2lzjJyc3MnXPenZn7JqeKAazgEhsYx6LmqGAzdAoo4x27sWAtxq2wjEKCZRTD4CXiawvVpChiOUHfL0Q/oS/B2z8YvSX/YALyTfJnWMdzjLsxh+HfGl1gx+clPGELexjJLmy2tUlcqfZLBfthtpqpsq7Re8RcZq4LPcEJTOME542M2iM+NqhyMOJdI6OhMDvEww9GR2hDb22i5GvLp//YGI5xEzzFfORmVfsv1ZTqGT1gJvOhjmCKKdzXaEr5OtvrxDYWcIDbmO/GaDBXo0nyuP5+DGREreCar8/IX1hGIS1xAEvob7GCFBXxsH0A+yBdhevdGHUAAAAASUVORK5CYII="


def join_path(*args):
    # Takes an list of values or multiple values and returns an valid path.
    if isinstance(args[0], list):
        path_list = args[0]
    else:
        path_list = args
    val = [str(v).strip(' ') for v in path_list]
    return os.path.normpath('/'.join(val))


dir_path = os.path.dirname(os.path.realpath(__file__))
save_dir = '/tmp/images'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def set_wallpaper(pic_path):
    if sys.platform.startswith('win32'):
        cmd = 'REG ADD \"HKCU\Control Panel\Desktop\" /v Wallpaper /t REG_SZ /d \"%s\" /f' % pic_path
        os.system(cmd)
        os.system('rundll32.exe user32.dll, UpdatePerUserSystemParameters')
    elif sys.platform.startswith('linux'):
        os.system(''.join(['gsettings set org.gnome.desktop.background picture-uri file://', pic_path]))
    elif sys.platform.startswith('darwin'):
        os.system("osascript -e 'set desktopImage to POSIX file \"" + pic_path +"\" \n tell application \"Finder\" \n set desktop picture to desktopImage \n end tell'")
    else:
        print('OS not supported.')
        return
    return


def download_old_wallpapers(minus_days=False):
    """Uses download_wallpaper(set_wallpaper=False) to download the last 20 wallpapers.
    If minus_days is given an integer a specific day in the past will be downloaded.
    """
    if minus_days:
        download_wallpaper(idx=minus_days, use_wallpaper=True)
        return
    for i in range(0, 20):  # max 20
        download_wallpaper(idx=i, use_wallpaper=True)


def download_wallpaper(idx=0, use_wallpaper=True):
    # Getting the XML File
    try:
        url = ''.join(['http://www.bing.com/HPImageArchive.aspx?format=js&idx=', str(idx), '&n=1&mkt=en-GB'])
        http = urllib3.PoolManager()
        response = http.request('GET', url)  # en-GB, because they always have 1920x1200 resolution
        if response.status != 200:
            raise Exception("Download wallpaper error: ")
    except Exception as e:
        print('Error while downloading #', idx, e)
        return
    try:
        bing_response = json.loads(response.data)

    # This is raised when there is trouble finding the image url.
    except Exception as e:
        print('Error while processing XML index #', idx, e)
        return
    # # Parsing the XML File
    for bing_images in bing_response['images']:
        url = 'http://www.bing.com' + bing_images['url']
        # Get Current Date as fileName for the downloaded Picture
        now = datetime.datetime.now()
        date = now - datetime.timedelta(days=int(idx))
        title = bing_images['title']

        pic_path = join_path(save_dir, ''.join([date.strftime(title + '_%d-%m-%Y'), '.jpg']))

        image_url = url.replace('_1366x768', '_1920x1200')

        print(title + " | bash=echo $0")

        if os.path.isfile(pic_path):
            # print('Image of', date.strftime('%d-%m-%Y'), 'already downloaded.')
            if use_wallpaper and idx == 0:
                set_wallpaper(pic_path)
            return
        # print('Downloading: ', date.strftime('%d-%m-%Y'), 'index #', idx)

        # Download and Save the Picture
        # Get a higher resolution by replacing the file name



        obj = pySmartDL.SmartDL(image_url, pic_path, progress_bar=False)
        obj.start()

        # Set Wallpaper if wanted by user
        if use_wallpaper:
            set_wallpaper(pic_path)


def main():
    print("|image=" + bing_icon)
    print("---")
    download_old_wallpapers()


if __name__ == "__main__":
    main()
