import requests
import re
import urllib.parse
import wget
import os

email = ""
password = ""

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

    video_url = "https://www.facebook.com/elliotalderso/videos/vb.100007653464357/2024601894471573/?type=2&video_source=user_video_tab"
    video_id = re.search('videos/(.+?)/', video_url).group(1)

    video_page = session.get(video_url)
    identifier = re.search('ref=tahoe","(.+?)"', video_page.text).groups()[0]
    final_url = "https://www.facebook.com/video/tahoe/async/{0}/?chain=true&isvideo=true&originalmediaid={0}&playerorigin=permalink&playersuborigin=tahoe&ispermalink=true&numcopyrightmatchedvideoplayedconsecutively=0&storyidentifier={1}&dpr=2".format(
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
    final_url = 'https://www.facebook.com/video/tahoe/async/2024601894471573/?originalmediaid=2024601894471573&playerorigin=permalink&playersuborigin=tahoe&ispermalink=true&numcopyrightmatchedvideoplayedconsecutively=0&storyidentifier=UzpfSTEwMDAwNzY1MzQ2NDM1NzpWSzoyMDI0NjAxODk0NDcxNTcz&payloadtype=primary'
    api_call = session.post(final_url, data=data)

    try:
        final_video_url = re.search('hd_src":"(.+?)",', api_call.text).groups()[0]
    except AttributeError:
        final_video_url = re.search('sd_src":"(.+?)"', api_call.text).groups()[0]
    print(final_video_url)

    donwload_dir = os.path.join('.')
    final_video_url = final_video_url.replace('\\', '')

    print("Downloading ...")
    wget.download(final_video_url, dir)

else:
    print("Login failed.")