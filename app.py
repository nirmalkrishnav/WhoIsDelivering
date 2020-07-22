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
        self.driver = webdriver.Chrome(options=op)

    def loadParam(self):
        f = open('param.json',) 
        self.param = json.load(f)

    def logMessage(self, message):
        print(message +'    '+  datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def saveOutput(self, provider ='', availability='', delivery_status=''):
        now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        
        with open(r'output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([now, provider, self.param['zip'], availability, delivery_status])

    def checkFlipkart(self):
        self.driver.get(self.param['flipkart_item'])
        self.logMessage('[bot]    opened Flipkart')
        
        zip_textbox = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[5]/div/div/div[1]/div[2]/div/div[2]/div[1]/form/input')
        zip_textbox.send_keys(self.param['zip'])
        press('enter')
        sleep(10)

        delivery_stat = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[5]/div/div/div[2]/div').text
        self.saveOutput(provider='Flipkart', delivery_status= delivery_stat)


    def checkAmazon(self):
        self.driver.get(self.param['amazon_item'])
        sleep(5)
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
      
        self.saveOutput(provider='Amazon', availability = availability, delivery_status= delivery_status)
        self.logMessage('[bot]    output recorded')
        

    def quitBrowser(self):
        self.logMessage('[bot]    gg')
        self.driver.quit()

bot = WhoIsDelivering()
bot.loadParam()
bot.checkFlipkart()
bot.quitBrowser()
