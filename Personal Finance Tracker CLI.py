import tkinter as tk
from tkinter import ttk
import json
import datetime

# main Dictionary called transactions
transactions = {}

# error handling function for main menu 
def choice_error(message,error_message="Invalid Choice,Please Enter Choice Between 1 And 8"):
    while True:
        try:
            choice = int(input(message))
        except ValueError:
            print(error_message)
        else:
            # check user input choice is between 1 and 8 range
            if choice > 0 and choice <= 8:
                return choice
            else:
                # if choice not in range error message displaying and ask to re enter
                print(error_message)
                continue

# error handling function for transaction amount
def transaction_amount_error(message,error_message="Please Enter A integer Amount"):
    while True:
        try:
           # check if the user input value is number or not
           transaction_amount = int(input(message))
        except ValueError:
             # if user input is not a number,display error message and ask to re enter
             print(error_message)
             continue
        else:
            return transaction_amount
        
# error handling function for task type
def task_type_error(message,error_message="Please Enter Task Type Income Or Expense : "):
    while True:
        try:
            task_type = str(input(message).capitalize())
        except ValueError:
            print(error_message)
            
        else:
            # check user input string is equals with "Income" or "Expense"
            if task_type == "Income" or task_type == "Expense":
                return task_type
            else:
                print(error_message)
                continue

# error handling function for task date
def task_date_error(message,error_message="Please Enter Valid Data Type (YYYY-MM-DD)"):
    while True:
        task_date = input(message)
        try:
            # check user input date is in correct format or not
            datetime.datetime.strptime(task_date,"%Y-%m-%d")
            return task_date
        except ValueError:
            print(error_message)
            continue

# error handling function for task index number
def index_error(task_name,message,error_message="This Index is not in the list."):
    while True:
        try:
            value = int(input(message))
        except ValueError:
            print('Please Enter A Integer Number.')
            continue
        else:
            # check the user input index number is in correct range or not
            if value < 1 or value > len(transactions[task_name]):
                print(error_message)
                continue
            else:
                return value
# error handling function for key error inside dictionary
def key_error(message,error_message="This Task not in transactions"):
    while True:
        try:
            task_name = str(input(message)).capitalize()
        except ValueError:
            print('Please Enter A valid name.')
            continue
        else:
            # check the user input task name is in transactions
            if task_name in transactions:
                return task_name
            else:
                print(error_message)
                continue

# load json file to the programme
def load_transactions():
    global transactions
    try:
        # open transactions.json file 
        with open('transactions.json','r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        pass

def save_transactions():
    # open transactions.json file and write the transactions on it
    with open('transactions.json','w') as f:
        f.write(json.dumps(transactions,indent=3))

# function for read bulk transactions
def read_bulk_transactions_from_file(transactions):
    while True:
        try:
            # getting user input for the file name
            file_path=input("Enter The Text File Name :")
            with open(f"{file_path}.txt","r") as file:
                # read data inside txt file line by line
                for line in file:
                    line = line.strip().split(',')
                    # Check if the line has the correct number of elements
                    if len(line) == 4:
                        task_name = line[0].capitalize()
                        transaction_amount = int(line[1])
                        task_type = line[2].capitalize()
                        task_date = line[3]
                    # adding the data inside the tct file to the json file
                    if task_name not in transactions:
                        transactions[task_name] = []
                    transactions[task_name].append({"amount":transaction_amount,"type":task_type,"date":task_date})
                save_transactions()
            break
        except FileNotFoundError:
            print('Please Enter Valid File Name')
            continue

# function for add transactions
def add_transaction():
    task_name = input('Enter Task Name : ').capitalize()
    transaction_amount = transaction_amount_error('Enter Amount : ')
    task_type = task_type_error('Enter Task Type (Income/Expense) : ' )
    task_date = task_date_error('Enter The Date Of Task (YYYY-MM-DD) : ')
    if task_name in transactions:
    # check task_name is already in the transactions dictionary
        transactions[task_name].append({"amount":transaction_amount,"type":task_type,"date":task_date})
    else:
        transactions[task_name] = [{"amount":transaction_amount,"type":task_type,"date":task_date}]
    print('Transaction Added Successfully.')
    save_transactions()

# function for view transactions
def view_transactions():
    for key,values in transactions.items():
        print(f'{key}\n')
        count = 1
        for i in transactions[key]:
            print(f'{count} {i}\n')
            count +=1 
    

# Function For Update Transactions
def update_transaction():
    view_transactions()
    task_name = key_error("Enter Task Name : ")
    task_number = index_error(task_name,'Enter Task number : ')-1
    transaction_amount = transaction_amount_error('Enter Amount : ')
    task_type = task_type_error('Enter Task Type (Income/Expense) : ' )
    task_date = task_date_error('Enter The Date Of Task (YYYY-MM-DD) : ')
    transactions[task_name][task_number]["amount"] = transaction_amount
    transactions[task_name][task_number]["type"] = task_type
    transactions[task_name][task_number]["date"] = task_date
    save_transactions()
    print("Transactions Updated Successfully.")

def delete_transaction():
    view_transactions()
    task_name = key_error("Enter Task Name : ")
    task_number = index_error(task_name,'Enter Transaction Number You Want To Delete : ')-1
    del transactions[task_name][task_number]
    # check the task category is empty or not after delete the tasks
    if len(transactions[task_name]) ==0:
        # if it is empty then delete entire task category from dictionary
        del transactions[task_name]
    save_transactions()
    print("Transactions Deleted Successfully.")

# function for display summary of incomes and expenses
def display_summary():
    # variable initialize
    income = 0
    expense = 0
    for key,values in transactions.items():
        for item in values:
            # calculate the total of expenses
            if item["type"] == "Expense":
                total = int(item["amount"])
                expense +=total
            else:
                # calculate the total of incomes
                total = int(item["amount"])
                income +=total
            
    print(f'Total Expenses : {expense}')
    print(f'Total Incomes  : {income}')


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
        #search_entry.pack(side=tk.LEFT, padx=5, pady=5)
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
def gui():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()
 
# main menu function
def main_menu():
    load_transactions()  
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transaction")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Bulk Transaction")
        print("7.GUI Window")
        print("8.Exit Programme")
        choice = choice_error('Enter Your choice : ')
        print()
        if choice == 1:
            add_transaction()
        elif choice == 2:
            view_transactions()
        elif choice == 3:
            update_transaction()
        elif choice == 4:
            delete_transaction()
        elif choice == 5:
            display_summary()
        elif choice == 6:
            read_bulk_transactions_from_file(transactions)
        elif choice == 7:
            gui()
        elif choice == 8:
            print('Programme Ended.')
            break



# calling main Function Of Programme
if __name__ == "__main__":
    main_menu()