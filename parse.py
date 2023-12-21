import time
import re
import math

from openpyxl import load_workbook
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup


class Parse:
    def __init__(self, url):
        self.price_dict = {}
        self.url = url
        self.brands_pl = ['Apple', 'Huawei', 'Realme', 'Samsung', 'Xiaomi', 'Honor']
        self.brands_kof = ['DeLonghi', 'Philips', 'Smeg', 'Polaris', 'Nivona', 'Jura', 'Bosh']

    def _set_up(self):  # запускаем браузер
        options = Options()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)

    def _get_url(self):
        # print(self.url)
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def parse(self):
        self._set_up()
        self._get_url()
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        pr = soup.find_all('div', {'class': 'item-block'})
        # print(pr)
        for i in pr:
            product = i.find('div', {'class': 'item-title'}).a
            url = f"https://megamarket.ru{product['href']}"
            name = product['title']
            p = i.find('div', {'class': 'item-money'})
            price = int(re.sub(r"[\s,₽]", "", p.find('span').get_text()))
            try:
                bonus = int(re.sub(r"[\s,₽]", "", p.find('span', {'class': 'bonus-amount'}).get_text()))
            except AttributeError:
                bonus = 0
            sale = math.ceil((bonus * 100) / price)
            # if sale >= 44 and any(brand in name for brand in self.brands):
            # print(sale)
            if sale >= 32 and (any(brand in name for brand in self.brands_pl) or any(brand in name for brand in self.brands_kof)):
                self.price_dict[f'{name}'] = [url, sale]

        return self.price_dict


class Parse_Price:
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.products = {}
        self.counter = 0
        global wb
        wb = load_workbook(f'./price.xlsx')

    def _set_up(self):  # запускаем браузер
        options = Options()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)

    def _get_url(self, url):
        self.driver.get(f'{url}#?details_block=prices')
        self.driver.implicitly_wait(10)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def open(self):
        sheet = wb[f'{self.sheet_name}']
        row = self.counter
        self.products = {}
        for i in range(30):
            row += 1
            if sheet.cell(row=row, column=1).value is None:
                break
            self.products[sheet.cell(row=row, column=1).value] = sheet.cell(row=row, column=2).value
        print(self.products)

    def save(self):
        column = self.counter
        self.create_table()
        sheet = wb[f'{self.sheet_name}_1']
        for name, url_name in self.products.items():
            column += 1
            sheet[f'A{column}'], sheet[f'B{column}'] = name, url_name
        wb.save('price.xlsx')

    def create_table(self):
        print('create')
        if f'{self.sheet_name}_1' not in wb.sheetnames:
            wb.create_sheet(f'{self.sheet_name}_1')
            wb.save('./price.xlsx')
        # elif self.counter == 0:
        #     print(wb.sheetnames)
        #     wb.remove(f'{self.sheet_name}_1')
        #     print(wb.sheetnames)
        #     wb.create_sheet(f'{self.sheet_name}_1')
        #     wb.save('./price.xlsx')

    def calculation(self):
        self.open()
        for name, url in self.products.copy().items():
            self._set_up()
            self._get_url(url)
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            text = soup.find_all('div', {'class': 'product-offer product-offer_with-payment-method'})
            price_list = []
            discount_price_list = []
            for i in text:
                s = BeautifulSoup(str(i), 'lxml')
                price = int(re.sub(r"[\s,₽]", "", s.find('span',
                                                         {'class': 'product-offer-price__amount'}).get_text(
                    strip=True)))
                bonus = s.find('span', {'class': 'bonus-amount'})
                bonus = int(bonus.get_text(strip=True).replace(' ', '')) if bonus else 0
                price_list.append(price)
                discount_price_list.append(price - (bonus * 0.7))
            try:
                if min(price_list) < min(discount_price_list)+(min(discount_price_list)*0.35):
                    del self.products[name]
            except ValueError:
                pass
        self.save()

    def run(self):
        for i in range(0, 210, 30):
            self.counter = i
            self.calculation()


if __name__ =='__main__':
    # url = 'https://megamarket.ru/catalog/planshety/#?filters=%7B%222B0B1FF4756D49CF84B094522D57ED3D%22%3A%5B%22Apple%22%2C%22Honor%22%2C%22Huawei%22%2C%22Lenovo%22%2C%22Realme%22%2C%22Redmi%22%2C%22Samsung%22%2C%22Xiaomi%22%5D%7D'
    # url = 'https://megamarket.ru/catalog/planshety/'
    # Parse(url).parse()
    # Parse_Price('planshety').run()
    Parse_Price('kofemashiny').run()