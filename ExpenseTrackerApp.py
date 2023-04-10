import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter import messagebox
from ExpenseDatabase import ExpenseDatabase


class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        self.db_size = 0

        # create the ExpenseDatabase instance
        self.expense_db = ExpenseDatabase('expenses.db')

        # All the widgets used in the UI are present in this constructor

        # Create a label and entry widget for the expense type
        self.eTypeLabel = ttk.Label(self.master, text="Expense Type:", font=("TkDefaultFont", 16))
        self.eTypeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entryType = ttk.Entry(self.master, font=("TkDefaultFont", 16))
        self.entryType.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        # Create a label and entry widget for the amount
        self.eAmt = ttk.Label(self.master, text="Amount:", font=("TkDefaultFont", 16))
        self.eAmt.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entryAmt = ttk.Entry(self.master, font=("TkDefaultFont", 16))
        self.entryAmt.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        # Create a button to submit the expense
        self.btnAdd = ttk.Button(self.master, text="Submit", command=self.submit_expense)
        self.btnAdd.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Create a button to delete all the rows selected in the table
        self.btnDelete = ttk.Button(self.master, text="Delete Selected", command=self.delete_selected)
        self.btnDelete.grid(row=2, column=2, padx=10, pady=10, sticky="we")

        # Create a label and entry widget for the expense type
        self.search = ttk.Label(self.master, text="Search Expense:", font=("TkDefaultFont", 16))
        self.search.grid(row=0, column=2, padx=20, pady=10, sticky="w")

        # Create an entry widget to input the search sequence
        self.searchStr = ttk.Entry(self.master, font=("TkDefaultFont", 16))
        self.searchStr.grid(row=0, column=3, padx=10, pady=10, sticky="we")

        # Create a label and entry widget for the amount
        self.total = ttk.Label(self.master, text="Total for selected:", font=("TkDefaultFont", 16))
        self.total.grid(row=1, column=2, padx=20, pady=10, sticky="w")

        # Create a label to show the average for the expense list shown in the table
        self.avg = ttk.Label(self.master, text="Avg for selected:", font=("TkDefaultFont", 16))
        self.avg.grid(row=1, column=3, padx=20, pady=10, sticky="e")

        # Stylizing the TreeView
        style = ttk.Style(self.master)
        style.configure("Treeview.Heading", font=('Helvetica', 16), foreground="black")
        style.configure("Treeview", font=('Helvetica', 15), foreground="black")

        # create a Treeview widget to display the expenses
        self.tree = ttk.Treeview(self.master, columns=('Type', 'Amount', 'Date'), show='headings')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Date', text='Date')
        self.tree.grid(row=3, column=0, padx=10, pady=10, columnspan=5, sticky="nsew")
        self.tree.configure(height=12)

        # Create a button to search the search string
        self.btn_find = ttk.Button(self.master, text="Find", command=self.populate_treeview)
        self.btn_find.grid(row=0, column=4, padx=10, pady=10, sticky="e")

        # Create a button that will clear the searchStr entry widget
        self.btn_clear = ttk.Button(self.master, text="Clear Search", command=self.reset_tree)
        self.btn_clear.grid(row=2, column=3, padx=10, pady=10, sticky="e")

        # Refresh the expense table
        self.reset_tree()

    def populate_treeview(self):
        # delete any existing data from the Treeview
        self.tree.delete(*self.tree.get_children())
        seq = self.searchStr.get()

        if seq == '':
            rows = self.expense_db.get_all_expenses()

        else:
            # get all the expenses from the database
            rows = self.expense_db.search_expenses(seq)
        for row in rows:
            self.tree.insert('', tk.END, values=row)
        self.db_size = len(rows)
        self.total.config(text=f'Total for selected: {ExpenseDatabase.sum_amount(rows)}/-')
        if self.db_size != 0:
            format_num = "{:.2f}".format(ExpenseDatabase.sum_amount(rows) / self.db_size)
            self.avg.config(text=f'Avg for selected: {format_num}/-')
        else:
            self.avg.config(text=f'Avg for selected: {0}/-')

    def submit_expense(self):
        expense_type = self.entryType.get()
        amount = self.entryAmt.get()

        if expense_type == '' or amount == '':
            messagebox.showwarning("Alert", "Invalid Entry! Please check your inputs.")
        elif expense_type.isdigit() or amount.isalpha():
            messagebox.showwarning("Alert", "Invalid Entry! Please check your inputs.")

        else:
            # Get the current date
            current_date = datetime.today()

            # Format the current date as a string
            date = current_date.strftime("%d/%m/%Y")

            self.expense_db.add_expense(expense_type, amount, date)
            self.clear_fields()
            self.reset_tree()

    def delete_selected(self):
        selected_rows = self.tree.selection()
        if not selected_rows:
            messagebox.showwarning("Message", "Select entries to delete.")
        else:
            self.expense_db.delete_selected_rows(self.tree)
            self.reset_tree()

    def clear_fields(self):
        self.entryType.delete(0, tk.END)
        self.entryAmt.delete(0, tk.END)

    def reset_tree(self):

        self.tree.delete(*self.tree.get_children())
        # get all the expenses from the database
        rows = self.expense_db.get_all_expenses()
        self.db_size = len(rows)
        self.searchStr.delete(0, tk.END)
        # insert each row into the Treeview
        for row in rows:
            self.tree.insert('', tk.END, values=row)
        self.total.config(text=f'Total for selected: {ExpenseDatabase.sum_amount(rows)}/-')
        if self.db_size != 0:
            format_num = "{:.2f}".format(ExpenseDatabase.sum_amount(rows) / self.db_size)
            self.avg.config(text=f'Avg for selected: {format_num}/-')
        else:
            self.avg.config(text=f'Avg for selected: {0}/-')
