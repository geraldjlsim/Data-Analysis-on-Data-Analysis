# import requests
from time import sleep
# from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')


class JobstreetScraper:

    def __init__(self):

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(4)

    def search(self, text):
        results = pd.DataFrame()
        self.driver.get('https://www.jobstreet.com.sg/en/job-search/find-specialization?sal=1')
        sleep(1)
        input_what = self.driver.find_element_by_xpath('//*[@id="key"]')
        input_what.send_keys(text)
        self.driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()

        listings = int(self.driver.find_element_by_xpath(
          '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[1]/span').text.split()[2].replace(',', ''))
        pages = round(listings/30)

        for i in range(1, pages+1):
            self.driver.get('https://www.jobstreet.com.sg/en/job-search/'
              + text.replace(' ', '-') + '-jobs-in-singapore/{:d}/'.format(i))
            sleep(1)
            jobs_in_page = self.driver.find_elements_by_class_name('_1JtWu_1')
            for job in jobs_in_page:
                try:
                    job.click()
                except:
                    try:
                        skipsub = self.driver.find_element_by_xpath(
                            '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[3]/div/div[31]/div/div[3]/div/button')
                        skipsub.click()
                        job.click()
                    except:
                        try:
                            skipsub = self.driver.find_element_by_xpath(
                                '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[3]/div/div[24]/div/div[3]/div/button')
                            skipsub.click()
                            job.click()
                        except:
                            try:
                                skipsub = self.driver.find_element_by_xpath(
                                    '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[3]/div/div[25]/div/div[3]/div/button')
                                skipsub.click()
                                job.click()
                            except:
                                try:
                                    skipsub = self.driver.find_element_by_xpath(
                                        '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[3]/div/div[26]/div/div[3]/div/button')
                                    skipsub.click()
                                    job.click()
                                except:
                                    skipsub = self.driver.find_element_by_xpath(
                                        '//*[@id="contentContainer"]/div[2]/div/div/div[2]/div/div/div[3]/div/div[27]/div/div[3]/div/button')
                                    skipsub.click()
                                    job.click()

                try:
                    title = self.driver.find_element_by_xpath(
                      '//*[@id="contentContainer"]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div/div/div[1]/h1'
                      ).text
                except:
                    title = None

                try:
                    company = self.driver.find_element_by_xpath(
                      '//*[@id="contentContainer"]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div/div/div[2]/span'
                      ).text
                except:
                    company = None

                try:
                    salary = self.driver.find_element_by_xpath(
                      '//*[@id="contentContainer"]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[2]/span'
                      ).text
                except:
                    salary = None

                description = self.driver.find_element_by_class_name('vDEj0_1').text
                results = results.append(
                    {'Company': company, 'Title': title, 'Salary': salary, 'Description': description},
                    ignore_index=True)
        return results

bot = JobstreetScraper()

jobstreet1 = bot.search('data analyst')
jobstreet2 = bot.search('data scientist')
jobstreet3 = bot.search('machine learning')

jobstreet = pd.concat([jobstreet1, jobstreet2, jobstreet3], axis = 0).drop_duplicates()

jobstreet.to_csv('jobstreet.csv',index = False)

