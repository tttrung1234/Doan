
from django import http
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from requests import Response

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pickle
import os
import numpy as np
import threading

import pathlib

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def index(request):
    return render(request, "start.html")


def chitiet(request):
    content = None
    if "city" in request.GET:
        content = request.GET["city"]
    return render(request, "chitiet.html", {'content': content})


class Cookie:
    def __init__(self):
        self.driver = None
        self.cookie = None
        self.UID = None

    def wait_load(self):
        while True:
            lenh = 'return document.readyState == "complete"'
            dk = self.driver.execute_script(lenh)

            if dk == True:
                break

    def start_chorme(self):

        chrome_options = Options()

        chrome_options.add_argument("--window-size=540,700")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-images")
        self.driver = webdriver.Chrome(options=chrome_options)

    def start_chorme_profile(self, UID):
        if self.driver == None:
            self.chrome_options = Options()

            scriptDirectory = pathlib.Path().absolute()
            self.chrome_options.add_argument(
                f"user-data-dir={scriptDirectory}\\Profile\\"+UID)

            self.chrome_options.add_argument("--window-size=540,700")
            self.chrome_options.add_argument("--disable-notifications")
            self.chrome_options.add_argument("--disable-images")
            self.driver = webdriver.Chrome(options=self.chrome_options)

            return 1
        else:
            return -1

    def load_page(self):
        self.driver.get("https://facebook.com/")
        self.driver.find_element_by_id('email').click()
        self.driver.find_element_by_id('email').send_keys(
            'trannamssb123@outlook.com')
        time.sleep(2)
        self.driver.find_element_by_id('pass').click()
        lenh = 'document.querySelector("#pass").value="TrinhTrung2020"'
        self.driver.execute_script(lenh)
        time.sleep(3)
        try:
            self.driver.find_element(By.XPATH, "//*[@name='login']").click()
        except:
            print("Không tìm thấy nút Login")

    def get_cookie(self):

        while True:
            lenh = 'return document.readyState == "complete"'
            dk = self.driver.execute_script(lenh)

            if dk == True:
                break

        time.sleep(8)
        cookies = self.driver.get_cookies()
        print(cookies)
        self.UID = cookies[5]['value']
        # read file

        with open("UID.txt", "r") as f:
            for line in f:
                inner_list = [elt.strip() for elt in line.split(',')]

        if (self.UID not in inner_list):
            # write UID
            with open("UID.txt", "a") as file:
                file.write(self.UID + ",")
                file.close()
        path = "./Profile\\" + self.UID
        print(self.UID)
        p = os.path.exists(path)
        if(not p):
            os.makedirs(path)
            print("Tạo profie" + self.UID + "....")
            time.sleep(1)
            pickle.dump(cookies, open(path + "\\cookie.pkl", "wb"))
        self.driver.close()

    def load_cookie(self, UID):
        self.driver.get("https://m.facebook.com/")

        cookies = pickle.load(open("Profile\\" + UID + "\\cookie.pkl", "rb"))

        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    # like
    def Like_post(self, link_post):
        self.driver.get(link_post)
        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[4]/div/div[1]/div[1]/div/div/footer/div/div/div[1]/a").click()


def ThucThiLogin_loadCookie(UID):
    bot = Cookie()
    bot.start_chorme_profile(UID)
    bot.load_cookie(UID)
    bot.Like_post(
        "https://m.facebook.com/story.php?story_fbid=2893865214198532&id=100007252455965&m_entstream_source=timeline")

    input(".....................")


def ThucThiLogin_getCookie():
    bot = Cookie()
    bot.start_chorme()
    bot.load_page()
    bot.get_cookie()
 # get post facebook#################3


def Getpost_tuyentruyen(request):
    import requests
    html = None
    post_data = []
    url = 'https://m.facebook.com/groups/YAN.VietNamOi/permalink/5430846466948584/?m_entstream_source=feed_mobile'
    r = requests.get(url)
    html = r.text

    post = {
        'html': html,
        'url': 'url111111111111',
        'id': 11111111,
    }
    post_data.append(post)
    post = {
        'html': html,
        'url': 'url2222222222222',
        'id': 22222222,
    }
    post_data.append(post)

    content = {'post_data': post_data}
    if 'city' in request.GET:
        city = request.GET.get('city')
        print(city)

    return render(request, "autofb.html", content)


def Getpost_phandong(request):
    import requests
    test1 = None
    url = 'https://m.facebook.com/groups/YAN.VietNamOi/permalink/5430846466948584/?m_entstream_source=feed_mobile'
    r = requests.get(url)
    test1 = r.text

    return render(request, "autofb.html", {'content': test1})


# end get post facebook ##############3


def TrinhsatFB(request):
    import requests
    test1 = None
    url = 'https://m.facebook.com/groups/YAN.VietNamOi/permalink/5430846466948584/?m_entstream_source=feed_mobile'
    r = requests.get(url)
    test1 = r.text

    return render(request, "trinhsatfb.html", {'content': test1})
