from ExpenseTrackerApp import ExpenseTrackerApp
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    # Used to define the window size
    root.geometry("800x550")


    root.title("Expense Tracker")
    app = ExpenseTrackerApp(root)
    root.mainloop()