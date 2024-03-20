
# Exness Automation
- [Exness Automation](#exness-automation)
  - [Installation](#installation)
  - [List of Chrome URLs](#list-of-chrome-urls)
  - [Get User Data Directory of Chrome](#get-user-data-directory-of-chrome)

## Installation
- Install [Chrome](https://www.google.com/chrome/)
- Install [ChromeDriver](https://chromedriver.chromium.org/downloads)
- Install [Selenium](https://selenium-python.readthedocs.io/installation.html)
    ```bash
    pip install selenium
    ```
- Install [Pytest](https://docs.pytest.org/en/stable/getting-started.html) 
 

## List of Chrome URLs
- find version of Chrome and find related version of ChromeDriver
    > chrome://version  

- find all Chrome URLs
    > chrome://about/  
    > chrome://chrome-urls/  
    > chrome://flags/  
    > chrome://settings/  

## Get User Data Directory of Chrome
- /Users/chunhao/Library/Application Support/Google/Chrome/
  > chrome://version/


## Start Up
- copy `MQL5/onTrade.mq5` into `MetaEditor`
- run API server
  ```bash
  $ virtualenv .venv
  $ source .venv/bin/activate
  # or ( source .venv/Scripts/activate ) on Windows

  $ ./start.sh
  ```
- make sure you have API server address whitelisted in the settings of MT5 before you start running MQL


# [Python Integration](https://www.mql5.com/en/docs/python_metatrader5)
  - [Return Code of the Trade Server](https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes)
  - [Trade Request Action](https://www.mql5.com/en/docs/python_metatrader5/mt5ordercheck_py#trade_request_actions)
  - [Order Filling Type](https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_type_filling)

## .env
```
LOGIN=blah.blah@gmail.com
LOGIN_PASSWORD=xyz

ACCOUNT=41084529
PASSWORD=Aa@124786017
SERVER=Exness-MT5Trial3
```
