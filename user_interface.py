from tkinter import *
import os
#from spending_processor import Web_Search
from data_prep import Data_Prep
from spending_processor import Transaction

'''
class TransactionsFile:
    def __init__(self, loaded_transactions):
        self.loaded_transactions = loaded_transactions
    
    def load_transactions_from_file(self):
        with open("transaction_record", "r") as f:
            data = f.readlines()
            i = 0
            transaction_array = []
            for line in data: 
                if(i % 3 == 0):
                    transaction_array.append(line. rstrip('\n'))
                elif(i % 3 == 1):
                    transaction_array.append(line. rstrip('\n'))
                elif(i % 3 == 2):
                    transaction_array.append(line. rstrip('\n'))
                    transaction = Transaction(transaction_array[1], transaction_array[0], transaction_array[2])
                    self.loaded_transactions.append(transaction)
                i += 1 

        print("The following are loaded transactions")
        for transaction in self.loaded_transactions:
            print(transaction.transaction_name)

        return self.loaded_transactions
         
    def write_transactions_to_file(self, loaded_transactions): 
        with open("transaction_record", "w") as f:
            for transaction in loaded_transactions:
                f.write(transaction.transaction_name + "\n")
                f.write(transaction.date + "\n")
                f.write(transaction.amount + "\n")'''    

class PaneOne:
    def __init__(self, window, start_y_value, loaded_transactions):
        self.write_once = True
        self.create_components(window, start_y_value, loaded_transactions)

    def search_already_loaded(self, target_transaction, loaded_transactions):
        for transaction in loaded_transactions:
            if(transaction.transaction_name == target_transaction.transaction_name and transaction.date == target_transaction.date):
                return True
        return False

    def load_csv_file_contents(self, loaded_transactions):
        self.dp = Data_Prep()
        (transfers, subscriptions, web_required) = self.dp.categorize_transactions(self.dp.remove_filler_phrases(self.dp.read_spreadsheet(self.drop_one_clicked.get())))
        
        self.search_start_index = int(self.lowTxtFld.get())
        self.search_end_index = int(self.highTxtFld.get())

        #tf = TransactionsFile(loaded_transactions)
        #loaded_transactions = tf.load_transactions_from_file()

        for i in range(self.search_start_index, self.search_end_index):
            if(self.search_already_loaded(web_required[i], loaded_transactions) == False):
                loaded_transactions.append(web_required[i])

        #if self.write_once == True:
            #tf.write_transactions_to_file(loaded_transactions)
            #self.write_once = False       
            
    def create_load_transaction_components(self, window, start_y_value, transactions_to_search):
        y_spacer = start_y_value
        #space value 
        sv = 30

        #drop down menu to display the contents of unprocessed_transactions folder
        options = []
        for item in os.listdir(os.getcwd()):
            if(item.endswith('.csv')):
                options.append(item) 
        
        
        self.selectCSVLbl=Label(window, text="Select the csv file from which to load", fg='blue', font=("Helvetica", 20))
        self.selectCSVLbl.place(x=20, y=y_spacer)
        y_spacer += sv
        self.drop_one_clicked = StringVar()
        self.drop_one = OptionMenu( window , self.drop_one_clicked , *options )
        self.drop_one.place(x=20, y=y_spacer)
        y_spacer += sv
        self.selectTransactionRange=Label(window, text="Select the range of transactions for which load", fg='blue', font=("Helvetica", 20))
        self.selectTransactionRange.place(x=20, y=y_spacer)
        y_spacer += sv
        self.lowTxtFld=Entry(window, text="Low end of range", fg='black', bd=3, bg='white', width=5)
        self.lowTxtFld.place(x=20, y=y_spacer)
        self.highTxtFld=Entry(window, text="High end of range", fg='black', bd=3, bg='white', width=5)
        self.highTxtFld.place(x=120, y=y_spacer)
        y_spacer += sv
        self.btn1=Button(window, text="Upload Transactions", fg='blue', command=lambda: self.load_csv_file_contents(transactions_to_search))
        self.btn1.place(x=20, y=y_spacer)

    def create_components(self, window, start_y_value, transactions_to_search):
        self.create_load_transaction_components(window, start_y_value, transactions_to_search)

from spending_processor import Web_Search

class PaneTwo:
    def __init__(self, window, start_y_value, loaded_transactions):
        self.create_components(window, loaded_transactions, start_y_value)
    
    def generate_titles(self, loaded_transactions):
        ws = Web_Search()
            
        for transaction in loaded_transactions: 
            print(transaction.get_transaction_name())
            cur_titles = ws.get_webpage_titles(transaction.get_transaction_name())

            filename = 'unprocessed_title_files/' + transaction.get_transaction_name() + " " + transaction.date + ".txt"
            #overwrites any existing file with the same name 
            text_file = open(filename, "w")
            for title in cur_titles:
                text_file.write((title.get_text() + " "))

            text_file.close()

        ws.quit_webdriver()

    def create_components(self, window, loaded_transactions, start_y_value):
        y_spacer = start_y_value
        self.btn1=Button(window, text="Generate title pages from range", fg='blue', command=lambda: self.generate_titles(loaded_transactions))
        self.btn1.place(x=20, y=y_spacer)

class PaneThree:
    def __init__(self, window, start_y_value):
        self.create_components(window, start_y_value)

    def move_file(self):
        os.replace("unprocessed_title_files/" + self.drop_one_clicked.get(), 'processed_title_files/' + self.drop_one_clicked.get())

    def print_title_file_conents(self): 
        filename = os.getcwd() +  "/unprocessed_title_files/" + self.drop_one_clicked.get()
        with open(filename, "r") as f:
            data = f.readlines()
            for line in data: 
                print(line)
            f.close()

    def search_database_for_word(self, lines):
        for line in lines:
            if(self.wordTxtFld.get() in line):
                return True
        return False

    def append_word_to_file(self):
        with open(self.drop_clicked.get(), "r+") as f:
            lines = f.readlines()
            if(self.search_database_for_word(lines) == False):
                f.write(self.wordTxtFld.get())
            else:
                print(self.wordTxtFld.get() + "is already in the database")
            f.close()

    def place_read_title_file_interactive_components(self, nsyv):
        #font_size
        fs = 18
        #spacer_value
        sv = 30
        y_spacer = nsyv

        #label instructing the user
        self.pathLbl=Label(window, text="Choose the title file you'd like to read", fg='blue', font=("Helvetica", fs))
        self.pathLbl.place(x=20, y=y_spacer)
        y_spacer += sv

        #drop down menu to display the contents of unprocessed_transactions folder
        options = []
        for item in os.listdir("unprocessed_title_files"):
            options.append(item) 
        self.drop_two_clicked = StringVar()
        self.drop_two = OptionMenu( window , self.drop_two_clicked , *options )
        self.drop_two.place(x=20, y=y_spacer)
        y_spacer += sv
        self.btn1=Button(window, text="Open title file", fg='blue', command=self.print_title_file_conents)
        self.btn1.place(x=20, y=y_spacer)

        #return the ending y location value
        return y_spacer

    def place_database_dropdown(self, ssyv):
        #second_division_value
        sdv = 30

        self.nextStepLbl=Label(window, text="Select the file you'd like to append to", fg='blue', font=("Helvetica", 20))
        self.nextStepLbl.place(x=20, y=ssyv + sdv)
        options = [
            "shopping_words.txt",
            "leisure_words.txt",
            "restaurant_words.txt",
            "grocery_words.txt",
            "coffee_words.txt",
            "utility_words.txt"
        ]
        # datatype of menu text
        self.drop_clicked = StringVar()
        # initial menu text
        self.drop_clicked.set( "shopping_words.txt" )
        # Create Dropdown menu
        self.drop = OptionMenu( window , self.drop_clicked , *options )
        final_placement = ssyv + (2 * sdv)
        self.drop.place(x=20, y=final_placement)

        return final_placement

    def place_word_entry_components(self, tsyv):
        #third_division_value
        tdv = 30

        self.wordLbl=Label(window, text="Enter the word you'd like to append to the database file", fg='blue', font=("Helvetica", 20))
        tsyv = tsyv + tdv
        self.wordLbl.place(x=20, y=tsyv)
        self.wordTxtFld=Entry(window, text="Word to append", fg='black', bd=3, bg='white', width=20)
        tsyv = tsyv + tdv
        self.wordTxtFld.place(x=20, y=tsyv)
        self.appendWordBtn=Button(window, text="Append word to file", fg='blue', command=lambda: self.append_word_to_file())
        tsyv = tsyv + tdv
        self.appendWordBtn.place(x=20, y=tsyv)
        return tsyv

    def place_move_file_components(self, fsyv):
        #fourth_division_value
        fdv = 30

        self.moveLbl=Label(window, text="Once finished adding words, press the following button to move the file", fg='blue', font=("Helvetica", 20))
        fsyv = fsyv + fdv
        self.moveLbl.place(x=20, y=fsyv)
        self.moveFileBtn=Button(window, text="Move file to processed transactions", fg='blue', command=lambda: self.move_file())
        fsyv = fsyv + fdv
        self.moveFileBtn.place(x=20, y=fsyv)
        return fsyv

    def create_components(self, window, start_y_value):
        #component spacer 
        cs = 15

        #second start y value
        ssyv = self.place_read_title_file_interactive_components(start_y_value) + cs
        #third_start_y_value
        tsyv = self.place_database_dropdown(ssyv) + cs
        #fourth_start_y_value
        fsyv = self.place_word_entry_components(tsyv) + cs
        #fifth_start_y_value
        fsyv = self.place_move_file_components(fsyv) + cs

class PaneFour:
    def __init__(self, window):
        self.create_components(window)

    def create_components():
        return

class FrameOverall:
    def __init__(self, window):
        self.left_clicked = False
        self.right_clicked = False
        self.loaded_transactions = []
        self.current_page = 1
        self.update_current_page()

    def update_current_page(self):
        start_y_value = self.place_switch_page_buttons(window)
        if(self.current_page == 1):
            self.current_pane = PaneOne(window, start_y_value * 3, self.loaded_transactions)
        elif(self.current_page == 2):
            self.current_pane = PaneTwo(window, start_y_value * 3, self.loaded_transactions)
        elif(self.current_page == 3):
            self.current_pane = PaneThree(window, start_y_value * 3)
        elif(self.current_page == 4):
            self.current_pane = PaneFour(window, start_y_value * 3)

    def destroy_pane_contents(self, window):
        for widgets in window.winfo_children():
            widgets.destroy()
    
    def pan_left(self, window):
        self.left_clicked = True
        self.destroy_pane_contents(window)
        self.current_page -= 1
        self.update_current_page()

    def pan_right(self, window):
        self.right_clicked = True
        self.destroy_pane_contents(window)
        self.current_page += 1
        self.update_current_page()

    def place_switch_page_buttons(self, window):
        self.rightBtn=Button(window, text="-->", fg='black', command=lambda: self.pan_right(window))
        self.leftBtn=Button(window, text="<--", fg='black', command=lambda: self.pan_left(window))

        final_y_placement = 20
        self.rightBtn.place(x=80, y=final_y_placement)
        self.leftBtn.place(x=20, y=final_y_placement)
        return final_y_placement



window=Tk()
mywin=FrameOverall(window)
window.title('Hello Python')
window.geometry("800x600+400+200")
window.mainloop()
