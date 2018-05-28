# -*- coding: utf-8 -*-
import re
import sys
import config.baseConfig;
from selenium import webdriver #浏览器驱动
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq

class DataProcess:
    __browser = None
    __total = 0
    __type = None
    __wait = None
    __htmlTag = None


    def __init__(self, type):
        self.__browser = webdriver.PhantomJS(service_args=config.baseConfig.SERVICE_ARGS,executable_path=config.baseConfig.executable_path)
        self.__wait = WebDriverWait(self.__browser, 10)
        self.__browser.set_window_size(1400, 900)
        self.__type = type
        self.__htmlTag = config.baseConfig.detail[type]

    def __search(self, keyWord):
        try:
            # self.__browser.get(self.__htmlTag["url"])
            # print 'yyyyyyyyyyy'
            # print self.__htmlTag["url"]
            # #input = self.__wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.__htmlTag["input"])))
            # print self.__htmlTag["input"]
            # input = self.__wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.__htmlTag["input"])))
            # print self.__htmlTag["submit"]
            # submit = self.__wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.__htmlTag["submit"])))
            # print keyWord
            # input.send_keys(keyWord)
            # submit.click()
            # print self.__htmlTag["page"]
            # self.__total = self.__wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.__htmlTag["page"])))[0].text
            # print '333333333333  '
            # print self.__total
            # self.__get_products();

            self.__browser.get(self.__htmlTag["url"])
            input = self.__wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.__htmlTag["input"]))
            )  # 等待搜索栏加载完成后，获取该元素
            print ('aaaaaaaaaaaaaaaa')  ###J_TSearchForm > div.search-button > button
            submit = self.__wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, self.__htmlTag["submit"])))  # 等待搜索按钮加载完成后，获取该按钮
            print('aaaaaaaaaaaaaaaa')
            input.send_keys(keyWord)
            # input.send_keys(KEYWORD)
            print ('aaaaaaaaaaaaaaaa')
            submit.click()  # 点击按钮
            ##等待总页数加载完成后，获取该元素
            self.__total = self.__wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.__htmlTag["page"])))[
                0].text
            self.__get_products()

        except TimeoutException,e:
            print e.message
            self.__search(keyWord)

    def __next_page(self, pageNumber):
        try:
            print pageNumber
            submit = self.__wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.__htmlTag["next"])))
            submit.click()
            self.__wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.__htmlTag["pageCur"]), str(pageNumber)))
            self.__get_products()

        except TimeoutException, e:
            print e
            self.__next_page(pageNumber)


    def __parse_amazon(self, items):
        for item in items:
            product = {
                'image': item.find('.a-section .s-access-image').attr('src'),
                'price': item.find('.a-price-whole').text(),
                 'deal': '',
                'title': item.find('.a-spacing-mini .a-spacing-none .a-text-normal').attr('title'),
                'shop':'',
                'location':'',
                'platform':'amazon',
                'url': item.find('.a-link-normal').attr('href')
            }
            print product
            self.__queue.put(product)

    def __parse_taobao(self, items):
        for item in items:
            product = {
                'image': "https:" + (item.find('.pic .img').attr('src') if (item.find('.pic .img').attr('src')) != None else ''),
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text()[:-3],
                'title': item.find('.title').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text(),
                'url': "https:"+(item.find('.J_ClickStat').attr('href') if (item.find('.J_ClickStat').attr('href') != None) else ''),
                'platform':'taobao'
            }
            print product


    def __get_products(self):
        self.__wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.__htmlTag["result"])))
        html = self.__browser.page_source
        doc = pq(html)
        items = doc(self.__htmlTag["result"]).items()
        if self.__htmlTag["url"] == "https://www.amazon.cn":
            self.__parse_amazon(items)

        elif self.__htmlTag["url"] == "https://www.taobao.com":
            self.__parse_taobao(items)

    def run(self):
        print "11111111111111111"
        for keyWords in config.baseConfig.key_word_list:
            self.__search(keyWords)
            total = int(re.compile('(\d+)').search(self.__total).group(1))
            for i in range(2,total + 1):
                print '======'
                self.__next_page(i)
        self.__browser.close()


if __name__ == '__main__':

    data = DataProcess(0)
    data.run()
    # with mysqlhandler.mysql() as cursor:
    #     cursor.execute("select * from product")
    #     row = cursor.fetchone()
    #     row1 = cursor.fetchone()
    #     print row
    #     print row1