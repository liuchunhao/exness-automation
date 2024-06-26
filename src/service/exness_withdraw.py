

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
import logging
import dotenv
from datetime import datetime

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)5s|%(message)s')

dotenv.load_dotenv()
LOGIN = os.getenv('LOGIN')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')

BINANCE_ADDRESS_TRC20 = os.getenv('BINANCE_ADDRESS_TRC20')
BINANCE_ADDRESS_ERC20 = os.getenv('BINANCE_ADDRESS_ERC20')


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


ADDRESSES = {
    'TRC20': BINANCE_ADDRESS_TRC20,
    'ERC20': BINANCE_ADDRESS_ERC20 
}


def get_binance_withdrwal_address(network='TRC20'):
    try:
        if network.upper() not in [ addr for addr in ADDRESSES.keys() ]:
            raise Exception(f'Error: Invalid network: {network}')   

        address = ADDRESSES[network.upper()]

        res = {
            "code": 0,
            "msg": "success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": {
                "network": network,
                "address": ADDRESSES[network.upper()]
            }
        }
    except Exception as e:
        res = {
            "code": -1,
            "msg": f'Error: {e}',
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": {
                "network": network,
                "address": "N/A"
            }
        }
    return res


def withdraw(amount, network='TRC20', currency='USDT'):
    logging.info(f'0. Withdraw: {network} / {amount}')

    driver = webdriver.Firefox()
    try:

        if network.upper() not in [ addr for addr in ADDRESSES.keys() ]:
            raise Exception(f'Error: Invalid network: {network}')

        address = ADDRESSES[network.upper()]

        driver.get('https://my.exness.com/accounts/sign-in?lng=en')
        driver.maximize_window()


        # 1. Login
        time.sleep(5)
        logging.info(f'1. Login')
        driver.find_element(By.NAME, 'login').send_keys(LOGIN)
        time.sleep(1)
        driver.find_element(By.NAME, 'password').send_keys(LOGIN_PASSWORD)
        time.sleep(1)
        driver.find_element(By.ID,'mui-3').click()
        time.sleep(1)


        # 2. Switch to withdrawal
        logging.info(f'2. Click withdrawal link')
        xpath = '//*/a[@data-test="menu-item-withdrawal"]'
        wait = WebDriverWait(driver, 30)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        withdrawal_link = driver.find_element(By.XPATH, xpath)
        withdrawal_link.click()
        logging.info(f'click withdrawal link: {withdrawal_link.text}|Done')
        

        # 3.  Switch iframe
        logging.info(f'3. Switch iframe:')
        wait = WebDriverWait(driver, 10)
        iframe = '//*/iframe[@data-test="kyc-app-iframe"]'
        div = wait.until(EC.element_to_be_clickable((By.XPATH, iframe)))
        driver.switch_to.frame(driver.find_element(By.XPATH , iframe))
        logging.info(f'3. Switch iframe|Done')


        # 3.2  Choose Network / Select TRC20 
        logging.info(f'4. Select: {network}')
        wait = WebDriverWait(driver, 10)
        xpath = '//*/div[@data-auto="pl-item-button-usdttrc"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        div_network = driver.find_element(By.XPATH, xpath)
        div_network.click()
        time.sleep(1)


        # 4. Drop down list and switch currency selection
        logging.info(f'5. Drop down currency list')
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="deposit"]'
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        time.sleep(2)


        # 4.1. Choose currency TRC20
        logging.info(f'choose currency: {network}')
        wait = WebDriverWait(driver, 10)
        xpath = '//*/div[@title="Tether (USDT ERC20)"]'
        if network == 'ERC20':
            xpath = '//*/div[@title="Tether (USDT ERC20)"]'
        elif network == 'TRC20':
            xpath = '//*/div[@title="Tether (USDT TRC20)"]'
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        time.sleep(1)

        # DO NOT CHANGE TO DIFFERENT CURRENCY !!!

        # 5. Input withdrawal address
        logging.info(f'input withdrawal address: {address}')
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="destination_account"]'
        input_address = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        input_address.send_keys(address)
        time.sleep(1)


        # 6. Input withdrawal amount
        amount = str(amount)
        logging.info(f'input withdrawal amount: {amount}')
        wait = WebDriverWait(driver, 10)
        xpath = '//*[@id="main_amount"]'
        input_amount = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        input_amount.send_keys(amount)
        time.sleep(1)


        # 7 Click submit
        try:
            logging.info(f'click submit button')
            wait = WebDriverWait(driver, 10)
            xpath = '//*/button'

            submit = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            submit.click()
            time.sleep(1)
        except Exception as e:
            # 7.1 Check if amount is valid
            logging.info(f'7.1 Check if amount is valid')
            wait = WebDriverWait(driver, 10)
            xpath = '//*[@id="main_amount-helper-text"]/div/div/div'
            helper_text = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            msg = helper_text.get_attribute('innerHTML')
            msg = str(msg).replace('&nbsp;', ' ')
            raise Exception(f'{msg}')


        # 8. Confirm withdrawal
        try:
            logging.info(f'click confirm button : send OTP verification code')
            xpath = '//*/button'
            submit = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            submit.click()
            time.sleep(1)
        except Exception as e:
            # 7.1 Check if amount is valid
            logging.info(f'7.1 Check if amount is valid')
            wait = WebDriverWait(driver, 10)
            xpath = '//*[@id="main_amount-helper-text"]/div'
            helper_text = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            msg = helper_text.get_attribute('innerHTML')
            msg = str(msg).replace('&nbsp;', ' ')
            raise Exception(f'{msg}')

        # 8.1 Wait for OTP verification code
        begin_time = time.localtime()
        time.sleep(10 * 3)


        # 9. Get OTP verification code from server
        '''
        {
            "code": 0,
            "data": {
                "mobile": "0932307567",
                "timestamp": "Mar 6, 2024 15:28:56",
                "verfication_code": "66668"
            },
            "msg": "GET Exness verification code successfully",
            "timestamp": "2024-03-06 15:35:22"
        }
        '''
        verification_code = "654321"
        try: 

            # requests.get('https://api.exness.com/withdrawal/otp?mobile=0932307567')
            endpoint = "http://ec2-3-112-51-9.ap-northeast-1.compute.amazonaws.com:5000/api/v1/exness/sms/verificationCode"
            done = False
            while not done:
                response = requests.get(endpoint)
                response = json.loads(response.text)
                logging.info(f'OTP verification code response: \n{json.dumps(response, indent=4)}')

                # timestamp ( convert to time struct )
                recv_time = response['timestamp']
                logging.info(f'OTP verification code received time: {recv_time}')   
                recv_time = time.strptime(recv_time, '%Y-%m-%d %H:%M:%S')

                # check if begin_time is before recv_time
                if begin_time > recv_time:
                    logging.error(f'Error: OTP verification code is expired')
                    # send notification to LINE
                    time.sleep(10*1)
                    continue

                data = response['data']
                verification_code = data['verfication_code']
                done = True

            logging.info(f'OTP verification code: {verification_code}')
        except Exception as e:
            raise Exception(f'Failed to retrieve OTP verification code')
        
        # 9. Enter OTP verification code : 6 digits
        try:
            logging.info(f'Enter OTP verification code')
            xpath = '//*[@id="otp"]/div/div/div[3]/div[1]/input'
            input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            digit = verification_code[0]
            input.send_keys(digit)
            time.sleep(1)
            xpath = '//*[@id="otp"]/div/div/div[3]/div[2]/input'
            input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            digit = verification_code[1]
            input.send_keys(digit)
            time.sleep(1)
            xpath = '//*[@id="otp"]/div/div/div[3]/div[3]/input'
            input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            digit = verification_code[2]
            input.send_keys(digit)
            time.sleep(1)
            xpath = '//*[@id="otp"]/div/div/div[3]/div[4]/input'
            input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            digit = verification_code[3]
            input.send_keys(digit)
            time.sleep(1)
            xpath = '//*[@id="otp"]/div/div/div[3]/div[5]/input'
            input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            digit = verification_code[4]
            input.send_keys(digit)
            time.sleep(1)
            xpath = '//*[@id="otp"]/div/div/div[3]/div[6]/input'
            input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            digit = verification_code[5]
            input.send_keys(digit)
            time.sleep(1)
        except Exception as e:
            raise Exception(f'Failed entering OTP verification code')

        # 10. Click confrim button to withdraw
        try:
            logging.info(f'Click confirm button: start to withdraw')
            time.sleep(2)
            xpath = '//*[@id=":rh:"]'
            xpath = '//*/button[contains(@id, ":.*:")]'
            xpath = '//*/button[@type="submit"]'
            xpath = '/html/body/div/div/div/div/div/div[2]/div/div[1]/form/div/div[5]/button'
            confirm = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            confirm.click()
            time.sleep(1)
        except Exception as e:
            # check if OPT verification code is invalid
            xpath = '//*[@id="otp"]/div/div/div[4]'
            error = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            error = error.get_attribute('innerHTML')
            error = str(error).replace('&nbsp;', ' ')
            raise Exception(f'OPT verification code is invalid: {verification_code}')

        # 11. Check history
        # xpath = '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div[4]/div/div/button'
        # button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        # button.click()

        # 12. Send notification to LINE
        logging.info(f'Withdrawal successfully')

        res = {
            "code": 0,
            "msg": "success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": {
                "network": network,
                "address": address,
                "amount": amount
            }
        }
    except Exception as e:
        logging.error(f'Error: {e}')    
        # send notification to LINE
        res = {
            "code": -1,
            "msg": f'Failed: {e}',
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": {
                "network": network,
                "address": address,
                "amount": amount
            }
        }
    finally:
        driver.quit()
    logging.info(f'Withdraw: res: \n{json.dumps(res, indent=4)}')

    return res
    
if __name__ == '__main__':

    # [] 
    withdraw(network='TRC20', amount=100)
    # [] withdraw(network='ERC20', amount=100)
    