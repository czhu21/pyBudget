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
import hashlib
from copy import deepcopy
from datetime import date

global usr
usr = None

today = date.today()
currentDay = today.strftime("%m/%d/%y")
print(currentDay)

gigaFont = ("Calibri", 24, 'bold')
largeFont = ("Calibri", 16)
medFont = ("Calibri", 12)
smallFont = ("Calibri", 8)
directory = os.getcwd()

banned_chars = ['\\', ' ', '`', '\'', '"', '#', ":", ";", "|"]

categories = ['rent', 'bills', 'food', 'subscriptions', 'entertainment', 'misc']
transaction_info = ['date', 'type', 'note', 'amt']


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

        for i in (homeScreen, loginScreen, registerScreen, mainScreen):
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

        global username_try
        global password_try
        global unamefield_try
        global pwdfield_try

        username_try = tk.StringVar()
        password_try = tk.StringVar()

        nameLabel = tk.Label(self, text="Username:")
        nameLabel.pack()
        unamefield_try = ttk.Entry(self, textvariable=username_try)
        unamefield_try.pack()

        pwd = tk.Label(self, text="Password:")
        pwd.pack()
        pwdfield_try = ttk.Entry(self, textvariable=password_try, show='*')
        pwdfield_try.pack()

        loginButton = ttk.Button(self, text="Login",
                                 command=self.login)
        loginButton.pack(pady=20)

        homebutton = ttk.Button(self, text="Home",
                                command=lambda: controller.show_frame(homeScreen))
        homebutton.pack(side='bottom', pady=20)

    def login(self):
        self.uname = username_try.get()

        pwd = password_try.get()
        unamefield_try.delete(0, tk.END)
        pwdfield_try.delete(0, tk.END)

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
                self.controller.frames[mainScreen].set_uname(self.uname)

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

        global username
        global password
        global unamefield
        global pwdfield

        username = tk.StringVar()
        password = tk.StringVar()

        uname = tk.Label(self, text="Username:")
        uname.pack()
        unamefield = ttk.Entry(self, textvariable=username)
        unamefield.pack()
        unamefield.focus_set()

        pwd = tk.Label(self, text="Password:")
        pwd.pack()
        pwdfield = ttk.Entry(self, textvariable=password, show='*')
        pwdfield.pack()

        registerButton = ttk.Button(self, text="Register",
                                    command=self.register)
        registerButton.pack(pady=20)

        homeButton = ttk.Button(self, text="Home",
                                command=lambda: controller.show_frame(homeScreen))
        homeButton.pack(side='bottom', pady=20)

    def register(self):
        uname = username.get()
        pwd = password.get()
        unamefield.delete(0, tk.END)
        pwdfield.delete(0, tk.END)

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
            info_filepath = './profiles/' + uname + '.csv'
            info_df.to_csv(info_filepath)

            transactions_df = pd.DataFrame(columns=transaction_info)
            transactions_filepath = './profiles/' + uname + '_transactions.csv'
            transactions_df.to_csv(transactions_filepath)

            alert("Account creation successful!")
            self.controller.show_frame(homeScreen)


class mainScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.username = None

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Budget Home:", font=largeFont)
        label.grid(pady=30, padx=50)

        # testButton = ttk.Button(self, text="test",
        #                         command=self.pr)
        # testButton.pack(side='top', pady=20)

        # test2Button = ttk.Button(self, text="test2",
        #                          command=lambda: print(usr))
        # test2Button.pack(side='top', pady=20)

        # logoutButton = ttk.Button(self, text="Logout",
        #                           command=lambda: controller.show_frame(homeScreen))
        # logoutButton.pack(side='bottom', pady=20)

    def pr(self):
        # print(self.bud_nums)
        print(usr)
        print(type(usr))

    def get_username(self):
        username = usr
        return username

    def set_uname(self, uname):
        self.username = uname

        path = './profiles/' + self.username + '.csv'
        bud_nums = pd.read_csv(path, index_col=0)
        path = './profiles/' + self.username + '_transactions.csv'
        transactions = pd.read_csv(path, index_col=0)
        print(bud_nums)
        print(transactions)


if __name__ == "__main__":
    window = pyBudget()
    window.title("pyBudget")
    window.wm_geometry("1200x800")
    window.mainloop()
