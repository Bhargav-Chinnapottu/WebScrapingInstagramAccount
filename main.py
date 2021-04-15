import shutil

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os
import requests


class App:
    def __init__(self, user_name, password, target_username, path='/Users/USER/Desktop/WebScraping/instaphotos'):
        self.user_name = user_name
        self.password = password
        self.target_username = target_username
        self.path = path
        self.driver = webdriver.Chrome()
        self.main_url = 'https://www.instagram.com'
        self.error = False
        self.driver.get(self.main_url)
        sleep(5)
        self.accept_cookies()
        self.log_in()
        self.close_dialog_box()
        self.notifications_dialog()
        self.open_target_profile()
        self.posts()
        self.downloading_posts()
        self.driver.close()

    def accept_cookies(self):
        sleep(5)
        try:
            accept = self.driver.find_element_by_xpath("//button[@class='aOOlW  bIiDR  ']")
            accept.click()
        except Exception:
            pass

    def close_dialog_box(self):
        sleep(5)
        try:
            close_dialog = self.driver.find_element_by_xpath("//button[@class='sqdOP yWX7d    y3zKF     ']")
            close_dialog.click()
        except Exception:
            pass

    def notifications_dialog(self):
        sleep(5)
        try:
            close_notification = self.driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']")
            close_notification.click()
        except Exception:
            pass

    def log_in(self):
        try:
            user_name_input = self.driver.find_element_by_xpath("//input[@aria-label='Phone number, username, "
                                                                "or email']")
            user_name_input.send_keys(self.user_name)
            password_input = self.driver.find_element_by_xpath("//input[@aria-label='Password']")
            password_input.send_keys(self.password)
            password_input.submit()
            sleep(5)
        except Exception:
            print('Some exception occurred while trying to find username or password field')
            self.error = True

    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
            search_bar.send_keys(self.target_username)
            target_profile = self.main_url + '/' + self.target_username+'/'
            self.driver.get(target_profile)
            sleep(5)
        except Exception:
            self.error = True
            print('Could not find search bar')

    def posts(self):
        try:
            no_of_posts = self.driver.find_element_by_xpath("//span[@class='g47SY ']")
            no_of_posts = str(no_of_posts.text).replace(',', '')
            print(no_of_posts)
            no_of_posts = int(no_of_posts)
            if no_of_posts > 12:
                no_of_scrolls = int(no_of_posts/12)+3

                for value in range(no_of_scrolls):
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    sleep(1)
            sleep(5)
        except Exception:
            print('Could not find no of posts while trying to scroll down')
            self.error = True

    def downloading_posts(self):
        sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        all_images = soup.find_all('img', class_="FFVAD")
        self.downloading_captions(all_images)
        print(len(all_images))
        for index, image in enumerate(all_images):
            file_name = 'image_'+str(index)+'.jpg'
            file_path = os.path.join(self.path, file_name)
            link = image['src']
            response = requests.get(link, stream=True)
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
        sleep(5)

    def downloading_captions(self, images):
        sleep(5)
        caption_folder_path = os.path.join(self.path, 'captions')
        if not os.path.exists(caption_folder_path):
            os.mkdir(caption_folder_path)
        for index, image in enumerate(images):
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists for the selected image'
            file_name = 'caption_'+str(index)+'.txt'
            file_path = os.path.join(caption_folder_path, file_name)
            link = image['src']
            with open(file_path, 'wb') as file:
                file.write(str("link:" + str(link)+'\n'+"caption:"+caption).encode())
        sleep(5)


if __name__ == '__main__':
    username = input('Enter your user name: ')
    password_user = input('Enter your password')
    target_user_name = input('Enter user name from which you want to download photos: ')
    app = App(username, password_user, target_user_name)
