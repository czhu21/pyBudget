import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
import math
import os
import sys
import pandas as pd
pd.options.display.float_format = '${:,.2f}'.format
import hashlib
from copy import deepcopy
from datetime import date
from decimal import Decimal

global usr
usr = None

today = date.today()
currentDate = today.strftime("%Y/%m/%d")
currentYear = today.strftime("%Y")
currentMonth = today.strftime("%m")
currentDay = today.strftime("%d")
print(currentDate)

gigaFont = ("Calibri", 24, 'bold')
largeFont = ("Calibri", 16)
medFont = ("Calibri", 12)
smallFont = ("Calibri", 8)
directory = os.getcwd()

banned_chars = ['\\', ' ', '`', '\'', '"', '#', ":", ";", "|"]

categories = ['Misc', 'Bills', 'Food', 'Subscriptions', 'Entertainment']
transaction_info = ['Date', 'Type', 'Note', 'Amount', 'y', 'm', 'd']


def alert(message):

    pop = tk.Toplevel()
    pop.wm_geometry("300x120")

    lab = tk.Label(pop, text=message)
    lab.pack(pady=20)

    okButton = ttk.Button(pop, text="OK", command=pop.destroy)
    okButton.pack(pady=10)


class pyBudget(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for i in (homeScreen, loginScreen, registerScreen, mainScreen, pieScreen, budgetScreen):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(homeScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_main(self):
        frame = self.frames[mainScreen]
        frame.tkraise()


class homeScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to pyBudget!", font=gigaFont)
        label.pack(pady=(200, 0), padx=10)
        label = tk.Label(self, text="A Tkinter-based budgeting app by Casey Zhu", font=medFont)
        label.pack(pady=(2, 20), padx=10)

        button = ttk.Button(self, text="Login Existing User",
                            command=lambda: controller.show_frame(loginScreen))
        button.pack(pady=10)

        button2 = ttk.Button(self, text="Register New User",
                             command=lambda: controller.show_frame(registerScreen))
        button2.pack(pady=10)

        exitButton = ttk.Button(self, text="Exit Application",
                                command=parent.quit)
        exitButton.pack(side='bottom', pady=20)


class loginScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Login:", font=largeFont)
        label.pack(pady=(200, 10), padx=10)

        self.username_try = tk.StringVar()
        self.password_try = tk.StringVar()

        nameLabel = tk.Label(self, text="Username:")
        nameLabel.pack()
        self.unamefield_try = ttk.Entry(self, textvariable=self.username_try)
        self.unamefield_try.pack()

        pwd = tk.Label(self, text="Password:")
        pwd.pack()
        self.pwdfield_try = ttk.Entry(self, textvariable=self.password_try, show='*')
        self.pwdfield_try.pack()

        loginButton = ttk.Button(self, text="Login",
                                 command=self.login)
        loginButton.pack(pady=20)

        homebutton = ttk.Button(self, text="Home",
                                command=lambda: controller.show_frame(homeScreen))
        homebutton.pack(side='bottom', pady=20)

    def login(self):
        self.uname = self.username_try.get()

        pwd = self.password_try.get()
        self.unamefield_try.delete(0, tk.END)
        self.pwdfield_try.delete(0, tk.END)

        logins = {}
        f = open('logins', 'r')
        for line in f:
            logins[line.split()[0]] = line.split()[1]
        f.close()

        if self.uname in logins.keys():
            pwd = pwd.encode('utf-8')
            hashed_pass = hashlib.sha512(pwd)
            digest = hashed_pass.hexdigest()

            if digest == logins[self.uname]:
                self.controller.frames[mainScreen].load_user(self.uname)
                self.controller.frames[mainScreen].write_name()
                self.controller.frames[mainScreen].tracker()
                global usr
                usr = deepcopy(self.uname)
                self.controller.show_frame(mainScreen)

            else:
                popup = tk.Toplevel()
                popup.wm_geometry("300x120")

                lab = tk.Label(popup, text="Password incorrect, try again!")
                lab.pack(pady=20)

                okButton = ttk.Button(popup, text="OK", command=popup.destroy)
                okButton.pack(pady=10)

        else:
            popup = tk.Toplevel()
            popup.wm_geometry("300x120")

            lab = tk.Label(popup, text="User not found, try again!")
            lab.pack(pady=20)

            okButton = ttk.Button(popup, text="OK", command=popup.destroy)
            okButton.pack(pady=10)


class registerScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Enter a username and password to register a new account:", font=largeFont)
        label.pack(pady=(200, 10), padx=10)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        uname = tk.Label(self, text="Username:")
        uname.pack()
        self.unameEntry = ttk.Entry(self, textvariable=self.username)
        self.unameEntry.pack()
        self.unameEntry.focus_set()

        pwd = tk.Label(self, text="Password:")
        pwd.pack()
        self.pwdfield = ttk.Entry(self, textvariable=self.password, show='*')
        self.pwdfield.pack()

        registerButton = ttk.Button(self, text="Register",
                                    command=self.register)
        registerButton.pack(pady=20)

        homeButton = ttk.Button(self, text="Home",
                                command=lambda: controller.show_frame(homeScreen))
        homeButton.pack(side='bottom', pady=20)

    def register(self):
        uname = self.username.get()
        pwd = self.password.get()
        self.unameEntry.delete(0, tk.END)
        self.pwdfield.delete(0, tk.END)

        logins = {}
        f = open('logins', 'r')
        for line in f:
            logins[line.split()[0]] = line.split()[1]
        f.close()

        if uname in logins.keys():
            alert("Username already taken, try again!")

        elif uname == "":
            alert("Username field cannot be empty!")

        elif any(i in uname for i in banned_chars):
            alert("Username contains invalid character!")

        elif any(i in pwd for i in banned_chars):
            alert("Password contains invalid character!")

        elif pwd == "":
            alert("Password field cannot be empty!")

        else:
            pwd = pwd.encode('utf-8')
            hashed = hashlib.sha512(pwd)
            digest = hashed.hexdigest()

            with open('logins', 'a') as f:
                f.write(uname + " " + digest + "\n")

            info_df = pd.DataFrame(columns=categories)
            temp = pd.DataFrame({
                'Misc': [0],
                'Bills': [0],
                'Food': [0],
                'Subscriptions': [0],
                'Entertainment': [0]})
            info_df = info_df.append(temp)
            info_filepath = './profiles/' + uname + '.csv'
            info_df.to_csv(info_filepath)

            transactions_df = pd.DataFrame(columns=transaction_info)
            transactions_filepath = './profiles/' + uname + '_transactions.csv'
            transactions_df.to_csv(transactions_filepath)

            alert("Account creation successful!")
            self.controller.show_frame(homeScreen)


class mainScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.username = None
        tk.Frame.__init__(self, parent)

        # Vertical frame for grid reference
        vertframe = ttk.Frame(self, borderwidth=5, width=1, height=800)
        vertframe.grid(column=0, row=1, columnspan=1, rowspan=30)
        # Horizontal frame for grid reference
        horframe = ttk.Frame(self, borderwidth=5, width=1200, height=1)
        horframe.grid(column=0, row=0, columnspan=50, rowspan=1)
        # Username
        self.namelabel = tk.Label(self, text="", font=largeFont)
        self.namelabel.grid(row=2, column=2, columnspan=15)

        toBudget = ttk.Button(self, text="Edit Budget",
                                  command=lambda: controller.show_frame(budgetScreen))
        toBudget.grid(row=3, column=2, columnspan=15)

        # Page title
        # label1 = tk.Label(self, text="Your Transactions:", font=gigaFont)
        # label1.grid(row=3, column=2, columnspan=15)
        
        # Logout button
        logoutButton = ttk.Button(self, text="Logout",
                                  command=lambda: controller.show_frame(homeScreen))
        logoutButton.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky='ew')

        # New transaction label
        label2 = tk.Label(self, text="New Transaction", font=largeFont)
        label2.grid(row=4, column=2, columnspan=15)

        # Dropdown menu for transaction categories
        # self.category = tk.StringVar()
        # self.category.set('Misc')
        # popupMenu = ttk.OptionMenu(self, self.category, *categories)
        # menuLabel = tk.Label(self, text="Select a transaction category:",
        #                      font=medFont)
        # menuLabel.grid(row=5, column=2, columnspan=15)
        # popupMenu.grid(row=6, column=2, rowspan=1, columnspan=15)

        self.category = tk.StringVar()
        # self.category.set('Misc')
        popupMenu = ttk.Combobox(self, textvariable=self.category,
                                 state='readonly')
        popupMenu['values'] = categories
        popupMenu.current(0)
        menuLabel = tk.Label(self, text="Select a transaction category:",
                             font=medFont)
        menuLabel.grid(row=5, column=2, columnspan=15)
        popupMenu.grid(row=6, column=2, rowspan=1, columnspan=15, sticky="ew")

        # Notes
        self.note = tk.StringVar()
        label3 = tk.Label(self, text="Notes:", font=medFont)
        label3.grid(row=7, column=2, columnspan=5, sticky='w')
        self.notesEntry = ttk.Entry(self, textvariable=self.note)
        self.notesEntry.grid(row=7, column=7, columnspan=9, sticky='e')

        # Amount
        self.amount = tk.StringVar()
        label4 = tk.Label(self, text="Amount:", font=medFont)
        label4.grid(row=8, column=2, columnspan=5, sticky='w')
        self.amountEntry = ttk.Entry(self, textvariable=self.amount)
        self.amountEntry.grid(row=8, column=7, columnspan=9, sticky='e')

        # Add Transaction
        transactionButton = ttk.Button(self, text="Add Transaction",
                                       command=self.add_transaction)
        transactionButton.grid(row=9, column=2, columnspan=15)

        # View Pie Chart of Transactions
        transactionButton = ttk.Button(self, text="View Current Month Spending",
                                       command=self.pieplot)
        transactionButton.grid(row=12, column=8, padx=(20, 0))

        # Text widget for displaying transaction history
        self.history1 = tk.Text(self, height=24, width=20)
        self.history1.grid(row=3, column=22, rowspan=7, columnspan=5)
        
        self.history2 = tk.Text(self, height=24, width=20)
        self.history2.grid(row=3, column=27, rowspan=7, columnspan=6)
        
        self.history3 = tk.Text(self, height=24, width=24)
        self.history3.grid(row=3, column=33, rowspan=7, columnspan=7)
        
        self.history4 = tk.Text(self, height=24, width=20)
        self.history4.grid(row=3, column=40, rowspan=7, columnspan=5)
        

    def write_name(self):
        welcome = "Welcome " + self.username + "!"
        self.namelabel.config(text=welcome)

    def add_transaction(self):
        tcat = self.category.get()
        tnote = self.note.get()
        try:
            tamt = round(float(self.amount.get()), 2)
        except ValueError:
            alert("Amount must be a number!")
            self.amountEntry.delete(0, tk.END)
            return

        if tamt > 999999:
            alert("You don't have that much money.")
            self.amountEntry.delete(0, tk.END)
            return
        
        if len(tnote) > 20:
            alert("Note length must be <20 characters!")
            self.notesEntry.delete(0, tk.END)
            return

        self.amountEntry.delete(0, tk.END)
        self.notesEntry.delete(0, tk.END)

        if tnote.strip() == '':
            alert("Note field cannot be empty!")
        else:
            temp = pd.DataFrame({
                'Date': [currentDate],
                'Type': [tcat],
                'Note': [tnote],
                'Amount': [tamt],
                'y': [int(currentYear)],
                'm': [int(currentMonth)],
                'd': [int(currentDay)]
                })
            self.transactions = self.transactions.append(temp)
            print(self.transactions)
            path = './profiles/' + self.username + '_transactions.csv'
            self.transactions.to_csv(path)
            self.tracker()

    def load_user(self, uname):
        self.username = uname

        path = './profiles/' + self.username + '.csv'
        self.bud_nums = pd.read_csv(path, index_col=0)
        path = './profiles/' + self.username + '_transactions.csv'
        self.transactions = pd.read_csv(path, index_col=0)
        print(self.bud_nums)
        print(self.transactions)

    def pieplot(self):
        self.controller.frames[pieScreen].plot()
        self.controller.show_frame(pieScreen)

    def tracker(self):
        
        self.history1.delete('1.0', tk.END)
        self.history2.delete('1.0', tk.END)
        self.history3.delete('1.0', tk.END)
        self.history4.delete('1.0', tk.END)

        if self.transactions.size == 0:
            self.history1.insert(tk.END, "Date")
            self.history1.tag_configure("right", justify='right')
            self.history1.tag_add("right", 1.0, "end")
            self.history2.insert(tk.END, "Type")
            self.history2.tag_configure("right", justify='right')
            self.history2.tag_add("right", 1.0, "end")
            self.history3.insert(tk.END, "Note")
            self.history3.tag_configure("right", justify='right')
            self.history3.tag_add("right", 1.0, "end")
            self.history4.insert(tk.END, "Amount")
            self.history4.tag_configure("right", justify='right')
            self.history4.tag_add("right", 1.0, "end")
            return

        last25 = self.transactions.tail(25)
        self.history1.insert(tk.END, last25[['Date']].to_string(index=False))
        self.history1.tag_configure("left", justify='left')
        self.history1.tag_add("left", 1.0, "end")
        # self.history1.tag_configure("bold", font=('bold'))
        # self.history1.tag_add("bold", "1.0", "1.2")

        self.history2.insert(tk.END, last25[['Type']].to_string(index=False))
        self.history2.tag_configure("right", justify='right')
        self.history2.tag_add("right", 1.0, "end")
        
        self.history3.insert(tk.END, last25[['Note']].to_string(index=False))
        self.history3.tag_configure("right", justify='right')
        self.history3.tag_add("right", 1.0, "end")
        
        amt = last25[['Amount']].round(2)
        self.history4.insert(tk.END, last25[['Amount']].round(2).to_string(index=False))
        self.history4.tag_configure("right", justify='right')
        self.history4.tag_add("right", 1.0, "end")


class pieScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        # Vertical frame for grid reference
        vertframe = ttk.Frame(self, borderwidth=5, width=1, height=800)
        vertframe.grid(column=0, row=1, columnspan=1, rowspan=30)
        # Horizontal frame for grid reference
        horframe = ttk.Frame(self, borderwidth=5, width=1200, height=1)
        horframe.grid(column=0, row=0, columnspan=50, rowspan=1)

        label = tk.Label(self, text="Pie Chart of Spending:", font=largeFont)
        label.grid(row=2, column=2, pady=0, padx=0)

        mainButton = ttk.Button(self, text="OK",
                                command=lambda: controller.show_frame(mainScreen))
        mainButton.grid(row=3, column=2, sticky='', padx=(0, 0))

    def plot(self):
        # code to plot pie chart goes here
        print('yes')


class budgetScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
       
        # Vertical frame for grid reference
        vertframe = ttk.Frame(self, borderwidth=5, width=1, height=800)
        vertframe.grid(column=0, row=1, columnspan=1, rowspan=30)
        # Horizontal frame for grid reference
        horframe = ttk.Frame(self, borderwidth=5, width=1200, height=1)
        horframe.grid(column=0, row=0, columnspan=50, rowspan=1)

        mainButton = ttk.Button(self, text="Back",
                                command=lambda: controller.show_frame(mainScreen))
        mainButton.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky='ew')
        
        title = tk.Label(self, text="Edit your budget:", font=largeFont)
        title.grid(row=2, column=2, columnspan=2)
        
        # Bills
        self.bills = tk.StringVar()
        label1 = tk.Label(self, text="Bills:", font=medFont)
        label1.grid(row=4, column=2, columnspan=1, sticky='w')
        self.billsEntry = ttk.Entry(self, textvariable=self.bills)
        self.billsEntry.grid(row=4, column=3)

        # Food
        self.food = tk.StringVar()
        label1 = tk.Label(self, text="Food:", font=medFont)
        label1.grid(row=5, column=2, columnspan=1, sticky='w')
        self.foodEntry = ttk.Entry(self, textvariable=self.food)
        self.foodEntry.grid(row=5, column=3)

        # Subscriptions
        self.subscriptions = tk.StringVar()
        label1 = tk.Label(self, text="Subscriptions:", font=medFont)
        label1.grid(row=6, column=2, columnspan=1, sticky='w')
        self.subscriptionsEntry = ttk.Entry(self, textvariable=self.subscriptions)
        self.subscriptionsEntry.grid(row=6, column=3)

        # Entertainment
        self.entertainment = tk.StringVar()
        label1 = tk.Label(self, text="Entertainment:", font=medFont)
        label1.grid(row=7, column=2, columnspan=1, sticky='w')
        self.entertainmentEntry = ttk.Entry(self, textvariable=self.entertainment)
        self.entertainmentEntry.grid(row=7, column=3)

        # Misc
        self.misc = tk.StringVar()
        label1 = tk.Label(self, text="Miscellaneous:", font=medFont)
        label1.grid(row=8, column=2, columnspan=1, sticky='w')
        self.miscEntry = ttk.Entry(self, textvariable=self.misc)
        self.miscEntry.grid(row=8, column=3)

        # Save
        transactionButton = ttk.Button(self, text="Save Changes",
                                       command=self.save)
        transactionButton.grid(row=9, column=2, columnspan=2, sticky='ew')

    def save(self):
        print(self.controller.frames[mainScreen].username)


if __name__ == "__main__":
    window = pyBudget()
    window.title("pyBudget")
    window.wm_geometry("1200x640")
    window.mainloop()
