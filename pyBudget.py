# Casey Zhu
# Software Carpentry Final Project
# Designing a tkinter-based budgeting application

# For dummy data:
# Username 'Software_Carpentry'
# Password 'password123'

import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import pandas as pd
import hashlib
from datetime import date
from calendar import month_name

matplotlib.use("TkAgg")

# Format float values into money format ($x.yz)
pd.options.display.float_format = '${:,.2f}'.format

# Get date/date values
today = date.today()
currentDate = today.strftime("%Y/%m/%d")
currentYear = int(today.strftime("%Y"))
currentMonth = int(today.strftime("%m"))
currentDay = int(today.strftime("%d"))

# Set fonts
gigaFont = ("Calibri", 24, 'bold')
largeFont = ("Calibri", 16)
medFont = ("Calibri", 12)
smallFont = ("Calibri", 8)

# Set global lists for reference
banned_chars = ['\\', ' ', '`', '\'', '"', '#', ":", ";", "|"]
categories = ['Bills', 'Food', 'Subscriptions', 'Entertainment', 'Misc']
transaction_info = ['Date', 'Type', 'Note', 'Amount', 'y', 'm', 'd']
months = {}
for i in range(1, 13):
    months[month_name[i]] = i


def alert(message):
    '''
    Creates popup alert message

    **Parameters**
        message: str
            The message to display on the popup
    '''

    # Create popup window and send to top
    pop = tk.Toplevel()
    pop.wm_geometry("300x150")

    # Add label and OK button to popup
    lab = tk.Label(pop, text=message)
    lab.pack(pady=(35, 20))

    okButton = ttk.Button(pop, text="OK", command=pop.destroy)
    okButton.pack(pady=10)


class pyBudget(tk.Tk):
    '''
    pyBudget object that forms the structure of the various
    frames in the program
    '''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for i in (homeScreen, loginScreen,
                  registerScreen, mainScreen,
                  pieScreen, budgetScreen,
                  barScreen):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(homeScreen)

    def show_frame(self, cont):
        '''
        Switches frame to the container input

        **Parameters**
            cont: tk.Frame object
                The frame we want to switch to
        '''

        frame = self.frames[cont]
        frame.tkraise()


class homeScreen(tk.Frame):
    '''
    Object that defines the home screen
    '''

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to pyBudget!", font=gigaFont)
        label.pack(pady=(200, 0), padx=10)
        t = "A Tkinter-based budgeting app by Casey Zhu"
        label = tk.Label(self, text=t, font=medFont)
        label.pack(pady=(2, 20), padx=10)

        button = ttk.Button(self, text="Login Existing User",
                            command=lambda: controller.show_frame(loginScreen))
        button.pack(pady=10)

        button2 =\
            ttk.Button(self, text="Register New User",
                       command=lambda: controller.show_frame(registerScreen))
        button2.pack(pady=10)

        exitButton = ttk.Button(self, text="Exit Application",
                                command=parent.quit)
        exitButton.pack(side='bottom', pady=20)


class loginScreen(tk.Frame):
    '''
    Object that defines the login screen
    '''

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        # Login label
        label = tk.Label(self, text="Login:", font=largeFont)
        label.pack(pady=(200, 10), padx=10)

        # Define empty tk string objects to fill from entry fields
        self.username_try = tk.StringVar()
        self.password_try = tk.StringVar()

        # Set up username entry field
        nameLabel = tk.Label(self, text="Username:")
        nameLabel.pack()
        self.unamefield_try = ttk.Entry(self, textvariable=self.username_try)
        self.unamefield_try.pack()

        # Set up password entry field
        pwd = tk.Label(self, text="Password:")
        pwd.pack()
        self.pwdfield_try = ttk.Entry(self, textvariable=self.password_try,
                                      show='*')
        self.pwdfield_try.pack()

        # Set up login execution button to call login()
        loginButton = ttk.Button(self, text="Login",
                                 command=self.login)
        loginButton.pack(pady=20)

        # Set up home button to return to homeScreen
        homebutton =\
            ttk.Button(self, text="Home",
                       command=lambda: controller.show_frame(homeScreen))
        homebutton.pack(side='bottom', pady=20)

    def login(self):
        '''
        Executes login based on input username and password
        from loginScreen.

        **Parameters**
            None
        '''

        # Get username and password from entry fields
        self.uname = self.username_try.get()
        pwd = self.password_try.get()

        # Clear entry fields
        self.unamefield_try.delete(0, tk.END)
        self.pwdfield_try.delete(0, tk.END)

        # Load record of created profiles
        logins = {}
        f = open('logins', 'r')
        for line in f:
            logins[line.split()[0]] = line.split()[1]
        f.close()

        # Authenticate input username and password
        # Check if username is valid
        if self.uname in logins.keys():
            # Hash password input
            pwd = pwd.encode('utf-8')
            hashed_pass = hashlib.sha512(pwd)
            digest = hashed_pass.hexdigest()

            if digest == logins[self.uname]:
                # If password is correct for user, load dfs and mainScreen
                self.controller.frames[mainScreen].load_user(self.uname)
                self.controller.frames[mainScreen].write_name()
                self.controller.frames[mainScreen].tracker()

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
    '''
    Object that defines the registration screen
    '''

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        # Registration title
        t = "Enter a username and password to register a new account:"
        label = tk.Label(self, text=t, font=largeFont)
        label.pack(pady=(200, 10), padx=10)

        # Initialize username/password inputs
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # Username entry label and field
        uname = tk.Label(self, text="Username:")
        uname.pack()
        self.unameEntry = ttk.Entry(self, textvariable=self.username)
        self.unameEntry.pack()
        self.unameEntry.focus_set()

        # Password entry label and field
        pwd = tk.Label(self, text="Password:")
        pwd.pack()
        self.pwdfield = ttk.Entry(self, textvariable=self.password, show='*')
        self.pwdfield.pack()

        # Register button, calls self.register()
        registerButton = ttk.Button(self, text="Register",
                                    command=self.register)
        registerButton.pack(pady=20)

        # Button to go to homeScreen
        homeButton =\
            ttk.Button(self, text="Home",
                       command=lambda: controller.show_frame(homeScreen))
        homeButton.pack(side='bottom', pady=20)

    def register(self):
        '''
        Checks if given username/password are valid
        Adds to logins file if so, creates
        dataframes for user to track transactions/budget
        '''

        uname = self.username.get()
        pwd = self.password.get()
        self.unameEntry.delete(0, tk.END)
        self.pwdfield.delete(0, tk.END)

        # Get list of registered logins
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
            # Encrypts password, adds username and password
            # to logins file
            pwd = pwd.encode('utf-8')
            hashed = hashlib.sha512(pwd)
            digest = hashed.hexdigest()

            with open('logins', 'a') as f:
                f.write(uname + " " + digest + "\n")

            # Create and save dataframes to track user actions
            info_df = pd.DataFrame(columns=categories)
            temp = pd.DataFrame({
                'Misc': [0.0],
                'Bills': [0.0],
                'Food': [0.0],
                'Subscriptions': [0.0],
                'Entertainment': [0.0]})
            info_df = info_df.append(temp)
            info_filepath = './profiles/' + uname + '.csv'
            info_df.to_csv(info_filepath)

            transactions_df = pd.DataFrame(columns=transaction_info)
            transactions_filepath = './profiles/' + uname + '_transactions.csv'
            transactions_df.to_csv(transactions_filepath)

            alert("Account creation successful!")
            self.controller.show_frame(homeScreen)


class mainScreen(tk.Frame):
    '''
    Object that defines the main screen
    '''

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
                              command=self.editBudget)
        toBudget.grid(row=3, column=2, columnspan=15)

        # Page title
        # label1 = tk.Label(self, text="Your Transactions:", font=gigaFont)
        # label1.grid(row=3, column=2, columnspan=15)

        # Logout button
        logoutButton =\
            ttk.Button(self, text="Logout",
                       command=lambda: controller.show_frame(homeScreen))
        logoutButton.grid(row=0, column=0, sticky='ew')

        # New transaction label
        label2 = tk.Label(self, text="Add New Transaction:", font=largeFont)
        label2.grid(row=4, column=2, columnspan=15)

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
        label4.grid(row=8, column=2, columnspan=6)
        self.amountEntry = ttk.Entry(self, textvariable=self.amount)
        self.amountEntry.grid(row=8, column=7, columnspan=9, sticky='e')

        # Add Transaction
        transactionButton = ttk.Button(self, text="Add Transaction",
                                       command=self.add_transaction)
        transactionButton.grid(row=9, column=2, columnspan=15)

        # View Pie Chart of Transactions
        transactionButton = ttk.Button(self, text="Current Month Spending",
                                       command=self.pieplot)
        transactionButton.grid(row=12, column=8, padx=(20, 0))

        # View Bar Chart, comparing spending to budget
        transactionButton = ttk.Button(self, text="Compare Spending w/ Budget",
                                       command=self.barplot)
        transactionButton.grid(row=13, column=8, padx=(20, 0))

        # Text widget for displaying transaction history
        # Date
        self.history1 = tk.Text(self, height=24, width=20)
        self.history1.grid(row=3, column=22, rowspan=7, columnspan=5)
        # Type
        self.history2 = tk.Text(self, height=24, width=20)
        self.history2.grid(row=3, column=27, rowspan=7, columnspan=6)
        # Note
        self.history3 = tk.Text(self, height=24, width=30)
        self.history3.grid(row=3, column=33, rowspan=7, columnspan=7)
        # Amount
        self.history4 = tk.Text(self, height=24, width=20)
        self.history4.grid(row=3, column=40, rowspan=7, columnspan=5)

        self.history1.config(state='disabled')
        self.history2.config(state='disabled')
        self.history3.config(state='disabled')
        self.history4.config(state='disabled')

    def write_name(self):
        '''
        Prints username to mainscreen welcome message

        **Parameters**
            None
        '''

        welcome = "Welcome " + self.username + "!"
        self.namelabel.config(text=welcome)

    def add_transaction(self):
        '''
        Adds a transaction to the user's transaction
        history.
        Refreshes transaction tracker at the end.

        **Parameters**
            None
        '''

        # Get input transaction category, note, and amount
        tcat = self.category.get()
        tnote = self.note.get()

        # Check if amount is valid
        try:
            tamt = round(float(self.amount.get()), 2)
        except ValueError:
            alert("Amount must be a number!")
            self.amountEntry.delete(0, tk.END)
            return

        if tamt > 999999:
            # Let's be realistic here.
            # No one that rich is using my application.
            alert("""You don't have that much money.""")
            self.amountEntry.delete(0, tk.END)
            return

        # Check if note is valid
        if len(tnote) > 20:
            alert("Note length must be <20 characters!")
            self.notesEntry.delete(0, tk.END)
            return

        # Clear entry fields
        self.amountEntry.delete(0, tk.END)
        self.notesEntry.delete(0, tk.END)

        # If all are valid, prepare df of transaction information
        # and add df to existing transaction history
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
            path = './profiles/' + self.username + '_transactions.csv'
            self.transactions.to_csv(path)

            # Refresh tracker to print new transaction
            self.tracker()

    def load_user(self, uname):
        '''
        Load transaction history and budget information for a user

        **Parameters**
            uname: str
                The current user's username
        '''

        self.username = uname

        path = './profiles/' + self.username + '.csv'
        self.bud_nums = pd.read_csv(path, index_col=0)
        path = './profiles/' + self.username + '_transactions.csv'
        self.transactions = pd.read_csv(path, index_col=0)

    def pieplot(self):
        '''
        Method to transition from mainScreen to pieScreen
        Calls plot() method from pieScreen class

        **Parameters**
            None
        '''

        self.controller.frames[pieScreen].plot()
        self.controller.show_frame(pieScreen)

    def barplot(self):
        '''
        Method to transition from mainScreen to barScreen
        Calls start() method from barScreen

        **Parameters**
            None
        '''

        self.controller.frames[barScreen].start()
        self.controller.show_frame(barScreen)

    def tracker(self):
        '''
        Gets transaction history and displays to screen

        **Parameters**
            None
        '''

        # Set textboxes to normal state so text can be inserted
        self.history1.config(state='normal')
        self.history2.config(state='normal')
        self.history3.config(state='normal')
        self.history4.config(state='normal')

        # Clear all content in text boxes
        self.history1.delete('1.0', tk.END)
        self.history2.delete('1.0', tk.END)
        self.history3.delete('1.0', tk.END)
        self.history4.delete('1.0', tk.END)

        # Check in case transaction history is empty
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

        # Get most recent 20 transactions
        # Add info (date, type, note, amount) to corresponding textboxes
        last20 = self.transactions.tail(20)
        last20 = last20[::-1]
        self.history1.insert(tk.END, last20[['Date']].to_string(index=False))
        self.history1.tag_configure("right", justify='right')
        self.history1.tag_add("right", 1.0, "end")

        self.history2.insert(tk.END, last20[['Type']].to_string(index=False))
        self.history2.tag_configure("right", justify='right')
        self.history2.tag_add("right", 1.0, "end")

        self.history3.insert(tk.END, last20[['Note']].to_string(index=False))
        self.history3.tag_configure("right", justify='right')
        self.history3.tag_add("right", 1.0, "end")

        amt = last20[['Amount']].round(2)
        self.history4.insert(tk.END, amt.to_string(index=False))
        self.history4.tag_configure("right", justify='right')
        self.history4.tag_add("right", 1.0, "end")

        # Re-disable textboxes so they cannot be altered by user
        self.history1.config(state='disabled')
        self.history2.config(state='disabled')
        self.history3.config(state='disabled')
        self.history4.config(state='disabled')

    def editBudget(self):
        '''
        Transitions from mainScreen to budgetScreen.
        Calls loadBudget() method from budgetScreen
        '''

        self.controller.frames[budgetScreen].loadBudget()
        self.controller.show_frame(budgetScreen)


class pieScreen(tk.Frame):
    '''
    Object that defines the pie chart screen
    '''

    def __init__(self, parent, controller):
        self.controller = controller
        self.transactions = None
        tk.Frame.__init__(self, parent)

        # Vertical frame for grid reference
        vertframe = ttk.Frame(self, borderwidth=5, width=1, height=800)
        vertframe.grid(column=0, row=1, columnspan=1, rowspan=30)
        # Horizontal frame for grid reference
        horframe = ttk.Frame(self, borderwidth=5, width=1200, height=1)
        horframe.grid(column=0, row=0, columnspan=50, rowspan=1)

        # Title label
        t = "Spending breakdown for the month of %s, %d" \
            % (month_name[currentMonth], currentYear)
        label = tk.Label(self, text=t, font=gigaFont)
        label.grid(row=0, column=1, columnspan=45, sticky='ew')

        # Button to go back to mainScreen
        mainButton =\
            ttk.Button(self, text="OK",
                       command=lambda: controller.show_frame(mainScreen))
        mainButton.grid(row=0, column=0, sticky='nw', padx=(0, 0))

        # Figure/canvas objects to contain pie chart
        self.fig = Figure(figsize=(7, 6), dpi=105)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=2, column=1, rowspan=20,
                                         columnspan=45, sticky='ew')
        self.canvas._tkcanvas.grid(row=2, column=1, rowspan=20,
                                   columnspan=45, sticky='ew')

    def plot(self):
        '''
        Plots pie chart based on total spending for the current month
        '''

        self.fig.clf()
        self.sub = self.fig.add_subplot(111)
        self.transactions = self.controller.frames[mainScreen].transactions

        # Get transaction data for current month
        data = self.transactions[(self.transactions['y'] == currentYear) &
                                 (self.transactions['m'] == currentMonth)]
        print(data)
        # Check to see if there is no data for current month
        if data.size == 0:
            alert('No transactions this month!')
            return

        # Get spending totals for each category from data
        bills = data.loc[data['Type'] == 'Bills', 'Amount'].sum()
        food = data.loc[data['Type'] == 'Food', 'Amount'].sum()
        subs = data.loc[data['Type'] == 'Subscriptions', 'Amount'].sum()
        ent = data.loc[data['Type'] == 'Entertainment', 'Amount'].sum()
        misc = data.loc[data['Type'] == 'Misc', 'Amount'].sum()

        labels = categories
        sizes = [bills, food, subs, ent, misc]
        print(sizes)

        # Function to get spending totals to show on pie chart
        def val(i):
            amt = round(i / 100 * sum(sizes), 0)
            amt = '${:,.0f}'.format(amt)
            return(amt)

        # Plot and show pie chart
        self.sub.pie(sizes, labels=labels, autopct=val, startangle=90)
        self.sub.legend(categories, loc='best')
        self.sub.axis('equal')
        self.canvas.draw()


class barScreen(tk.Frame):
    '''
    Object that defines the bar plot screen
    '''

    def __init__(self, parent, controller):
        self.controller = controller
        self.transactions = None
        self.bud_nums = None
        self.username = None
        self.budget_total = 0
        self.budget = None
        self.fig = None
        self.fig2 = None
        tk.Frame.__init__(self, parent)

        # Vertical frame for grid reference
        vertframe = ttk.Frame(self, borderwidth=5, width=1, height=800)
        vertframe.grid(column=0, row=1, columnspan=1, rowspan=30)
        # Horizontal frame for grid reference
        horframe = ttk.Frame(self, borderwidth=5, width=1200, height=1)
        horframe.grid(column=0, row=0, columnspan=50, rowspan=1)

        # Title
        t = "Select a year and month to view spending totals"
        label = tk.Label(self, text=t, font=gigaFont)
        label.grid(row=0, column=0, columnspan=50, sticky='ew')

        # Button to go back to mainScreen
        mainButton =\
            ttk.Button(self, text="OK",
                       command=self.back)
        mainButton.grid(row=0, column=0, sticky='nw', padx=(0, 0))

        # Year selection box
        self.yearselection = tk.StringVar()
        self.yearmenu = ttk.Combobox(self, textvariable=self.yearselection,
                                     state='readonly')
        self.yearmenu['values'] = ['']
        self.yearmenu.current(0)
        self.yearmenu.grid(row=1, column=14, rowspan=1,
                           columnspan=6, sticky="ew")

        # Month selection box
        self.monthselection = tk.StringVar()
        self.monthmenu = ttk.Combobox(self, textvariable=self.monthselection,
                                      state='readonly')
        self.monthmenu['values'] = list(months.keys())
        self.monthmenu.current(0)
        self.monthmenu.grid(row=1, column=22, rowspan=1,
                            columnspan=6, sticky="ew")

        # Go button to graph spending for selected month
        self.goButton = ttk.Button(self, text="Go",
                                   command=self.graphSpending)
        self.goButton.grid(row=1, column=30, sticky='ew', padx=(0, 0))

        # Figure for graphing budget
        self.fig = Figure(figsize=(7, 2), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=2, column=1, rowspan=8,
                                         columnspan=45, sticky='ew')
        self.canvas._tkcanvas.grid(row=2, column=1, rowspan=8,
                                   columnspan=45, sticky='ew')

        # Figure for graphing spending
        self.fig2 = Figure(figsize=(7, 2), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, self)
        self.canvas2.get_tk_widget().grid(row=12, column=1, rowspan=8,
                                          columnspan=45, sticky='ew')
        self.canvas2._tkcanvas.grid(row=12, column=1, rowspan=8,
                                    columnspan=45, sticky='ew')

    def back(self):
        '''
        Clears figures, goes back to mainScreen

        **Parameters**
            None
        '''

        self.fig.clf()
        self.fig2.clf()
        self.controller.show_frame(mainScreen)

    def start(self):
        '''
        Initialization method for barScreen
        Graphs current budget as stacked bar graph
        '''

        self.fig.clf()
        self.canvas.draw()
        self.fig2.clf()
        self.canvas2.draw()

        # Get updated data from csv files
        self.username = self.controller.frames[mainScreen].username
        path = './profiles/' + self.username + '.csv'
        self.bud_nums = pd.read_csv(path, index_col=0)
        path = './profiles/' + self.username + '_transactions.csv'
        self.transactions = pd.read_csv(path, index_col=0)

        # Make go button clickable
        self.goButton['state'] = 'normal'

        # Check to make sure data exists
        if self.transactions.size == 0:
            alert("No transaction history available!")
            self.goButton['state'] = 'disabled'
            return

        # Get list of years appearing in transaction history
        # Assign to dropdown menu for year selection
        years = list(set(list(self.transactions['y'])))
        for i, v in enumerate(years):
            years[i] = int(v)
        years = years[::-1]
        self.yearmenu['values'] = years
        self.yearmenu.current(0)

        # Get budget values for each category, get total budget
        self.budget = {}
        self.budget_total = 0
        for i in categories:
            self.budget[i] =\
                self.bud_nums.iloc[0, self.bud_nums.columns.get_loc(i)]
            self.budget_total +=\
                self.bud_nums.iloc[0, self.bud_nums.columns.get_loc(i)]

        # Plot stacked bar graph of budget
        self.fig.clf()
        self.sub = self.fig.add_subplot(111)

        left_pos = 0
        width = 0.5
        for i in self.budget.keys():
            self.sub.barh('Your Budget', self.budget[i], width,
                          align='center', label=i, left=left_pos)
            left_pos += self.budget[i]

        self.sub.legend(ncol=len(self.budget))
        self.sub.set_xlim([0, 1.1 * self.budget_total])
        self.canvas.draw()

    def graphSpending(self):
        '''
        Graphs spending for selected month

        **Parameters**
            None
        '''

        # Get input year and month from comboboxes
        year = int(self.yearselection.get())
        month = months[self.monthselection.get()]

        # Get transaction data from selected month/year
        data = self.transactions[(self.transactions['y'] == year) &
                                 (self.transactions['m'] == month)]

        # Get categorical and total spending for given month/year
        spending_total = 0
        spending = {}
        for i in categories:
            spending[i] = data.loc[data['Type'] == i, 'Amount'].sum()
            spending_total += data.loc[data['Type'] == i, 'Amount'].sum()

        # Check if spending or budget total is larger
        # Will be used as xlim for bar graphs
        xmax = max(spending_total, self.budget_total)

        # Graph selected month's spending
        self.fig2.clf()
        self.sub2 = self.fig2.add_subplot(111)

        left_pos = 0
        width = 0.5
        for i in spending.keys():
            self.sub2.barh('Your Spending', spending[i], width,
                           align='center', label=i, left=left_pos)
            left_pos += spending[i]

        self.sub2.legend(ncol=len(spending))
        self.sub2.set_xlim([0, 1.1 * xmax])
        self.canvas2.draw()

        # Redraw budget graph to account for xlim
        self.fig.clf()
        self.sub = self.fig.add_subplot(111)

        left_pos = 0
        for i in self.budget.keys():
            self.sub.barh('Your Budget', self.budget[i], width,
                          align='center', label=i, left=left_pos)
            left_pos += self.budget[i]

        self.sub.legend(ncol=len(self.budget))
        self.sub.set_xlim([0, 1.1 * xmax])
        self.canvas.draw()


class budgetScreen(tk.Frame):
    '''
    Object that defines the budget control screen
    '''

    def __init__(self, parent, controller):
        self.controller = controller
        self.username = None
        self.bud_nums = None

        tk.Frame.__init__(self, parent)

        # Vertical frame for grid reference
        vertframe = ttk.Frame(self, borderwidth=5, width=1, height=800)
        vertframe.grid(column=0, row=1, columnspan=1, rowspan=30)
        # Horizontal frame for grid reference
        horframe = ttk.Frame(self, borderwidth=5, width=1200, height=1)
        horframe.grid(column=0, row=0, columnspan=50, rowspan=1)

        # Button to go back to mainScreen
        mainButton =\
            ttk.Button(self, text="Back",
                       command=lambda: controller.show_frame(mainScreen))
        mainButton.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky='ew')

        # Screen title
        title = tk.Label(self, text="Edit your budget:", font=largeFont)
        title.grid(row=2, column=4, columnspan=2)

        # Bills budget entry
        self.bills = tk.StringVar()
        label1 = tk.Label(self, text="Bills:", font=medFont)
        label1.grid(row=4, column=4, columnspan=1, sticky='w')
        self.billsEntry = ttk.Entry(self, textvariable=self.bills)
        self.billsEntry.grid(row=4, column=5)

        # Food budget entry
        self.food = tk.StringVar()
        label1 = tk.Label(self, text="Food:", font=medFont)
        label1.grid(row=5, column=4, columnspan=1, sticky='w')
        self.foodEntry = ttk.Entry(self, textvariable=self.food)
        self.foodEntry.grid(row=5, column=5)

        # Subscriptions budget entry
        self.subscriptions = tk.StringVar()
        label1 = tk.Label(self, text="Subscriptions:", font=medFont)
        label1.grid(row=6, column=4, columnspan=1, sticky='w')
        self.subscriptionsEntry = ttk.Entry(self,
                                            textvariable=self.subscriptions)
        self.subscriptionsEntry.grid(row=6, column=5)

        # Entertainment budget entry
        self.entertainment = tk.StringVar()
        label1 = tk.Label(self, text="Entertainment:", font=medFont)
        label1.grid(row=7, column=4, columnspan=1, sticky='w')
        self.entertainmentEntry = ttk.Entry(self,
                                            textvariable=self.entertainment)
        self.entertainmentEntry.grid(row=7, column=5)

        # Misc budget entry
        self.misc = tk.StringVar()
        label1 = tk.Label(self, text="Miscellaneous:", font=medFont)
        label1.grid(row=8, column=4, columnspan=1, sticky='w')
        self.miscEntry = ttk.Entry(self, textvariable=self.misc)
        self.miscEntry.grid(row=8, column=5)

        # Save input button
        transactionButton = ttk.Button(self, text="Save Changes",
                                       command=self.save)
        transactionButton.grid(row=9, column=5, columnspan=2,
                               pady=(30, 0), sticky='ew')

        # DISPLAY CURRENT VALUES
        title = tk.Label(self, text="Current Budget Values:", font=largeFont)
        title.grid(row=2, column=20, columnspan=2)

        # Bills
        label1 = tk.Label(self, text="Bills:", font=medFont)
        label1.grid(row=4, column=20, columnspan=1, sticky='w')
        self.bills_budget = tk.Text(self, height=1, width=15, state='disabled')
        self.bills_budget.grid(row=4, column=21)

        # Food
        self.food = tk.StringVar()
        label1 = tk.Label(self, text="Food:", font=medFont)
        label1.grid(row=5, column=20, columnspan=1, sticky='w')
        self.food_budget = tk.Text(self, height=1, width=15, state='disabled')
        self.food_budget.grid(row=5, column=21)

        # Subscriptions
        self.subscriptions = tk.StringVar()
        label1 = tk.Label(self, text="Subscriptions:", font=medFont)
        label1.grid(row=6, column=20, columnspan=1, sticky='w')
        self.subs_budget = tk.Text(self, height=1, width=15, state='disabled')
        self.subs_budget.grid(row=6, column=21)

        # Entertainment
        self.entertainment = tk.StringVar()
        label1 = tk.Label(self, text="Entertainment:", font=medFont)
        label1.grid(row=7, column=20, columnspan=1, sticky='w')
        self.ent_budget = tk.Text(self, height=1, width=15, state='disabled')
        self.ent_budget.grid(row=7, column=21)

        # Misc
        self.misc = tk.StringVar()
        label1 = tk.Label(self, text="Miscellaneous:", font=medFont)
        label1.grid(row=8, column=20, columnspan=1, sticky='w')
        self.misc_budget = tk.Text(self, height=1, width=15, state='disabled')
        self.misc_budget.grid(row=8, column=21)

    def save(self):
        '''
        Saves input budget values, writes to budget csv

        **Parameters**
            None
        '''

        # Get input values
        bills = self.billsEntry.get()
        food = self.foodEntry.get()
        subs = self.subscriptionsEntry.get()
        ent = self.entertainmentEntry.get()
        misc = self.miscEntry.get()

        # Check if inputs are valid
        for i in bills, food, subs, ent, misc:
            try:
                i = round(float(i), 2)
            except ValueError:
                alert("All budget values must be numbers!")
                return

            if i < 0:
                alert("Budget values must be positive!")
                return
            elif i > 999999:
                alert("You don't have that much money.")
                return

        # Assign new values to budget info dataframe
        self.bud_nums = self.controller.frames[mainScreen].bud_nums
        self.bud_nums.iloc[0, self.bud_nums.columns.get_loc('Bills')] = bills
        self.bud_nums.iloc[0, self.bud_nums.columns.get_loc('Food')] = food
        self.bud_nums.iloc[0, self.bud_nums.columns.get_loc('Subscriptions')]\
            = subs
        self.bud_nums.iloc[0, self.bud_nums.columns.get_loc('Entertainment')]\
            = ent
        self.bud_nums.iloc[0, self.bud_nums.columns.get_loc('Misc')] = misc

        # Save dataframe to file
        filepath = './profiles/'\
            + self.controller.frames[mainScreen].username + '.csv'
        self.bud_nums.to_csv(filepath)
        self.loadBudget()

    def loadBudget(self):
        '''
        Loads updated budget information from csv to display to budgetScreen
        '''

        # Enable textboxes to allow for text insertion
        self.bills_budget.config(state='normal')
        self.food_budget.config(state='normal')
        self.subs_budget.config(state='normal')
        self.ent_budget.config(state='normal')
        self.misc_budget.config(state='normal')

        # Clear textboxes
        self.bills_budget.delete(1.0, tk.END)
        self.food_budget.delete(1.0, tk.END)
        self.subs_budget.delete(1.0, tk.END)
        self.ent_budget.delete(1.0, tk.END)
        self.misc_budget.delete(1.0, tk.END)

        # Load budget file
        self.username = self.controller.frames[mainScreen].username
        path = './profiles/' + self.username + '.csv'
        self.bud_nums = pd.read_csv(path, index_col=0)

        # Get budget values for each category
        # Write to corresponding textbox
        # Disable each textbox after writing
        temp = float(self.bud_nums.iloc[0]['Bills'])
        temp = '${:,.2f}'.format(temp)
        self.bills_budget.insert(tk.END, temp)
        self.bills_budget.config(state='disabled')

        temp = float(self.bud_nums.iloc[0]['Food'])
        temp = '${:,.2f}'.format(temp)
        self.food_budget.insert(tk.END, temp)
        self.food_budget.config(state='disabled')

        temp = float(self.bud_nums.iloc[0]['Subscriptions'])
        temp = '${:,.2f}'.format(temp)
        self.subs_budget.insert(tk.END, temp)
        self.subs_budget.config(state='disabled')

        temp = float(self.bud_nums.iloc[0]['Entertainment'])
        temp = '${:,.2f}'.format(temp)
        self.ent_budget.insert(tk.END, temp)
        self.ent_budget.config(state='disabled')

        temp = float(self.bud_nums.iloc[0]['Misc'])
        temp = '${:,.2f}'.format(temp)
        self.misc_budget.insert(tk.END, temp)
        self.misc_budget.config(state='disabled')


if __name__ == "__main__":
    # Thanks for playing
    window = pyBudget()
    window.title("pyBudget")
    window.wm_geometry("1200x640")
    window.mainloop()
