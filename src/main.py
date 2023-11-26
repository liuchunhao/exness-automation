

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import sys
import re
import json

def login_free_using_browser_user_data():

    # get the user data directory from chrome://version/
    # remember bypass 'Default' dir
    user_data_dir = r'/Users/chunhao/Library/Application Support/Google/Chrome/'

    user_option = webdriver.ChromeOptions()
    user_option.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(options=user_option)
    driver.get('https://my.exness.com/accounts/sign-in?lng=en')


def login_free_using_cookie():
    
    # get the user data directory from chrome://version/
    # remember bypass 'Default' dir
    user_data_dir = r'/Users/chunhao/Library/Application Support/Google/Chrome/'

    user_option = webdriver.ChromeOptions()
    user_option.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(options=user_option)
    driver.get('https://my.exness.com/accounts/sign-in?lng=en')

    # get cookie from browser
    cookies = driver.get_cookies()

    # save cookie to file
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)

    # load cookie from file
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)

    # add cookie to browser
    for cookie in cookies:
        driver.add_cookie(cookie)

    # refresh page
    driver.refresh()


def firefox():
    driver = webdriver.Firefox()
    try:
        driver.get('https://my.exness.com/accounts/sign-in?lng=en')
        driver.maximize_window()

        # Step 1: login
        driver.find_element(By.NAME, 'login').send_keys('liu.chun.hao.tw@gmail.com')
        time.sleep(3)
        driver.find_element(By.NAME, 'password').send_keys('mtG36Abw#Gsb$cr')
        driver.find_element(By.ID,'mui-3').click()

        # Step 2: switch to withdrawal
        wait = WebDriverWait(driver, 30)
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@data-locator='layout-root']/main/div/div[@data-test='menu-root']/div[@data-walkthrough='mainMenu']/a[@data-test='menu-item-withdrawal']")))
        xpath = "/html/body/div[@id='root']/div[@data-locator='layout-root']/main/div/div[@data-test='menu-root']/div[@data-walkthrough='mainMenu']/a[@data-test='menu-item-withdrawal']"
        withdrawal_link = driver.find_element(By.XPATH, xpath)
        withdrawal_link.click()
        print(f'click withdrawal link: {withdrawal_link.text}')
        
        # Step 3: Choose network ERC20

        # Step 3.1: switch to iframe
        wait = WebDriverWait(driver, 10)
        xpath = '/html/body/div[1]/div[3]/main/div/div[2]/div/div'
        div = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        print(f'wait for iframe to display: {xpath}')

        xpath = f'{xpath}/iframe'
        driver.switch_to.frame(driver.find_element(By.XPATH , xpath))
        print(f'switch to iframe: {xpath}')

        # Step 3.2: click ERC20 (Ethereum)
        wait = WebDriverWait(driver, 10)
        xpath = '/html/body/div/div/div/div/div/div[2]/div/div/div[2]/div[5]'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        network = driver.find_element(By.XPATH, xpath)
        network.click()


        # Step 4: drop down currency list
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="deposit"]'
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        print(f'drop down currency list')
        
        # Step 4.1: choose currency ERC20
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="edecbfd5-0652-4296-ac1b-7347a66155da"]'
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        print(f'choose currency: {currency.text}')

        # Step 4.2: drop down currency list
        '''
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="deposit"]'
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        print(f'drop down currency list')

        # Step 4.3: choose currency TRC20
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="d09edeee-bc6e-4b87-bef3-ac62e30d111f"]'
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        print(f'choose currency: {currency.text}')
        '''

        # Step 5: input withdrawal address
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        erc20_address = '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE'
        trc20_address = 'TQjgj6KZ2KZzqQKXeR4qWYcEn5qX7e1n6i'
        xpath = '//*[@id="destination_account"]'
        address = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        address.send_keys(erc20_address)
        print(f'input withdrawal address: {erc20_address}')

        # Step 6: input withdrawal amount
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="main_amount"]'
        amount = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        amount.send_keys('0.0001')
        print(f'input withdrawal amount: 0.0001')

        # Step 7: click submit
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id=":rg:"]'
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        submit.click()
        print(f'click submit button')

    finally:
        time.sleep(60)
        driver.quit()

    
if __name__ == '__main__':
    # login_free_using_browser_user_data()
    firefox()
    

