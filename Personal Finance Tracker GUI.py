import tkinter as tk
from tkinter import ttk
import json

class FinanceTrackerGUI:
    def __init__(self, root):
        # Defind A Dictionary To Store Transactions
        self.transactions ={}
        self.root = root
        # size of a main window in gui
        self.root.geometry('500x300')
        root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions("transactions.json")

    def create_widgets(self):
        # Frame for table and scrollbar
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying transactions
        self.my_tree = ttk.Treeview(self.frame)

        # Definding column names
        self.my_tree['columns'] = ("Category","Amount","Type","Date")
        
        # Format of column names 
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("Category",anchor=tk.W, width=0)
        self.my_tree.column("Amount",anchor=tk.W, width=20)
        self.my_tree.column("Type",anchor=tk.W, width=20)
        self.my_tree.column("Date",anchor=tk.W, width=20)

        # Create headings
        self.my_tree.heading("Category",text="Category",anchor=tk.W)
        self.my_tree.heading("Amount",text="Amount",anchor=tk.W)
        self.my_tree.heading("Type",text="Type",anchor=tk.W)
        self.my_tree.heading("Date",text="Date",anchor=tk.W)

        # sorting columns
        for col in ['Category', 'Amount', 'Type', 'Date']:
            self.my_tree.heading(col, command=lambda c=col: self.sort_column(c))

        # Scroll Bar for treeview
        tree_scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.my_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill="y")
        self.my_tree.configure(yscrollcommand=tree_scroll.set)

        # packing tree view
        self.my_tree.pack(fill=tk.BOTH, expand=True)
    

    # load transactions in json file to the dictionary called dictionary
    def load_transactions(self, filename):
        global transactions
        try:
            # open transactions.json file 
            with open(filename,'r') as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            pass
        else:
            return self.transactions

    
    # display transactions in gui
    def display_transactions(self, transactions):
        self.transactions = transactions
        # getting keys and values of transactions dictionary
        for key, values in transactions.items():
            for items in values:
                # insert values in transactions dictionay to tree view
                self.my_tree.insert("", "end", values=(key, items["amount"],items["type"],items["date"]))
        

        # Search bar and button
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.X)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        search_button = ttk.Button(frame, text="Search", command=self.search_transactions)
        search_button.pack(side=tk.LEFT, padx=5)
        
        
    # defind function for search transactions    
    def search_transactions(self):
        text = self.search_var.get().capitalize()
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        
        for key,values in self.transactions.items():
            for items in values:
                if(text in str(key) or text in str(items["amount"]) or text in str(items["type"]) or text in str(items["date"])):
                    self.my_tree.insert("", "end", values=(key, items["amount"],items["type"],items["date"]))


    # defind function for sort transactions
    def sort_column(self, col):
        # defind a list calld transaction_data
        transaction_data = []
        for child in self.my_tree.get_children(''):
            value = self.my_tree.set(child, col)
            # Convert value to intiger format if possible
            try:
                value = int(value)
            except ValueError:
                pass
            # Append data to transaction_data list
            transaction_data.append((value, child))
            # Sort data ascending order
            transaction_data.sort()

        for index, (value, child) in enumerate(transaction_data):
            self.my_tree.move(child, '', index)
            self.my_tree.set(child, col, value)
        self.my_tree.heading(col, command=lambda : self.sort_column(col))


# main function
def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()
    
    
if __name__ == "__main__":
    main()   
