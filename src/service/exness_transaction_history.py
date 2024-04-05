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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)5s|%(message)s')

dotenv.load_dotenv()
LOGIN = os.getenv('LOGIN')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')

FUTURES_ACCOUNT = str(os.getenv('FUTURES_ACCOUNT') if os.getenv('FUTURES_ACCOUNT') else "")
SPOT_ACCOUNT_TRC20 = str(os.getenv('SPOT_ACCOUNT_TRC20') if os.getenv('SPOT_ACCOUNT_TRC20') else "")
SPOT_ACCOUNT_ERC20 = str(os.getenv('SPOT_ACCOUNT_ERC20') if os.getenv('SPOT_ACCOUNT_ERC20') else "")


# def get_withdrawal_status(account, invoice_id=None):
#     driver = webdriver.Firefox()
#     try:
#         driver.get('https://my.exness.com/accounts/sign-in?lng=en')
#         driver.maximize_window()

#         # 1. Login
#         time.sleep(5)
#         logging.info(f'1. Login')
#         driver.find_element(By.NAME, 'login').send_keys(LOGIN)
#         time.sleep(1)
#         driver.find_element(By.NAME, 'password').send_keys(LOGIN_PASSWORD)
#         time.sleep(1)
#         driver.find_element(By.ID,'mui-3').click()
#         time.sleep(1)

#         # 2. Switch to History
#         logging.info(f'2. Click History link')
#         xpath = '//*/a[@data-test="menu-item-history"]'
#         wait = WebDriverWait(driver, 30)
#         wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#         withdrawal_link = driver.find_element(By.XPATH, xpath)
#         withdrawal_link.click()
#         logging.info(f'2. Click History link: {withdrawal_link.text}|Done')
        
#         # 3.  Switch iframe
#         logging.info(f'3. Switch iframe:')
#         wait = WebDriverWait(driver, 10)
#         iframe = '//*/iframe[@data-test="kyc-app-iframe"]'
#         div = wait.until(EC.element_to_be_clickable((By.XPATH, iframe)))
#         driver.switch_to.frame(driver.find_element(By.XPATH , iframe))
#         logging.info(f'3. Switch iframe|Done')

#         # 3.2  Select Transaction Type
#         logging.info(f'4. Select Transaction Type')
#         wait = WebDriverWait(driver, 10)
#         xpath = '//*/div[@data-auto="filter-payment-types"]'
#         wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#         div_network = driver.find_element(By.XPATH, xpath)
#         div_network.click()
#         time.sleep(1)

#         # 4. Drop down list and switch Trasaction type
#         logging.info(f'5. Drop down list and switch Trasaction type: [withdrawal]')
#         wait = WebDriverWait(driver, 10)
#         xpath = '//*/div[@data-auto="filter-payment-types-option-withdrawal"]'
#         currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#         currency.click()
#         time.sleep(2)

#         # 6. Drop down list and switch account type
#         logging.info(f'6. Select account ')
#         wait = WebDriverWait(driver, 10)
#         xpath = '//*/div[@data-auto="filter-payment-account"]'
#         currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#         currency.click()
#         time.sleep(1)

#         # 7. Select account 
#         logging.info(f'7. Select account: {account}')
#         wait = WebDriverWait(driver, 10)
#         xpath = f'//*/div[@data-auto="filter-payment-account-option-{account}"]'
#         currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#         currency.click()
#         time.sleep(2)

#         # Do below steps until the status turn into "Done" or "Rejected"
#         status_value = "Processing"

#         amount_value = 0.0
#         invoice_id_value = None

#         while status_value not in ["Done", "Rejected"]:
#             # 8. Check the status of selected invoice id:
#             logging.info(f'8. Check the status of selected invoice id: [{invoice_id}]')

#             wait = WebDriverWait(driver, 10)
#             xpath = f'//*/div[@data-auto="row-{invoice_id}"]'
#             if invoice_id == None:
#                 xpath = f'//*/div[@data-auto="group-rows"]/div[1]'

#             ## Get invoice id on the selected row
#             xpath_invoice_id = f'{xpath}//*/div[@data-auto="operation_invoice_id"]'
#             el_invoice_id = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_invoice_id)))
#             invoice_id_value = el_invoice_id.get_attribute('innerHTML')
#             invoice_id_value = str(invoice_id_value).split("Invoice ID ")[1]
#             logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] -> invoice_id: {invoice_id_value}')


#             ## Get amount on the selected row
#             xpath_amount = f'{xpath}//*/div[@data-auto="ltr"]'
#             xpath_amount = f'{xpath}//*/div[@data-auto="amount"]/div[@data-auto="ltr"]'
#             amount = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_amount)))
#             amount_value = str(amount.get_attribute('innerHTML'))
#             amount_value = amount_value.replace('&nbsp;', '')
#             logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] -> amount: {amount_value}')

#             ## Click the selected row
#             transaction_row = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#             transaction_row.click()
#             logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] | Clicked')
#             time.sleep(1)

#             '''

#             # 9. Get subtitle (invoice id) of withdrawal status
#             logging.info(f'9. Get subtitle of withdrawal status:')
#             wait = WebDriverWait(driver, 10)
#             xpath = '//*/div[@data-auto="history-detail"]/div[@data-auto="details-operation"]//*/div[@data-auto="subtitle"]'
#             subtitle = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#             subtitle = driver.find_element(By.XPATH, xpath)
#             subtitle_value = subtitle.get_attribute('innerHTML')    # get value in the <div>value</div> 
#             logging.info(f'9. Get subtitle of withdrawal status: [{subtitle_value}]')
#             invoice_id_value = str(subtitle_value).split("Invoice ID ")[1]
#             logging.info(f'9. Get subtitle of withdrawal status: {invoice_id_value}')
#             time.sleep(1)

#             '''

#             # 9. Get status of withdrawal
#             logging.info(f'9. Get status of withdrawal: {invoice_id if invoice_id else invoice_id_value}')
#             wait = WebDriverWait(driver, 10)
#             xpath = '//*/div[@data-auto="history-detail"]/div[2]/div[1]/div[2]/div[2]'
#             status = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#             status = driver.find_element(By.XPATH, xpath)
#             status_value = status.get_attribute('innerHTML')    # get value in the <div>value</div> 
#             logging.info(f'9. Get status of withdrawal: {invoice_id if invoice_id else invoice_id_value} -> {status_value}')
#             time.sleep(1)

#             # 10. Close the history details
#             logging.info(f'10. Close the history details {invoice_id if invoice_id else invoice_id_value}')
#             wait = WebDriverWait(driver, 10)
#             xpath = '//*/div[@data-auto="modal-close-button"]'
#             close_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#             close_button.click()
#             logging.info(f'10. Close the history details {invoice_id if invoice_id else invoice_id_value }|Closed')
#             time.sleep(5)

#         res = {
#             "code": 0,
#             "msg": f'Withdrawal status: {status_value}',
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "data": {
#                 "account": account,
#                 "invoice_id": invoice_id if invoice_id else invoice_id_value,
#                 "amount": amount_value
#             }
#         }

#     except Exception as e:
#         logging.error(f'Error: {e}')    

#         # send notification to LINE
#         res = {
#             "code": -1,
#             "msg": f'Withdrawal: Error: {e}',
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "data": {
#                 "account": account,
#                 "invoice_id": invoice_id,
#                 "amount": "N/A"
#             }
#         }

#     finally:
#         driver.quit()

#     # 12. Send notification to LINE
#     logging.info(f'get_withdrawal_status of invoice id [{invoice_id}]]: \n {res}')

#     return res


def list_transaction_history(account="", status="", payment_type=""):
    logging.info(f'list_transaction_history: account={account}, status={status}, payment_type={payment_type}')
    begin = datetime.now()

    res = {}
    res["data"] = {}
    res["data"]['account'] = account
    res["data"]['status'] = status.upper()
    res["data"]['payment_type'] = payment_type.upper()
    res["data"]['transactions'] = []

    driver = webdriver.Firefox()

    try:
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

        # 2. Switch to History
        logging.info(f'2. Click History link')
        xpath = '//*/a[@data-test="menu-item-history"]'
        wait = WebDriverWait(driver, 30)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        withdrawal_link = driver.find_element(By.XPATH, xpath)
        withdrawal_link.click()
        logging.info(f'2. Click History link: {withdrawal_link.text}|Done')
        
        # 3. Switch iframe
        logging.info(f'3. Switch iframe:')
        wait = WebDriverWait(driver, 10)
        iframe = '//*/iframe[@data-test="kyc-app-iframe"]'
        div = wait.until(EC.element_to_be_clickable((By.XPATH, iframe)))
        driver.switch_to.frame(driver.find_element(By.XPATH , iframe))
        logging.info(f'3. Switch iframe|Done')

        # 4. Select Transaction Type
        logging.info(f'4. Select Transaction Type')
        wait = WebDriverWait(driver, 10)
        xpath = '//*/div[@data-auto="filter-payment-types"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        div_network = driver.find_element(By.XPATH, xpath)
        div_network.click()
        time.sleep(1)

        # 5. Drop down list and switch Trasaction type
        logging.info(f'5. Drop down list and switch Trasaction type: [withdrawal]')
        wait = WebDriverWait(driver, 10)
        xpath_switch = { 
            "":           '//*/div[@data-auto="filter-payment-types-option-"]',
            "withdrawal": '//*/div[@data-auto="filter-payment-types-option-withdrawal"]',
            "deposit":    '//*/div[@data-auto="filter-payment-types-option-deposit"]',
            "transfer":   '//*/div[@data-auto="filter-payment-types-option-transfer"]'
        }

        xpath = xpath_switch[payment_type]
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        time.sleep(2)

        # 5. Drop down list and switch status
        logging.info(f'Select status: ')
        wait = WebDriverWait(driver, 10)
        xpath = '//*/div[@data-auto="filter-payment-status"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        div_network = driver.find_element(By.XPATH, xpath)
        div_network.click()
        time.sleep(1)

        # 5. Drop down list and switch status
        logging.info(f'Select status: Processing')
        wait = WebDriverWait(driver, 10)
        switch = {
            "":           '//*/div[@data-auto="filter-payment-status-option-"]',
            "processing": '//*/div[@data-auto="filter-payment-status-option-processing"]',
            "done":       '//*/div[@data-auto="filter-payment-status-option-done"]',
            "rejected":   '//*/div[@data-auto="filter-payment-status-option-rejected"]'
        }

        xpath = switch[status.lower()]

        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        logging.info(f'Select status: Processing | Done')
        time.sleep(2)

        # 6. Drop down list and switch account type
        logging.info(f'6. Select account ')
        wait = WebDriverWait(driver, 10)
        xpath = '//*/div[@data-auto="filter-payment-account"]'
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        time.sleep(1)

        # 6. Select account 
        logging.info(f'6. Select account: {account}')
        wait = WebDriverWait(driver, 10)
        xpath = f'//*/div[@data-auto="filter-payment-account-option-{account}"]'
        switch = {
            "":         f'//*/div[@data-auto="filter-payment-account-option-"]',
            "FUTURES":  f'//*/div[@data-auto="filter-payment-account-option-{FUTURES_ACCOUNT}"]',
            "TRC20":    f'//*/div[@data-auto="filter-payment-account-option-{SPOT_ACCOUNT_TRC20}"]',
            "ERC20":    f'//*/div[@data-auto="filter-payment-account-option-{SPOT_ACCOUNT_ERC20}"]',
        }
        xpath = switch[str(account).upper()]
        currency = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        currency.click()
        time.sleep(2)

        # 7. List the rows of transactions
        logging.info(f'7. List the rows of transactions')
        wait = WebDriverWait(driver, 10)
        xpath = f'//*/div[@data-auto="group-rows"]/*'       # list child tag <div> of parent
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        rows = driver.find_elements(By.XPATH, xpath)
        logging.info(f'7. List the rows of transactions: {len(rows)}')
        invoice_id_list = []
        for row in rows:
            attr_invoice_id = row.get_attribute("data-auto")
            attr_invoice_id = str(attr_invoice_id).split("-")[1]
            invoice_id_list.append(attr_invoice_id)
            logging.info(f'7. List the rows of transactions: {attr_invoice_id}')

        # 8. Check the status of selected invoice id:
        for invoice_id in sorted(invoice_id_list, key=int, reverse=True):
            transaction = {}
            transaction["invoice_id"] = invoice_id

            # 8. Check the status of selected invoice id:
            logging.info(f'8. Check the status of selected invoice id: [{invoice_id}]')
            wait = WebDriverWait(driver, 10)
            xpath = f'//*/div[@data-auto="row-{invoice_id}"]'

            ## Get <type> on the selected row
            xpath_type = f'{xpath}//*/div[@data-auto="type"]'
            _type = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_type)))
            _type = _type.get_attribute('innerHTML')
            transaction["type"] = _type
            logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] -> type: {_type}')

            ## Get <date> on the selected row
            xpath_date = f'{xpath}//*/div[@data-auto="date"]'
            element_date = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_date)))
            attr_date = element_date.get_attribute('innerHTML')
            transaction["date"] = attr_date
            logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] -> date: {attr_date}')

            ## Get <invoice id> on the selected row
            xpath_invoice_id = f'{xpath}//*/div[@data-auto="operation_invoice_id"]'
            element_invoice_id = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_invoice_id)))
            invoice_id_value = element_invoice_id.get_attribute('innerHTML')
            invoice_id_value = str(invoice_id_value).split("Invoice ID ")[1]
            logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] -> invoice_id: {invoice_id_value}')

            ## Get <from> on the selected row
            logging.info(f'{SPOT_ACCOUNT_TRC20}')
            logging.info(f'{SPOT_ACCOUNT_ERC20}')
            switch = {
                FUTURES_ACCOUNT: f'FUTURES',
                SPOT_ACCOUNT_TRC20[-6:] : 'SPOT(TRC20)',
                SPOT_ACCOUNT_ERC20[-6:] : 'SPOT(ERC20)',
            }
            logging.info(f'8. Check the source of the selected transaction [{invoice_id}]: {switch}')

            try:
                xpath_from = f'{xpath}//*/div[@data-auto="from"]'
                _from = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_from)))
                _from = str(_from.get_attribute('innerHTML')).replace("\u2022", "") 
                _from = switch[_from] if _from in switch.keys() else _from
                transaction["from"] = _from
                logging.info(f'8. Check the source of the selected transaction [{invoice_id}]: {_from}')   
            except Exception as e:
                raise Exception(f'8. Check the source of the selected transaction [{invoice_id}]: None')

            try:
                ## Get <to> on the selected row
                xpath_to = f'{xpath}//*/div[@data-auto="to"]'
                _to = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_to)))
                _to = str(_to.get_attribute('innerHTML')).replace('\u2022', "") 
                _to = switch[_to] if _to in switch.keys() else _to
                transaction["to"] = _to
                logging.info(f'8. Check the destination of the selected transaction [{invoice_id}]: {_to}')   
            except Exception as e:
                raise Exception(f'8. Check the destination of the selected transaction [{invoice_id}]: None')

            ## Get <amount> on the selected row
            try: 
                xpath_amount = f'{xpath}//*/div[@data-auto="amount"]/div[@data-auto="ltr"]'
                amount = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_amount)))
                amount_value = str(amount.get_attribute('innerHTML'))
                amount_value = amount_value.replace('&nbsp;', '')
                transaction["amount"] = amount_value
                logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] -> amount: {amount_value}')
            except Exception as e:
                raise Exception(f'8. Check the status of selected invoice id: [{invoice_id}] -> amount: None')

            ## Get <status> on the selected row
            try:
                xpath_status = f'{xpath}//*/div[@data-auto="status"]/span'
                status = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_status)))
                status_value = str(status.get_attribute('innerHTML'))
                transaction["status"] = status_value
                logging.info(f'8. Get <status> on the selected row: [{invoice_id}] -> status: {status_value}')
            except Exception as e:
                raise Exception(f'8. Get <status> on the selected row: [{invoice_id}] -> status: None')

            ## Get "reason" of rejection
            xpath_reason = f'{xpath}//*/div[@data-auto="reason"]'
            try:
                reason = driver.find_element(By.XPATH, xpath_reason)
                reason_value = str(reason.get_attribute('innerHTML'))
                transaction["reason"] = reason_value
                logging.info(f'8. Check the status of selected invoice id: [{invoice_id}] -> reason: {reason_value}')
            except NoSuchElementException as e:
                logging.warning(f'8. Check the status of selected invoice id: [{invoice_id}] -> reason: None')
                transaction["reason"] = "N/A"
            

            res["data"]["transactions"].append(transaction)

        res["code"] = 0
        res["msg"] = 'success'
        res["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except TimeoutException as e:
        logging.warning(f'{e}')

        res["code"] = 0
        res["msg"] = f'No transaction history found'
        res["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res["data"]["transactions"] = []

    except Exception as e:
        logging.error(f'Error: {e.with_traceback}')
        # send notification to LINE
        res["code"] = -1
        res["msg"] = f'Processing Withdrawal: Error: {e}'
        res["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res["data"]["transactions"] = []

    finally:
        driver.quit()

    # 12. Send notification to LINE
    end = datetime.now()
    duration = end - begin
    res["data"]["duration"] = str(duration)

    logging.info(f'list_withdrawal_history: \n {json.dumps(res, indent=4)}')
    return res


def get_latest_transaction_history(account="", status="", payment_type=""):
    logging.info(f'get_latest_transaction_history: account={account}, status={status}, payment_type={payment_type}')    
    res = list_transaction_history(account=account, status=status, payment_type=payment_type)
    res['data'] = res['data']['transactions'][0] if len(res['data']['transactions']) > 0 else {}
    logging.info(f'get_latest_transaction_history: \n {json.dumps(res, indent=4)}')


if __name__ == '__main__':

    account = ""
    account = "TRC20"
    account = "ERC20"
    account = "FUTURES"

    invoice_id = 1243621254 # done
    invoice_id = 1243605797 # done
    invoice_id = 1243551976 # rejected

    # [X] list_transaction_history(account=account, status="Rejected", payment_type="transfer")
    # [X] list_transaction_history(account=account, status="Rejected", payment_type="withdrawal")
    # [X] list_transaction_history(account=account, status="Rejected", payment_type="deposit")

    # [X] list_transaction_history(account=account, payment_type="deposit")
    # [X] list_transaction_history(account=account, payment_type="transfer")
    # [X] list_transaction_history(payment_type="withdrawal")
    # [X] list_transaction_history()
    

    # [X] get_latest_transaction_history(account=account, status="Rejected", payment_type="transfer")
    # [X] get_latest_transaction_history(payment_type="withdrawal")
