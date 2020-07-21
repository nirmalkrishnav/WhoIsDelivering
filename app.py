from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from keyboard import press
from datetime import datetime

class WhoIsDelivering():
    def __init__(self):
        op = Options()
        op.headless = True
        self.driver = webdriver.Chrome(options=op)

    def logMessage(self, message):
        print(message +'    '+  datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def checkAmazon(self):
        self.driver.get('https://www.amazon.in/dp/B0859LMY97/ref=cm_sw_r_tw_dp_x_HyYfFbYZFP80C')
        sleep(3)
        open_zip_popup = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[5]/div[1]/div[3]/div/div/div/form/div/div/div/div/div[2]/div/div[40]/span/a/div/div/div/span/div')
        open_zip_popup.click()
        sleep(5)

        self.logMessage('[bot]    opened Amazon.in')

        zip_textbox = self.driver.find_element_by_id('GLUXZipUpdateInput')
        zip_textbox.send_keys('600042')

        submit = self.driver.find_element_by_id('GLUXZipUpdate')
        submit.click()

        sleep(5)
        self.logMessage('[bot]    searching for availability at 600042')

        availability = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[5]/div[4]/div[20]/div[1]').text
        delivery_status = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[5]/div[4]/div[25]').text
        
        output_file = open("output.csv","a")

        now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        output_file.write(now +','+ delivery_status+','+ availability)
        print('[bot]    output recorded')
        
        self.driver.quit()
        print('[bot]    gg')


bot = WhoIsDelivering()
bot.checkAmazon()
# bot.autoLike()