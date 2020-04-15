# import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')


class IndeedScraper:

    def __init__(self):

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(4)

    def search(self, text):
        results = pd.DataFrame()
        self.driver.get('https://sg.indeed.com/')
        sleep(1)
        input_what = self.driver.find_element_by_xpath('//*[@id="text-input-what"]')
        input_what.send_keys(text)
        self.driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button').click()

        pages = int(self.driver.find_element_by_xpath('//*[@id="searchCountPages"]').text.split()[3].replace(',', ''))
        if pages > 1000:
            iterations = 1001
        else:
            iterations = pages
        for i in range(0, iterations, 10):
            self.driver.get('https://sg.indeed.com/jobs?q=' + text.replace(' ', '+') + '&start={:d}'.format(i))
            sleep(1)
            jobs_in_page = self.driver.find_elements_by_class_name('result')
            for job in jobs_in_page:
                job_html = job.get_attribute('innerHTML')
                job_soup = BeautifulSoup(job_html, 'html.parser')
                #print(job.id)

                try:
                    title = job_soup.find("a", class_="jobtitle").text.replace('\n', '')
                except:
                    title = np.nan

                try:
                    company = job_soup.find(class_="company").text.replace('\n', '')
                except:
                    company = np.nan

                try:
                    salary = job_soup.find(class_="salary").text.replace('\n', '')
                except:
                    salary = np.nan

                try:
                    job.find_elements_by_class_name('summary')[0].click()
                except:
                    self.driver.find_element_by_xpath('//*[@id="popover-x"]').click()
                    job.find_elements_by_class_name('summary')[0].click()
                description = self.driver.find_element_by_id('vjs-desc').text
                results = results.append(
                    {'Company': company, 'Title': title, 'Salary': salary, 'Description': description},
                    ignore_index=True)
        return results

bot = IndeedScraper()

indeed1 = bot.search('data analyst')
indeed2 = bot.search('data scientist')
indeed3 = bot.search('machine learning')

indeed = pd.concat([indeed1, indeed2, indeed3], axis = 0).drop_duplicates()

indeed.to_csv('indeed.csv',index = False)