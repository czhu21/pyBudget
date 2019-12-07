# pyBudget

This is a repository for pyBudget, a tkinter-based budgeting application. The application is written in and for python3.

## Using pyBudget

Note: This application requires the matplotlib and pandas modules to run.

Download or clone this repository, making sure to maintain the directory structure (pyBudget.py and logins in the same directory, as well as the 'profiles' folder).
Run the pyBudget.py script, which will launch the GUI.
```
$ python3 pyBudget.py
```
In the home (launch) screen, you will have the option to login to an existing profile or create a new profile. Creating a profile invovles entering a username and password. 

Note: a pre-made profile (username 'Software_Carpentry' password 'password123') has been included to play around with.

Once you create a profile and login, you will be taken to the main screen. Here, you will have several options:

1) Edit Budget - Here you will be able to change your budget amounts for each category. Clicking 'Save Changes' will update your profile with the new values and display them on the right.

2) Add Transaction - Select a category, write a note describing the transaction, and enter a transaction amount. Clicking 'Add Transaction' will add the transaction to your profile's history and display it on the right.

3) Current Month Spending - Here you will be able to see a pie chart of all spending for the current month.

4) Compare Spending w/ Budget - Here you will be able to select a month/year and view a stacked bar graph of that month's spending compared to your budget.

## Authors

* **Casey Zhu**

## License

*

## Sources

The base structure of the GUI (writing frames as classes and their connecting framework) was inspired by the "GUIs with Tkinter (intermediate)" tutorial by sentdex on Youtube (https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk) as well as Bryan Oakley on Stack Overflow (https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter).

Other tutorials and guides I regularly referenced:

https://www.datacamp.com/community/tutorials/gui-tkinter-python

https://www.tutorialspoint.com/python/python_gui_programming.htm

https://likegeeks.com/python-gui-examples-tkinter-tutorial/

https://www.python-course.eu/tkinter_layout_management.php

https://pandas.pydata.org/pandas-docs/stable/getting_started/dsintro.html
