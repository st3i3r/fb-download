import requests
import re
import urllib.parse
import wget
import os
import sys

email = ""
password = ""

ERASE_LINE = '\x1b[2K'

session = requests.session()
session.headers.update({
  'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
})

if not email and not password:
    email = input("Email: ")
    password = input("Password: ")

response = session.get('https://m.facebook.com')
response = session.post('https://m.facebook.com/login.php', data={
  'email': email,
  'pass': password
}, allow_redirects=False)

if 'c_user' in response.cookies:
    # login was successful
    homepage_resp = session.get('https://m.facebook.com/home.php')
    fb_dtsg = re.search('name="fb_dtsg" value="(.+?)"', homepage_resp.text).group(1)
    user_id = response.cookies['c_user']
    print("Login successfully")

    video_url = input("Video URL: ")
    video_id = re.search('videos/(.+?)/', video_url).group(1)

    video_page = session.get(video_url)
    identifier = re.search('ref=tahoe","(.+?)"', video_page.text).groups()[0]
    final_url = "https://www.facebook.com/video/tahoe/async/{0}/?originalmediaid={0}&playerorigin=permalink&playersuborigin=tahoe&ispermalink=true&numcopyrightmatchedvideoplayedconsecutively=0&storyidentifier={1}&payloadtype=primary".format(
        video_id, identifier)

    data = {'__user': user_id,
            '__a': '',
            '__dyn': '',
            '__req': '',
            '__be': '',
            '__pc': '',
            '__rev': '',
            'fb_dtsg': fb_dtsg,
            'jazoest': '',
            '__spin_r': '',
            '__spin_b': '',
            '__spin_t': '',
            }

    api_call = session.post(final_url, data=data)

    try:
        final_video_url = re.search('hd_src":"(.+?)",', api_call.text).groups()[0]
        print("Get HD URL")
    except AttributeError:
        final_video_url = re.search('sd_src":"(.+?)"', api_call.text).groups()[0]

    donwload_dir = os.path.join('/home/viet/Videos')
    final_video_url = final_video_url.replace('\\', '')
    print(final_video_url)

    print("Downloading ...")
    wget.download(final_video_url, donwload_dir)
    sys.stdout.write(ERASE_LINE)

else:
    print("Login failed.")