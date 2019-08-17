from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import html2text
from urllib import (
    urlopen, urlretrieve)
import os
import sys

class IGImages:

    def __init__(self,username,password,hashtag, out_folder = "images/"):
        self.username = username
        self.password = password
        self.hashtag = hashtag
        out_folder = out_folder+hashtag
        self.out_folder = out_folder
        if not os.path.isdir(out_folder):
            os.mkdir(out_folder)
        self.bot = webdriver.Firefox()
    
    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(15)
        email = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(10)

    def search_images(self):
        bot = self.bot
        out_folder = self.out_folder
        hashtag = self.hashtag
        get_url = 'https://www.instagram.com/explore/tags/'+hashtag
        bot.get(get_url)

        print("Images Downloader")
        
        for i in range(1,3):

            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(10)
            instagram = bot.find_elements_by_xpath("//*[@class='v1Nh3 kIKUG  _bz0w']//a")
            links = [elem.get_attribute('href') for elem in instagram]

            for link in links:

                bot.get(link)

                try:
                    url = bot.find_element_by_xpath('//div[@class="KL4Bh"]//img').get_attribute('src')
                    """Download image at 'url' to images/hashtag/"""
                    image_url = url.split("/")[-1]
                    remove = "?_nc_ht=instagram.fntr6-1.fna.fbcdn.net"
                    pre_filename = image_url.split(remove, 1)[0]
                    filename = hashtag+"_"+pre_filename
                    out_path = out_folder+"/"+filename
                    urlretrieve(url, out_path)

                    """ Download text """
                    text = bot.find_element_by_xpath('//div[@class="C4VMK"]//span')
                    plain_text = html2text.html2text(text)
                    remove_text_filename = "."
                    text_filename = filename.split(remove_text_filename, 1)[0]
                    out_path_text = out_folder+"/"+text_filename+".txt"
                    text_file = open(out_path_text, "w")
                    text_file.write(format(plain_text))
                    text_file.close()


                    msg = "Downloaded image "+out_path
                    print(msg)
                except Exception as ex:
                    print("It's a video or something went wrong, it's not possible to download it yet")
                    time.sleep(10)
""" MAKING MAGIC HERE """
tag = raw_input('Write hashtag: ')
dig = IGImages('USERNAME', 'PASSWORD', tag)
dig.login()
dig.search_images()