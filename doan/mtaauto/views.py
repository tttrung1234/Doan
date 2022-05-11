
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

    def Close_webdriver(self):
        self.driver.close()

    def start_chorme(self):

        chrome_options = Options()

        chrome_options.add_argument("--window-size=540,700")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-images")
        self.driver = webdriver.Chrome(options=chrome_options)

    def start_chorme_profile(self, l):
        if self.driver == None:
            global data
            UID = str(data[0][l])
            self.chrome_options = Options()

            scriptDirectory = pathlib.Path().absolute()
            self.chrome_options.add_argument(
                f"user-data-dir={scriptDirectory}\\Profile\\"+UID)

            if(l <= 2):
                x = l*520
                y = 10
            if(l > 2 and l <= 6):
                x = (l-3)*520
                y = 330
            self.chrome_options.add_argument("--disable-notifications")
            self.chrome_options.add_argument("--disable-images")
            self.chrome_options.add_argument("--window-size=200,300")
            self.chrome_options.add_argument(f"--window-position={x},{y}")
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
    def Like_post(self, id):
        link_post = "https://m.facebook.com/"+id
        self.driver.get(link_post)
        try:
            self.driver.find_element_by_xpath('//a[text()="Thích"]').click()
        except:
            print("không thể Like")


def ThucThiLogin_loadCookie(l):
    bot = Cookie()

    bot.start_chorme_profile(l)
    try:
        bot.load_cookie(str(data[0][l]))
        print(data[1][0])
        bot.Like_post(
            str(data[1][0]))
    except:
        print(f"cửa sổ {l+1} load không thành công")
    bot.Close_webdriver()


data = None


def AutoLike(id):
    global data
    arr = []
    with open("UID.txt", "r") as f:
        for line in f:
            arr = [elt.strip() for elt in line.split(',')]

    data = np.array((arr, arr), dtype=np.uint64)

    lenUID = np.shape(data)[1]
    data[1][0] = id

    threads = []

    for l in range(7):

        threads += [threading.Thread(target=ThucThiLogin_loadCookie,
                                     args={l},)]

    for t in threads:

        t.start()

    for t in threads:
        t.join()

    # threads += [threading.Thread(target=ThucThiLogin_loadCookie,
    #                              args={str(data[1]), url},)]

    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()


def ThucThiLogin_getCookie():
    bot = Cookie()
    bot.start_chorme()
    bot.load_page()
    bot.get_cookie()

# get html


def Gethtml(idpost):
    import requests
    urlpost = 'https://m.facebook.com/'+idpost
    html = None
    r = requests.get(urlpost)
    html = r.text
    post = {
        'html': html,
        'url': urlpost,
        'id': idpost,
    }
    return post

# end get html
 # get post facebook#################3


def Getpost_tuyentruyen(request):
    # import requests
    # html = None
    post_data = []
    # url = 'https://m.facebook.com/groups/YAN.VietNamOi/permalink/5430846466948584/?m_entstream_source=feed_mobile'
    # r = requests.get(url)
    # html = r.text

    post_data.append(Gethtml("150561547426531"))
    post_data.append(Gethtml("381544837343636"))
    post_data.append(Gethtml("3629620013929952"))

    content = {'post_data': post_data}

    # xử lí like, share, cmt, bao cao, khong anh huong
    if 'idLike' in request.GET:
        id = request.GET.get('idLike')

        AutoLike(id)

    if 'idCmt' in request.GET:
        id = request.GET.get('idCmt')
        print("cmt thoi")

    if 'idShare' in request.GET:
        id = request.GET.get('idShare')
        print("share thoi" + id)

    if 'idBaocao' in request.GET:
        id = request.GET.get('idBaocao')
        print("bao cao thoi")

    if 'idKAH' in request.GET:
        id = request.GET.get('idKAH')
        print("khong anh huong")

    # end xử lí like, share, cmt, bao cao, khong anh huong

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
