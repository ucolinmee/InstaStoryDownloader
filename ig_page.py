from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
import os
from datetime import date
from google_drive import DriveAPI
from google_sheets import SheetsAPI

INSTAGRAM_URL = "https://www.instagram.com/accounts/login/"
INSTAGRAM_DOWNLOADER_URL = "https://chrome.google.com/webstore/detail/downloader-for-instagram/dhchoilkelgbblajmpbhpofhheecgkhh?hl=en"
USERNAME = "ShrekFlask"
PASSWORD = "PanadolExtra123"
CURRENT_DATE = date.today().strftime("%b-%d-%Y")

drive_api = DriveAPI()
sheets = SheetsAPI()
response = sheets.read_sheet()
sheet_rows = response["values"]


class IGPage:
    def __init__(self):
        chrome_driver_path = r"C:\Users\Colin\PycharmProjects\chromedriver.exe"
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': r'C:\Users\Colin\Documents\Colin\Kobe\Influencer-Stories'}
        options.add_experimental_option("prefs", prefs)
        options.add_extension('Downloader-for-Instagram™_v2.1.6.crx')
        self.driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)

    # The extension used for downloading Instagram stories/posts
    def download_extension(self):
        self.driver.get(INSTAGRAM_DOWNLOADER_URL)


    def login(self):
        self.driver.get(INSTAGRAM_URL)
        sleep(2)
        user = self.driver.find_element_by_name("username")
        user.send_keys(USERNAME)
        sleep(1)
        password = self.driver.find_element_by_name("password")
        password.send_keys(PASSWORD)
        sleep(1)
        button = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        button.click()
        sleep(7)
        not_now = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
        not_now.click()
        sleep(2)
        no_notifs = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        no_notifs.click()
        sleep(1)


    def get_page(self, influencer_handle):
        search_bar = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search_bar.send_keys(influencer_handle)
        sleep(3)
        suggested_acc = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div')
        suggested_acc.click()
        sleep(3)


    def download_story(self, influencername, folder_id):
        global NEWFILE_MIMETYPE
        count = 1
        view_story = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/div/div')
        view_story.click()
        sleep(2)
        num_stories = self.driver.find_elements_by_class_name('_7zQEa')
        for _ in range(len(num_stories)):
            download_button = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/div[1]/div/section/div/div[4]')
            download_button.click()

            # renaming the downloaded file
            old_filename = self.getDownLoadedFileName(100)
            old_file_ext = old_filename.split(".")[-1]
            # file mimetype required by Google drive API
            if old_file_ext == "jpg":
                NEWFILE_MIMETYPE = "image/jpeg"
            elif old_file_ext == "mp4":
                NEWFILE_MIMETYPE = "video/mp4"
            NEWFILE_NAME = f"{influencername}=({CURRENT_DATE})({count})"
            NEWFILE_PATH = f"C:\\Users\\Colin\\Documents\\Colin\\Kobe\\Influencer-Stories\\{influencername}=({CURRENT_DATE})({count}).{old_file_ext}"
            os.rename(src=f"C:\\Users\\Colin\\Documents\\Colin\\Kobe\\Influencer-Stories\\{old_filename}",
                   dst=f"C:\\Users\\Colin\\Documents\\Colin\\Kobe\\Influencer-Stories\\{influencername}=({CURRENT_DATE})({count}).{old_file_ext}")

            # upload file to Google drive
            try:
                drive_api.uploadFile(filename=NEWFILE_NAME, filepath=NEWFILE_PATH, mimetype=NEWFILE_MIMETYPE, folder_id=folder_id)
            except PermissionError:
                print(f"{NEWFILE_PATH} was unable to be uploaded.")

            finally:
                # switch back to Instagram tab
                self.driver.switch_to.window(self.driver.window_handles[0])

                # click to next story
                story_page = self.driver.find_element_by_tag_name('body')
                story_page.send_keys(Keys.RIGHT)
                sleep(1)
                count += 1


    def close_story(self):
        close_story = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div[3]/button')
        close_story.click()

    # gets the downloaded file name from Chrome downloads
    def getDownLoadedFileName(self, waitTime):
        self.driver.execute_script("window.open()")
        # switch to new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # navigate to chrome downloads
        self.driver.get('chrome://downloads')
        # define the endTime
        endTime = time() + waitTime
        while True:
            try:
                # get downloaded percentage
                downloadPercentage = self.driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
                # check if downloadPercentage is 100 (otherwise the script will keep waiting)
                if downloadPercentage == 100:
                    # return the file name once the download is completed
                    return self.driver.execute_script(
                        "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
            except:
                pass

            sleep(3)
            if time() > endTime:
                break


