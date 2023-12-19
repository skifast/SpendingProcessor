from web_search import Web_Search

class Transaction_Dict():
    transaction_dict = {"Groceries": [],  "Restaurants": [], "Coffee": [], "Leisure": [], "Shopping": [], "Gas": []}
    start_transaction_index = 0
    file_name = "webpage_titles.txt"

    def web_search_transaction(self, transaction_name):
        ws = Web_Search()
        print("one")
        titles = ws.get_webpage_titles(transaction_name)
        print("two")
        return titles

    def write_titles_to_file(self, titles):
        f = open(file_name, "a")
        f.write(titles)
        f.close()

    def print_titles(self):
        print(transaction_name)
        for title in titles:
            print(title.string)
        print("\n")

    def update_transaction_dict(self, transaction, transaction_dict):
        if((transaction_name := self.strip_transaction_name(transaction.transaction_name)) == "Name"):
            return
        titles = self.web_search_transaction(transaction_name)
        self.write_titles_to_file(titles)
        #transaction_dict = self.keyword_sort_titles(titles, transaction, transaction_name, transaction_dict)
        
        return transaction_dict

    #def write_searches_to_file(self):
        #todo

    #def generate_transaction_dict(self):
        #for each blank line
            #update the transaction dict

    def get_transaction_dict(self, transactions):
        end_transaction_index = len(transactions)
        i = self.start_transaction_index
        transaction_dict = self.transaction_dict
        
        while i < end_transaction_index:
            transaction = transactions[i] 
            if((transaction_name := self.strip_transaction_name(transaction.transaction_name)) == "Name"):
                return
            titles = self.web_search_transaction(transaction_name)
            self.write_titles_to_file(titles)
            i += 1
            #transaction_dict = self.keyword_sort_titles(titles, transaction, transaction_name, transaction_dict)
            #transaction_dict = self.update_transaction_dict(transactions[i], transaction_dict)
            
        return transaction_dict

    #def loop(self):
     #   end_transaction_index = len(transactions)
      #  i = self.start_transaction_index
       # while i < end_transaction_index:


    def strip_transaction_name(self, name):
        transaction_name = ""
        for char in name:
            if char.isalpha():
                transaction_name += char
            else:
                transaction_name += ' '
        return transaction_name
