# import requests
from time import sleep
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')


class MonsterScraper:

    def __init__(self):

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(4)

    def search(self, text):

        results = pd.DataFrame()
        self.driver.get(('https://www.monster.com.sg/srp/results?start=0&sort=1&limit=100&query='
                         + text.replace(" ", "%2C")))
        # sleep(1)
        # input_what = self.driver.find_element_by_xpath(
        #     '//*[@id="fts_id"]')
        # input_what.send_keys(text)
        # sleep(3)
        # input_what.send_keys(Keys.ENTER)
        # self.driver.find_element_by_xpath(
        #     '//*[@id="advance_main_form"]/div/div[15]/input').click()
        # except:
        #     sleep(4)
        #     input_what.send_keys(text)
        #     self.driver.find_elements_by_xpath('//*[@id="workhist-ui-id-1"]')[0].click()
        #     self.driver.find_element_by_xpath(
        #         '/html/body/app-root/div/app-home/div/div[1]/div/div/div/search-box/div/div/form/div/div[2]/button').click()

        pages = round((float(self.driver.find_element_by_xpath(
           '//*[@id="srp-main-container"]/div[1]/div[1]/span').text.split(' ')[3]))/100)

        # for i in range(0, pages):
        i = 0
        self.driver.get(('https://www.monster.com.sg/srp/results?start={:d}&sort=1&limit=100&query='
                         + text.replace(" ", "%2C")).format(0))
        jobs_in_page = self.driver.find_elements_by_class_name('job-apply-card')
        jobs_last_page = 0
        while jobs_in_page:

            #sleep(2)
            #jobs_last_page = self.driver.find_elements_by_class_name('job-apply-card')
            cards = len(jobs_in_page)
            for j in range(0,cards):
                job = jobs_in_page[j]
                if 'sponsored' not in job.text:
                    job = job.text.split('\n')
                    title = job[0]
                    company = job[1]
                    if len(job) > 5:
                        experience = job[3]
                        salary = job[4]
                        description = job[5] + ' ' + job[6]
                    else:
                        experience = None
                        salary = job[3]
                        description = job[4] + ' ' + job[5]
                    results = results.append(
                        {'Company': company, 'Title': title, 'Salary': salary, 'Description': description,
                         'Experience': experience}, ignore_index=True)
                    # print(results['Title'].iloc[-1])
                    # print(results['Company'].iloc[-1])
                    # print(results['Description'].iloc[-1])
                    # print(results['Salary'].iloc[-1])
                    # print(results['Experience'].iloc[-1])

            # for job in jobs_in_page:
            #     # ActionChains(self.driver) \
            #     #     .key_down(Keys.CONTROL) \
            #     #     .click(job) \
            #     #     .key_up(Keys.CONTROL) \
            #     #     .perform()
            #     # ActionChains(self.driver) \
            #     #     .key_down(Keys.CONTROL) \
            #     #     .key_down(Keys.TAB) \
            #     #     .key_up(Keys.CONTROL) \
            #     #     .key_up(Keys.TAB) \
            #     #     .perform()
            #     # self.driver.find_elements_by_class_name('job-tittle')[j-1]\
            #     if 'sponsored' not in job.text:
            #         job.click()
            #         try:
            #             self.driver.switch_to.window(self.driver.window_handles[1])
            #             try:
            #                 title = self.driver.find_element_by_xpath(
            #                   '//*[@id="jobDetailHolder"]/div/div/div[1]/div[2]/div[1]/\
            #                   div[1]/div/div[1]/div/div/div[2]/h1'
            #                   ).text
            #             except:
            #                 title = None
            #
            #             try:
            #                 company = self.driver.find_element_by_xpath(
            #                   '//*[@id="jobDetailHolder"]/div/div/div[1]/div[2]/div[1]/\
            #                   div[1]/div/div[1]/div/div/div[2]/span/a'
            #                   ).text
            #             except:
            #                 company = None
            #
            #             try:
            #                 salary = self.driver.find_element_by_xpath(
            #                   '//*[@id="jobDetailHolder"]/div/div/div[1]/div[2]/div[1]/\
            #                   div[1]/div/div[1]/div/div/div[2]/div/div[3]/span'
            #                   ).text
            #             except:
            #                 salary = None
            #
            #             try:
            #                 experience = self.driver.find_element_by_xpath(
            #                   '//*[@id="jobDetailHolder"]/div/div/div[1]/div[2]/\
            #                   div[1]/div[1]/div/div[1]/div/div/div[2]/div/div[2]/span'
            #                   ).text
            #             except:
            #                 experience = None
            #             try:
            #
            #                 description = self.driver.find_element_by_xpath(
            #                      '//*[@id="jobDetailHolder"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/p').text
            #             except:
            #                 description = None
            #
            #             results = results.append(
            #                 {'Company': company, 'Title': title, 'Salary': salary, 'Description': description,
            #                     'Experience': experience}, ignore_index=True)
            #             self.driver.close()
            #             sleep(1)
            #             self.driver.switch_to.window(self.driver.window_handles[0])
            #         except:
            #             print('skip')
            #
            #         print(results['Title'].iloc[-1])
            #         print(results['Company'].iloc[-1])
            #         print(results['Description'].iloc[-1])
            #         print(results['Salary'].iloc[-1])
            #         print(results['Experience'].iloc[-1])
            self.driver.get(('https://www.monster.com.sg/srp/results?start={:d}&sort=1&limit=100&query='
                             + text.replace(" ", "%2C")).format((i+1) * 100))
            jobs_in_page = self.driver.find_elements_by_class_name('job-apply-card')
            i += 1
        return results


bot = MonsterScraper()

#Monster = bot.search('"Data Analyst","data scientist","machine learning","data engineer","data visualisation","Analyst"')
Monster1 = bot.search('data analyst')
Monster2 = bot.search('data scientist')
Monster3 = bot.search('machine learning')
Monster4 = bot.search('data visualisation')

Monster = pd.concat([Monster1, Monster2, Monster3, Monster4], axis=0).drop_duplicates()

Monster.to_csv('Monster.csv', index=False)
