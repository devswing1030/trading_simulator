import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from marketdata.snapshot import Snapshot


class Nasdaq:
    def __init__(self):
        self.download_dir = '/tmp/scraper/nasdaq'
        os.makedirs(self.download_dir, exist_ok=True)
        self.watchlist = {}

    def create_driver(self, headless=True):
        service = Service('/opt/homebrew/bin/chromedriver')  # 替换为你的chromedriver路径
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'  # 设置为 eager 让页面尽快加载
        # Some websites might detect headless browsers and block access. Try setting a custom user-agent to mimic a real browser
        custom_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={custom_user_agent}')
        """
        options.add_argument('--disable-infobars')  # 禁用 Chrome 信息栏
        options.add_argument('--disable-extensions')  # 禁用扩展
        options.add_argument('--disable-translate')  # 禁用自动翻译
        options.add_argument('--disable-automatic-password-saving')  # 禁用自动保存密码
        options.add_argument('--disable-update')  # 禁用自动更新
        options.add_argument("--disable-extensions")  # 禁用扩展
        options.add_argument("--disable-gpu")  # 禁用GPU加速
        options.add_argument("--no-sandbox")  # 禁用沙箱
        options.add_argument("--disable-software-rasterizer")  # 禁用软件栅格化
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        """
        if headless:
            options.add_argument("--headless=new")

        # Set Chrome preferences for download behavior
        prefs = {
            "download.default_directory": self.download_dir,  # Path to the download directory
            "download.prompt_for_download": False,  # Don't prompt before downloading
            "download.directory_upgrade": True,  # Allow directory to be changed
            "safebrowsing.enabled": True  # Enable safe browsing for automatic downloads
        }
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def get_one_symbol(self, symbol):
        try:
            if symbol not in self.watchlist:
                self.watchlist[symbol] = {"driver": self.create_driver(), "is_ok": False }

            driver = self.watchlist[symbol]['driver']
            if not self.watchlist[symbol]['is_ok']:
                while True:
                    try:
                        driver.get(f'https://www.nasdaq.com/market-activity/stocks/{symbol}')
                        time.sleep(5)
                        break
                    except Exception as e:
                        print("Open symbol page failed: ", symbol, e)
                        time.sleep(10)

            snapshot = Snapshot(symbol)

            wait = WebDriverWait(driver, 30)  # 设置最大等待时间为 10 秒

            element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "nsdq-quote-header")))
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
            element = shadow_root.find_element(By.CLASS_NAME, 'nsdq-quote-header__pricing-information-saleprice')
            snapshot.last_px = element.text
            element = shadow_root.find_element(By.CLASS_NAME, 'nsdq-quote-header__pricing-information__timestamp')
            snapshot.timestamp = element.text
            element = shadow_root.find_element(By.CLASS_NAME, 'market-status-info')
            snapshot.market_status = element.text
            element = shadow_root.find_element(By.CLASS_NAME, 'nsdq-quote-header__asset-information-name')
            pos = element.text.find('(')
            snapshot.name = element.text[:pos].strip()
            if snapshot.market_status not in ['Open', 'Closed']:
                element = shadow_root.find_element(By.CLASS_NAME, 'quote-info-val')
                snapshot.close_px = element.text
            if snapshot.market_status != 'Closed':
                element = shadow_root.find_element(By.CLASS_NAME, 'header-info-bid-info')
                lines = element.text.split(' ')
                snapshot.bid_px = lines[0]
                snapshot.bid_qty = lines[2]
                element = shadow_root.find_element(By.CLASS_NAME, 'header-info-ask-info')
                lines = element.text.split(' ')
                snapshot.ask = lines[0]
                snapshot.ask_qty = lines[2]
                element = shadow_root.find_element(By.CLASS_NAME, 'header-info-volume-info')
                snapshot.volume = element.text

            self.watchlist[symbol]['is_ok'] = True

            return snapshot
        except Exception as e:
            print("Get symbol failed: ", symbol, e)
            self.watchlist[symbol]['is_ok'] = False
            time.sleep(10)
            return None

    def get_symbol_list(self):
        # clear all nasdaq_screener_*.csv
        for file in os.listdir(self.download_dir):
            if file.startswith('nasdaq_screener_') and file.endswith('.csv'):
                os.remove(os.path.join(self.download_dir, file))

        driver = self.create_driver()
        wait = WebDriverWait(driver, 5)  # 设置最大等待时间为 10 秒
        while True:
            try:
                driver.get("https://www.nasdaq.com/market-activity/stocks/screener")

                with open('nasdaq_screener.html', 'w') as f:
                    f.write(driver.page_source)

                element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jupiter22-c-table__download-csv")))
                element.click()
                print('Downloading csv file')
                break
            except Exception as e:
                print("Open screener page failed: ", e)

        symbol_list_file = None
        while True:
            files = os.listdir(self.download_dir)
            for file in files:
                if file.startswith('nasdaq_screener_') and file.endswith('.csv'):
                    print("Downloaded file: ", file)
                    symbol_list_file = file
                    break
            if symbol_list_file:
                break
            time.sleep(1)

        driver.close()

        symbols = []
        with open(os.path.join(self.download_dir, symbol_list_file), 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                fields = line.split(',')
                last_sale = fields[2][1:].strip()
                last_sale = float(last_sale)
                market_cap = fields[5].strip()
                if market_cap == "":
                    market_cap = 0
                else:
                    market_cap = float(market_cap)
                symbols.append({'symbol': fields[0], 'name': fields[1], 'last_sale': last_sale, 'market_cap': market_cap})
        return symbols


