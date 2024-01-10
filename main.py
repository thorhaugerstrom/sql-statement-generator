import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

class SQLGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Generator App")

        self.operation_var = tk.StringVar()
        self.table_var = tk.StringVar()
        self.csv_file_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Operation Selection
        tk.Label(self.root, text="Select operation:").pack()
        operations = ["UPDATE", "INSERT", "DELETE"]
        tk.OptionMenu(self.root, self.operation_var, *operations).pack()

        # Table Name Input
        tk.Label(self.root, text="Enter table name:").pack()
        tk.Entry(self.root, textvariable=self.table_var).pack()

        # CSV File Selection
        tk.Label(self.root, text="Select CSV file:").pack()
        tk.Entry(self.root, textvariable=self.csv_file_var, state="disabled").pack(side=tk.LEFT)
        tk.Button(self.root, text="Browse", command=self.browse_csv).pack(side=tk.RIGHT)

        # Generate SQL Button
        tk.Button(self.root, text="Generate SQL", command=self.generate_sql).pack()

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_file_var.set(file_path)

    def generate_sql(self):
        operation = self.operation_var.get()
        table_name = self.table_var.get()
        csv_file = self.csv_file_var.get()

        try:
            if operation == 'UPDATE':
                statements = generate_update_statements(table_name, csv_file)
            elif operation == 'INSERT':
                statements = generate_insert_statements(table_name, csv_file)
            elif operation == 'DELETE':
                statements = generate_delete_statements(table_name, csv_file)
            else:
                messagebox.showerror("Error", "Invalid operation selected. Please choose UPDATE, INSERT, or DELETE.")
                return

            sql_output = "\n".join(statements)
            self.show_result(sql_output)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_result(self, result):
        result_window = tk.Toplevel(self.root)
        result_window.title("SQL Statements")
        result_text = tk.Text(result_window, wrap=tk.WORD, height=20, width=50)
        result_text.insert(tk.END, result)
        result_text.pack()
        result_text.config(state=tk.DISABLED)


def generate_update_statements(table_name, csv_file):
    df = pd.read_csv(csv_file)
    update_statements = []

    for _, row in df.iterrows():
        set_clause = ', '.join(f"{column} = '{row[column]}'" for column in df.columns)
        where_clause = f"WHERE id = {row['id']}"  # Change 'id' to the primary key column of your table
        update_statement = f"UPDATE {table_name} SET {set_clause} {where_clause};"
        update_statements.append(update_statement)

    return update_statements

def generate_insert_statements(table_name, csv_file):
    df = pd.read_csv(csv_file)
    insert_statements = []

    for _, row in df.iterrows():
        columns = ', '.join(row.index)
        values = ', '.join(f"'{value}'" for value in row)
        insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        insert_statements.append(insert_statement)

    return insert_statements

def generate_delete_statements(table_name, csv_file):
    df = pd.read_csv(csv_file)
    delete_statements = []

    for _, row in df.iterrows():
        where_clause = f"WHERE id = {row['id']}"  # Change 'id' to the primary key column of your table
        delete_statement = f"DELETE FROM {table_name} {where_clause};"
        delete_statements.append(delete_statement)

    return delete_statements


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLGeneratorApp(root)
    root.mainloop()
