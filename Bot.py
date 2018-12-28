import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.common.keys
import time
import random
import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pickle
class Instagram:
    os.environ['MOZ_HEADLESS'] = '1'
    def __init__(self,Username , Password):
        self.Username = Username
        self.Password=Password
        self.driver=webdriver.Firefox()
    def closeBrowser(self):
        self.driver.close()
    def login(self):
        driver=self.driver
        driver.get("https://www.instagram.com")
        time.sleep(5)
        login_button=driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(5)
        user_name=driver.find_element_by_xpath("//input[@name='username']")
        user_name.clear()
        password_elem=driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        user_name.send_keys(self.Username)
        password_elem.send_keys(self.Password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(5)
        return True
    def likepic(self,hashtags,scroll):
        self.scroll=scroll
        driver=self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtags + "/")
        time.sleep(5)
        for i in range(1,self.scroll):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(5)
        hrefs = driver.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        #pic_hrefs = [href for href in pic_hrefs if hashtags in hrefs]
        #TRY ARIAL LABEL FOR LIKES
        print(hashtags+'__photos: ' + str(len(pic_hrefs)))
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            try:
                a=driver.find_element_by_xpath("//span[@aria-label='Like']")
                a.click()
                time.sleep(5)
            except Exception as e:
                time.sleep(2)
    def Followers(self):
        driver=self.driver
        driver.get("https://www.instagram.com/instagram/")
        time.sleep(2)
        for i in range(1000):
            print("Executing Level:",i)
            time.sleep(2)
            try:
                Follow_elem=driver.find_element_by_css_selector('button._5f5mN.jIbKX._6VtSN.yZn4P')
                Follow_elem.click()
                time.sleep(2)
            except NoSuchElementException as e:
                pass
            try:
                Following_elem=driver.find_element_by_css_selector('button._5f5mN.-fzfL._6VtSN.yZn4P')
                Following_elem.click()
                time.sleep(2)
                Confirm_unfollow= driver.find_element_by_css_selector('button.aOOlW.-Cab_')
                Confirm_unfollow.click()
                time.sleep(2)
            except NoSuchElementException as ee:
                pass
    def comments(self):
        time.sleep(2)
        driver=self.driver
        try:
            #user_comment=[]
            comments_block = self.driver.find_element_by_xpath("//ul[@class='k59kT']")
            comments_in_block=comments_block.find_elements_by_class_name('gElp9')
            comment=[x.find_element_by_tag_name('span') for x in comments_in_block]
            #for i in range(0,1000000):
             #   try:
            user_comment=re.sub(r'#.\w*','',comment[0].text)
              #  except Exception as e:
               #     pass
        except NoSuchElementException:
            return ''
        return user_comment

    def post_comment(self,comment_test):
        # time.sleep(2)
        # text_area=self.driver.find_element_by_xpath("//textarea[@class='Ypffh']")
        # text_area.click()
        # text_area.send_keys('')
        # text_area.clear()
        # time.sleep(1)
        # reply=self.reply_comment()
        # reply=str(reply)
        try:
            comment_link=lambda: self.driver.find_element_by_link_text('Comment')
            comment_link().click()
        except NoSuchElementException:
            pass
        #reply=self.reply_comment()
        try:
            add_comment_elem = lambda: self.driver.find_element_by_css_selector("textarea.Ypffh")
            add_comment_elem().click()
            add_comment_elem().clear()
            #comment_test=list(comment_test)
            add_comment_elem().send_keys(comment_test)
            #self.driver.execute_script("arguments[0].value = arguments[1]",self.driver.find_element_by_css_selector("textarea.Ypffh"), "nice!")
            #for i in comment_test:
             #   add_comment_elem.send_keys(i)
             #   time.sleep((random.randint(1,7)/30))
            add_comment_elem().send_keys(Keys.ENTER)
        except StaleElementReferenceException and NoSuchElementException as ee:
            print(ee)
            return False

    def reply_comment(self):

        bot = ChatBot('ChatterBot')
        bot.set_trainer(ListTrainer)
        message = self.comments()
        # for i in message:
        # print('user:',i)
        a = bot.get_response(message).__str__()
        return a

user_name=input('enter your username:')
password=input('enter your password:')
bot=Instagram(user_name,password)
bot.login()
#bot.likepic('newyork',1)
#hashtags=[]
#[bot.likepic(i,2) for i in hashtags]
#time.sleep(3)
#bot.driver.get("https://www.instagram.com/p/BrgS6AbAZkf/")
#time.sleep(3)
#cmmnts=bot.comments()
#for i in cmmnts:
 #   print(i)
bot.Followers()
#cmt=bot.reply_comment()
#bot.post_comment(cmt)
#bot.closeBrowser()
