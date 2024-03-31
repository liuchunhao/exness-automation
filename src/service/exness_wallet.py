

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException

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

FUTURES_ACCOUNT = os.getenv('FUTURES_ACCOUNT')
SPOT_ACCOUNT_TRC20 = os.getenv('SPOT_ACCOUNT_TRC20')
SPOT_ACCOUNT_ERC20 = os.getenv('SPOT_ACCOUNT_ERC20')

def transfer(amount, destination='futures', wallet='TRC20'):
    begin_time = time.localtime()
    invoice_id = 'N/A'
    status = 'N/A'
    text = ''

    if wallet == 'ERC20':
        spot_account = SPOT_ACCOUNT_ERC20
    elif wallet == 'TRC20':
        spot_account = SPOT_ACCOUNT_TRC20

    if destination == 'futures':
        destination_account = FUTURES_ACCOUNT
        source_account = spot_account
    elif destination == 'spot':
        destination_account = spot_account
        source_account = FUTURES_ACCOUNT

    logging.info(f'0. Begin transfer from {source_account} to {destination_account}, wallet: {wallet}, amount: {amount}')

    driver = webdriver.Firefox()
    try:
        driver.get('https://my.exness.com/accounts/sign-in?lng=en')
        driver.maximize_window()

        # 1. Login
        try: 
            logging.info(f'1. Login')
            time.sleep(5)
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.NAME, 'login'))).send_keys(LOGIN)
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.NAME, 'password'))).send_keys(LOGIN_PASSWORD)
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*/button[@data-testid="login-button"]'))).click()
        except TimeoutException as e:
            raise Exception(f'Login: Not found')

        # 2. drop down header wallets list
        try:
            logging.info(f'2. drop down header wallets list')
            xpath = '//*/button[@data-test="header-wallets-drop-down"]'
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except TimeoutException as e:
            raise Exception(f'Drop down header wallets list: Not found')

        # 3. click transfer button
        try:
            logging.info(f'3. Click transfer button')
            xpath = '//*/button[@data-test="wallet-transfer-button"]'
            xpath = '//*[@id="wallet-header-menu"]//*/button[@data-test="wallet-transfer-button"]'
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except TimeoutException as e:
            raise Exception(f'Click transfer button: Not found')
        
        # 4. switch iframe
        def swithc_iframe():
            try:
                logging.info(f'4. Switch iframe')
                wait = WebDriverWait(driver, 10)
                xpath = '//*/iframe[@data-test="kyc-app-iframe"]'
                iframe = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                driver.switch_to.frame(iframe)
            except TimeoutException as e:
                raise Exception(f'Switch iframe: Not found')

        swithc_iframe()

        # 5. click transfer between your accounts
        try:
            logging.info(f'5. Click transfer between your accounts')
            wait = WebDriverWait(driver, 10)
            xpath = '//*/div[@data-auto="pl-item-button-mt_to_wt_int"]'
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except TimeoutException as e:
            raise Exception(f'Click transfer between your accounts: Not found')

        # 6. drop down source account list
        try:
            logging.info(f'6. Drop down source account list')
            wait = WebDriverWait(driver, 10)
            xpath = '//*[@id="source_account"]'
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(1)
        except TimeoutException as e:
            raise Exception(f'Drop down your source account list: Not found')

        # 6.1 select source account
        try: 
            logging.info(f'6.1 Select source account: {source_account}')
            wait = WebDriverWait(driver, 10)
            xpath = f'//*/li[@data-value="{source_account}"]'
            xpath = f'//*/li[@data-auto="source_account-option-{source_account}"]'
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(1)       # must wait for the list to be updated
        except TimeoutException as e:
            raise Exception(f'Select source account {source_account}: Not found')

        # 7. drop down destination account list
        try:
            logging.info(f'7. Drop down destination account list')
            wait = WebDriverWait(driver, 10)
            xpath = '//*[@id="destination_account"]'
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(1)
        except Exception as e:
            raise Exception(f'Drop down destination account list: Not found')

        # 7.1 select destination account
        try:
            logging.info(f'7.1 Select destination account: {destination_account}')
            xpath = f'//*/li[@data-auto="destination_account-option-{destination_account}"]'
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(1)
        except Exception as e:
            raise  Exception(f'Select destination account {destination_account}: Not found')
        
        # 7.2 check if any helper text popping up below the destination account
        text = ''
        try:
            logging.info(f'7.2 Check if any helper text popping up below the destination account')
            wait = WebDriverWait(driver, 1)
            xpath = '//*/p[@id="destination_account-helper-text"]'
            p = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            text = p.get_attribute('innerHTML')
        except Exception as e:
            pass        # no helper text
        if text:
            raise Exception(f'{text}') 

        # 8. input amount
        try:    
            logging.info(f'8. Input amount: {amount}')
            xpath = '//*/input[@id="main_amount"]'
            amount = str(amount)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(amount)
        except Exception as e:
            raise Exception(f'Input amount: Not found')

        # 8.1 check if any helper text popping up below the amount input box
        text = ''
        try: 
            logging.info(f'8.1 Check if any helper text popping up below the amount input box')
            xpath = '//*[@id="main_amount-helper-text"]/div'
            wait = WebDriverWait(driver, 2)
            p = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            text = p.get_attribute('innerHTML') 
        except Exception as e:
            pass
        if text:
            raise Exception(f'{text}')


        # 9. click submit
        try:
            logging.info(f'9. click submit button')
            wait = WebDriverWait(driver, 10)
            xpath = '//*/button'
            submit = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            submit.click()
            time.sleep(1)
        except Exception as e:
            raise Exception(f'Click submit button: Not found')


        # 9.1 check if any helper text popping up below the amount input box
        text = ''
        try: 
            logging.info(f'9.1 Check if any helper text popping up below the amount input box')
            xpath = '//*[@id="main_amount-helper-text"]/div/div'
            wait = WebDriverWait(driver, 2)
            p = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            text = p.get_attribute('innerHTML') 
        except Exception as e:
            pass
        if text:
            raise Exception(f'{text}')


        # try: 
        #     logging.info(f'9.1 Check if any helper text popping up below the amount input box')
        #     xpath = '//*[@id="main_amount-helper-text"]/div/div'
        #     wait = WebDriverWait(driver, 2)
        #     p = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        #     text = p.get_attribute('innerHTML') 
        # except Exception as e:
        #     pass       # no helper text
        # if text:
        #     raise Exception(f'{text}')

        # 10. confirm transfer
        try:
            logging.info(f'10. Confirm transfer')
            wait = WebDriverWait(driver, 10)
            xpath = '//*/button[@data-auto="confirm-button"]'
            confirm = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            confirm.click()
        except Exception as e:
            raise Exception(f'Confirm transfer: Not found')

        # 11. confirm message
        try:
            logging.info(f'11. confirm message')
            wait = WebDriverWait(driver, 10)
            xpath = '//*/div[@data-auto="transfer"]//*/div[@data-auto="title"]'
            status = wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).get_attribute('innerHTML')
            logging.info(f'11. confirm message: {status}')
        except Exception as e:
            raise Exception(f'Confirm message: Not found')

        # 12. Check history for the transfer
        '''
        try:
            logging.info(f'12. Check history for the transfer')
            wait = WebDriverWait(driver, 10)
            xpath = '//*/button[@data-auto="action-history"]'
            history = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            history.click()
        except Exception as e:
            raise Exception(f'Check history for the transfer: Not found')
        '''

        # 13. Send notification to LINE
        logging.info(f'Success: Transfer {amount} {wallet}')

        res = {
            "code": 0,
            "msg": f"{status}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": {
                "from": source_account,
                "to": destination_account,
                "wallet": wallet,
                "amount": amount,
                "invoice_id": invoice_id
            }
        }

    except Exception as e:
        logging.error(f'Failed: {e}')    
        # send notification to LINE
        res = {
            "code": -1,
            "msg": f'Failed: {e}',
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": {
                "from": source_account,
                "to": destination_account,
                "wallet": wallet,
                "amount": amount,
                "invoice_id": invoice_id
            }
        }
    finally:
        driver.quit()

    end_time = time.localtime()
    duration = time.mktime(end_time) - time.mktime(begin_time)
    res ['data']['duration'] = duration

    logging.info(f'res: {json.dumps(res, indent=4)}')
    return res
    
if __name__ == '__main__':

    # [] transfer(source='futures', network='TRC20', amount=1)
    # [] transfer(source='spot', network='TRC20', amount=1)
    # [] transfer(destination='futures', wallet='TRC20', amount=1)
    transfer(destination='spot', wallet='ERC20', amount=1)
    # transfer(destination='futures', wallet='ERC20', amount=1)
    # transfer(network='ERC20', amount=1)
   