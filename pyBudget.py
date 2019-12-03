import tkinter as tk
from tkinter import ttk
import math
import os
import sys
import pandas as pd
import matplotlib
import hashlib


largeFont = ("Calibri", 16)
smallFont = ("Calibri", 8)
directory = os.getcwd()


class pyBudget(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for i in (loginScreen, homeScreen, registerScreen, mainScreen):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(homeScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class homeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to pyBudget!", font=largeFont)
        label.pack(pady=30, padx=10)

        button = ttk.Button(self, text="Login Existing User",
                           command=lambda: controller.show_frame(loginScreen))
        button.pack(pady=10)

        button2 = ttk.Button(self, text="Register New User",
                            command=lambda: controller.show_frame(registerScreen))
        button2.pack(pady=10)

        exitButton = ttk.Button(self, text="Exit Application",
                                command=parent.quit)
        exitButton.pack(side='bottom', pady=20)


def login():
    uname = username_try.get()
    pwd = password_try.get()
    unamefield_try.delete(0, tk.END)
    pwdfield_try.delete(0, tk.END)

    logins = {}
    f = open('logins', 'r')
    for line in f:
        logins[line.split()[0]] = line.split()[1]
    f.close()

    if uname in logins.keys():
        pwd = pwd.encode('utf-8')
        hashed_pass = hashlib.sha512(pwd)
        digest = hashed_pass.hexdigest()

        if digest == logins[uname]:
            print('yeet')
            #controller.show_frame(homeScreen)
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


class loginScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login:", font=largeFont)
        label.pack(pady=10, padx=10)

        global username_try
        global password_try
        global unamefield_try
        global pwdfield_try

        username_try = tk.StringVar()
        password_try = tk.StringVar()

        uname = tk.Label(self, text = "Username")
        uname.pack()
        unamefield_try = ttk.Entry(self, textvariable=username_try)
        unamefield_try.pack()

        pwd = tk.Label(self, text = "Password")
        pwd.pack()
        pwdfield_try = ttk.Entry(self, textvariable=password_try, show='*')
        pwdfield_try.pack()

        loginButton = ttk.Button(self, text="Login",
                                    command=login)
        loginButton.pack(pady=20)

        homebutton = ttk.Button(self, text="Home",
                           command=lambda: controller.show_frame(homeScreen))
        homebutton.pack(side='bottom', pady=20)


def register():
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
        popup = tk.Toplevel()
        popup.wm_geometry("300x120")
        
        lab = tk.Label(popup, text="Username already taken, try again!")
        lab.pack(pady=20)
        
        okButton = ttk.Button(popup, text="OK", command=popup.destroy)
        okButton.pack(pady=10)

    elif uname == "":
        popup = tk.Toplevel()
        popup.wm_geometry("300x120")
        
        lab = tk.Label(popup, text="Username field cannot be empty!")
        lab.pack(pady=20)
        
        okButton = ttk.Button(popup, text="OK", command=popup.destroy)
        okButton.pack(pady=10)

    elif pwd == "":
        popup = tk.Toplevel()
        popup.wm_geometry("300x120")
        
        lab = tk.Label(popup, text="Password field cannot be empty!")
        lab.pack(pady=20)
        
        okButton = ttk.Button(popup, text="OK", command=popup.destroy)
        okButton.pack(pady=10)

    else:
        pwd = pwd.encode('utf-8')
        hashed = hashlib.sha512(pwd)
        digest = hashed.hexdigest()

        with open('logins', 'a') as f:
            f.write(uname + " " + digest + "\n")


class registerScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter a username and password to register a new account:", font=largeFont)
        label.pack(pady=10, padx=10)

        global username
        global password
        global unamefield
        global pwdfield

        username = tk.StringVar()
        password = tk.StringVar()

        uname = tk.Label(self, text = "Username")
        uname.pack()
        unamefield = ttk.Entry(self, textvariable=username)
        unamefield.pack()
        unamefield.focus_set()

        pwd = tk.Label(self, text = "Password")
        pwd.pack()
        pwdfield = ttk.Entry(self, textvariable=password, show='*')
        pwdfield.pack()

        registerButton = ttk.Button(self, text="Register",
                                    command=register)
        registerButton.pack(pady=20)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(homeScreen))
        homeButton.pack(side='bottom', pady=20)

    

class mainScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="main screen goes here", font=largeFont)
        label.pack(pady=30, padx=10)

        logoutButton = ttk.Button(self, text="Logout",
                                command=lambda: controller.show_frame(homeScreen))
        logoutButton.pack(side='bottom', pady=20)


if __name__ == "__main__":
    window = pyBudget()
    window.title("pyBudget")
    window.wm_geometry("700x500")
    window.mainloop()
