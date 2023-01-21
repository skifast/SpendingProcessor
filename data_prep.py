import csv 

'''Transaction data structure which contains information about the date, name, and amount associated with the object'''
class Transaction:
    def __init__(self, date, transaction_name, amount):
        self.date = date 
        self.transaction_name = transaction_name
        self.amount = amount 

    def get_transaction_name(self):
        return self.transaction_name

'''Prepare entries to be entered directly into the record or to be used in an internet search to gather key words'''
class Data_Prep:
    #returns an array of transactions as they appear in the pre-downloaded spreadsheet
    def read_spreadsheet(self, spreadsheet_name):
        
        #dates = []
        #transaction_names = []
        #amounts = []

        #info = [dates, transaction_names, amounts]
        transactions_list = []

        with open(spreadsheet_name) as csv_file:
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
