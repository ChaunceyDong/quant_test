import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


class TreasuryDataScraper:
    def __init__(self):
        self.driver = self._initialize_driver()
        self.url = 'https://treasurydirect.gov/auctions/upcoming/'
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="institTableBillsUpcoming"]//tr[1]/td[1]')))
        self.html = self.driver.page_source
        self.tree = etree.HTML(self.html)

    def _initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')  # Headless browser
        driver = webdriver.Chrome(options=options,
                                  executable_path='/Users/chuanlin/Documents/chromedriver-mac-arm64/chromedriver')
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        driver.maximize_window()
        return driver

    def get_df_bills_with_link(self):
        num = self.tree.xpath('//*[@id="institTableBillsUpcoming"]/tbody/tr')
        all_datas = []
        for i in range(len(num)):
            bills = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[1]//text()')
            pdf_link = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[1]/a/@href')
            CMB = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[2]//text()')
            CUSIP = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[3]//text()')
            Offering_Amount = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[4]//text()')
            Announcement_Date = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[5]//text()')
            Auction_Date = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[6]//text()')
            Issue_Date = self.tree.xpath(f'//*[@id="institTableBillsUpcoming"]/tbody/tr[{i + 1}]/td[7]//text()')

            if len(pdf_link) == 0:
                pdf_link.append('')
            else:
                pdf_link[0] = 'https://treasurydirect.gov' + pdf_link[0]

            self._process_data_fields(bills, pdf_link, CMB, CUSIP, Offering_Amount, Announcement_Date, Auction_Date,
                                      Issue_Date)
            all_data = bills + CMB + CUSIP + Offering_Amount + Announcement_Date + Auction_Date + Issue_Date + pdf_link
            all_datas.append(all_data)

        df_bills = pd.DataFrame(all_datas,
                                columns=['Bills', 'CMB', 'CUSIP', 'Offering Amount', 'Announcement Date',
                                         'Auction Date', 'Issue Date', 'pdf_link'])
        return df_bills

    def _process_data_fields(self, *fields):
        for field in fields:
            if len(field) == 0:
                field.append('')

    def _get_df_generic(self, table_id, column_names):
        all_rows = []
        row_count = len(self.tree.xpath(f'//*[@id="{table_id}"]/tbody/tr'))
        for row_index in range(row_count):
            row_data = []
            for col_index in range(len(column_names)):
                data = self.tree.xpath(f'//*[@id="{table_id}"]/tbody/tr[{row_index + 1}]/td[{col_index + 1}]//text()')
                row_data.append(''.join(data).strip() if data else '')
            all_rows.append(row_data)
        return pd.DataFrame(all_rows, columns=column_names)

    def get_df_bills(self):
        # return self._get_df_generic("institTableBillsUpcoming",
        #                             ['Bills', 'pdf_link', 'CMB', 'CUSIP', 'Offering Amount', 'Announcement Date',
        #                              'Auction Date', 'Issue Date'])
        return self.get_df_bills_with_link()

    def get_df_notes(self):
        return self._get_df_generic("institTableNotesUpcoming",
                                    ['Notes', 'Reopening', 'CUSIP', 'Offering Amount', 'Announcement Date',
                                     'Auction Date',
                                     'Issue Date'])

    def get_df_Bonds(self):
        return self._get_df_generic("institTableBondsUpcoming",
                                    ['Bonds', 'Reopening', 'CUSIP', 'Offering Amount', 'Announcement Date',
                                     'Auction Date',
                                     'Issue Date'])

    def get_df_TIPS(self):
        return self._get_df_generic("institTableTIPSUpcoming",
                                    ['TIPS', 'Reopening', 'CUSIP', 'Offering Amount', 'Announcement Date',
                                     'Auction Date',
                                     'Issue Date'])

    def get_df_FRNs(self):
        return self._get_df_generic("institTableFRNUpcoming",
                                    ['FRNs', 'Reopening', 'CUSIP', 'Offering Amount', 'Announcement Date',
                                     'Auction Date',
                                     'Issue Date'])

    def close_driver(self):
        self.driver.close()


# Usage example:
scraper = TreasuryDataScraper()
df_bills = scraper.get_df_bills()

scraper.close_driver()
