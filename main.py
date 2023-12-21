from parse import Parse, Parse_Price
from openpyxl import load_workbook


class Main:
    def __init__(self, url):
        self.dict_page = {}
        self.url = url
        self.count = 0
        global wb
        wb = load_workbook('price.xlsx')

    def open(self):
        if self.url in wb.sheetnames:
            wb.remove(wb[self.url])
        wb.create_sheet(self.url)
        wb.save('./price.xlsx')

    def save(self):
        sheet = wb[f'{self.url}']
        counter = 0
        self.dict_page = dict(sorted(self.dict_page.items(), key=lambda item: -item[1][1]))
        for name, url_sale in self.dict_page.items():
            counter += 1
            sheet[f'A{counter}'], sheet[f'B{counter}'], sheet[f'C{counter}'] = name, url_sale[0], url_sale[1]
        wb.save('price.xlsx')

    def paginator_page(self):
        url = f'https://megamarket.ru/catalog/{self.url}/'
        dict_ = Parse(url).parse()
        self.dict_page |= dict_
        count = 0
        # while True:
        for i in range(2):
            count += 1
            try:
                dict_ = Parse(f'{url}page-{count}').parse()
                self.dict_page |= dict_
            except TypeError:
                break

    def start(self):
        self.paginator_page()
        self.open()
        self.save()
        # Parse_Price(self.url)


if __name__ =='__main__':
    # url = 'kofemashiny'
    # url = 'planshety'
    url = 'blendery'
    # Main(url).start()
    Parse_Price(url).run()
