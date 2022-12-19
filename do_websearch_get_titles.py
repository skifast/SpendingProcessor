'''Valerie Hetherington, December 19 2022'''

'''The goal of this project is to organize recorded transactions into categories. It will ultimately produce a 
document for the user to analyze their credit or debit expenditures. Right now, the program writes files with 
the website titles corresponding to each transaction. These can eventually be used in a database for machine learning 
to categorize a given transaction into categories.  '''

import requests
import csv 
from numbers_parser import Document
from web_search_data import Web_Search_Data
from transaction_dict import Transaction_Dict
from web_search import Web_Search
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import bs4 
from selenium.webdriver.common.keys import Keys

'''Transaction data structure which contains information about the date, name, and amount associated with the object'''
class Transaction:
    def __init__(self, date, transaction_name, amount):
        self.date = date 
        self.transaction_name = transaction_name
        self.amount = amount 

    def get_transaction_name(self):
        return self.transaction_name

'''A home for printing methods'''
class Display_Data:
    def display_data(self, data):
        for i in range(len(data[0])):
            print(data[0][i])
            print(data[1][i])
            print(data[2][i])
            print("\n")
    
    def display_transactions(self, data):
        for i in range(len(data[0])):
            print(data[1][i])

    def display_categories(self, categories):
        transfers = []
        subscriptions = []
        web_required = []

        for i in range(len(categories)):
            if(i == 0):
                print("Transfers:")
            elif(i == 1):
                print("Subscriptions:")
            else:
                print("Web Required:")

            for item in categories[i]:
                print(item)
            print("\n")

'''Prepare entries to be entered directly into the record or to be used in an internet search to gather key words'''
class Data_Prep:
    #returns an array of transactions as they appear in the pre-downloaded spreadsheet
    def read_spreadsheet(self):
        
        #dates = []
        #transaction_names = []
        #amounts = []

        #info = [dates, transaction_names, amounts]
        transactions_list = []

        with open('transactions.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                #dates.append(row[0])
                #transaction_names.append(row[2])
                #amounts.append(row[4])
                cur_transaction = Transaction(row[0], row[2], row[4])
                transactions_list.append(cur_transaction)
                #print(cur_transaction.date, cur_transaction.transaction_name, cur_transaction.amount)
                
        return transactions_list

    #edits the name so that it only contains words describing the transfer
    def remove_filler_phrases(self, transactions_list):
        filler_phrases = ["DEBIT PURCHASE -VISA", "DEBIT PURCHASE",
        "SQ", "-VISA"]

        for i in range(len(transactions_list)):
            transaction = transactions_list[i]
            date = transaction.date
            #transaction_name = transaction.transaction_name
            amount = transaction.amount

            for fp in filler_phrases:
                if fp in transactions_list[i].transaction_name:
                    #print(transaction_name.replace(fp, ''))
                    transactions_list[i].transaction_name = (transactions_list[i].transaction_name.replace(fp, ''))
                    #print(transactions_list[i].transaction_name)
                    #print("\n")

        return transactions_list

    #sort the transactioins that are known to be transfers, account fees, subscriptions, and venmo transactions
    def categorize_transactions(self, transactions_list):
        transfer_phrases = ["BANKING TRANSFER DEPOSIT", "OVERDRAFT PAID FEE",
        "OVERDRAFT PAID FEE", "Venmo", "VENMO" ]
        subscription_phrases = ["RECURRING"]

        transfers = []
        subscriptions = []
        web_required = []

        categories = []
        categories.append(transfers)
        categories.append(subscriptions)
        categories.append(web_required)

        for t in transactions_list:
            for tp in transfer_phrases:
                if tp in t.transaction_name:
                    transfers.append(t)
                    break
            for sp in subscription_phrases:
                if sp in t.transaction_name:
                    subscriptions.append(t)
                    break 
            if not t in transfers and not t in subscriptions:
                web_required.append(t)

        return categories

'''Using a transaction description, perform a search and collect website titles'''
class Web_Search():
    def __init__(self):
        self.client = requests.session()
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")    
        self.driver = uc.Chrome(use_subprocess=True,options=options)

    def click_button(self, xpath_string, transaction_name):
        result = True
        try:
            time.sleep(1)
            elem = self.driver.find_element(By.XPATH, xpath_string)
        except NoSuchElementException:
            result = False
        if (result == True):
            elem.click()
        return result

    #on Google.com, send the transaction label to the search bar and press search
    def google_page_navigation(self, transaction_name):
        try:
            self.driver.find_element("xpath", "//input[@name='q']").send_keys(transaction_name)
            self.driver.find_element("xpath", "//input[@name='q']").send_keys(Keys.RETURN)
        except TimeoutException or NoSuchElementException or ElementNotInteractableException:  
            self.driver.quit()
            print("google_page_navigation error")

    #not totally fleshed out...still figuring out when this even comes up
    def check_for_capatcha(self):
        xpath_string = "//form[@id='captcha-form']"
        try:
            elem = self.driver.find_element(By.XPATH, xpath_string)
            print("capatcha found!")
            return True
        except NoSuchElementException:
            return False

    #scroll down, loading more pages until there are no more or the 'show more' button appears. 
    #COULD EXTEND THINGS HERE by clicking that button, but when to stop?
    def title_extraction_loop(self, transaction_name):
        webpage_titles = [] 

        last_height = 0
        new_height = 1
        while(new_height != last_height):
            last_height = new_height
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            time.sleep(1)

        innerHTML = self.driver.execute_script("return document.body.innerHTML")
        root=bs4.BeautifulSoup(innerHTML,"lxml")
        webpage_titles += root.find_all("h3")

        return webpage_titles

    #get list of webpage titles for a given transaction
    def get_webpage_titles(self, transaction_name):
        self.driver.get("https://www.google.com/")
        time.sleep(1)
        self.google_page_navigation(transaction_name)
        webpage_titles = self.title_extraction_loop(transaction_name)
        return webpage_titles

class Main():
    def __init__(self):
        dp = Data_Prep()
        (transfers, subscriptions, web_required) = dp.categorize_transactions(dp.remove_filler_phrases(dp.read_spreadsheet()))
        
        for i in range(1, len(web_required)):
            item = web_required[i]
            ws = Web_Search()
            cur_titles = ws.get_webpage_titles(item.get_transaction_name())
            filename = item.get_transaction_name() + ".txt"
            text_file = open(filename, "w")
            for title in cur_titles:
                text_file.write(title.get_text())
            text_file.close()


main = Main()
