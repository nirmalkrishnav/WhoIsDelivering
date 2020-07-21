from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from keyboard import press
from datetime import datetime
import csv
import json 


class WhoIsDelivering():
    def __init__(self):
        op = Options()
        op.headless = True
        self.driver = webdriver.Chrome()

    def loadParam(self):
        f = open('param.json',) 
        self.param = json.load(f)

    def logMessage(self, message):
        print(message +'    '+  datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def checkAmazon(self):
        self.driver.get(self.param['amazon_item'])
        sleep(3)
        open_zip_popup = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[5]/div[1]/div[3]/div/div/div/form/div/div/div/div/div[2]/div/div[40]/span/a/div/div/div/span/div')
        open_zip_popup.click()
        sleep(5)

        self.logMessage('[bot]    opened Amazon.in')

        zip_textbox = self.driver.find_element_by_id('GLUXZipUpdateInput')
        zip_textbox.send_keys(self.param['zip'])

        submit = self.driver.find_element_by_id('GLUXZipUpdate')
        submit.click()

        # need try catch here
        sleep(20)
        self.logMessage('[bot]    searching for availability at'+self.param['zip'])

        availability = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[5]/div[4]/div[20]/div[1]').text
        delivery_status = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[5]/div[4]/div[25]').text
        now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        
        with open(r'output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([now, self.param['zip'], availability, delivery_status])

        self.logMessage('[bot]    output recorded')
        
        self.driver.quit()
        self.logMessage('[bot]    gg')


bot = WhoIsDelivering()
bot.loadParam()
bot.checkAmazon()