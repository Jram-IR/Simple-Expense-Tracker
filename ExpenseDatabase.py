import sqlite3


class ExpenseDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # create the expenses table if it does not exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                type TEXT, 
                                amount INTEGER, 
                                date TEXT)''')
        self.conn.commit()

    def add_expense(self, expense_type, amount, date):
        self.cursor.execute('INSERT INTO expenses (type, amount, date) VALUES (?, ?, ?)',
                            (expense_type, amount, date))
        self.conn.commit()

    def get_all_expenses(self):
        self.cursor.execute('SELECT type, amount, date FROM expenses')
        rows = self.cursor.fetchall()
        return rows

    def clear_database(self):
        self.cursor.execute('DELETE FROM expenses')
        self.conn.commit()

    def search_expenses(self, search_string):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT type, amount, date FROM expenses WHERE type LIKE ? OR amount LIKE ? OR date LIKE ?',
                           (f'%{search_string}%', f'%{search_string}%', f'%{search_string}%'))
            rows = cursor.fetchall()
            return rows

    @staticmethod
    def sum_amount(rows):
        total = 0
        for row in rows:
            total = total + row[1]
        return total

    def delete_selected_rows(self, tree):
        selected_rows = tree.selection()
        for row_id in selected_rows:
            row_values = tree.item(row_id)['values']
            self.cursor.execute("DELETE FROM expenses WHERE Type = ? AND Amount = ? AND Date = ?", row_values)
            self.conn.commit()
            tree.delete(row_id)

    def __del__(self):
        self.conn.close()
