import tkinter as tk
import csv
from io import StringIO
import pyperclip

def process_csv():
    csv_data = csv_text.get("1.0","end")

    csv_file = StringIO(csv_data)

    csv_reader = csv.reader(csv_file)

    insert_queries = []

    # Loop through CSV to create SQL queries
    for row in csv_reader:
        first_name, last_name, email, access_type, sso = row

        if "@lumeon.com" in email and access_type.lower() == 'system admin':
            insert_query_individual = f"INSERT INTO individual (individual_type_id, title, forename, surname, sex, email, status, all_locations, no_email, no_telephone) VALUES (1, '{access_type}', '{first_name}', '{last_name}', 'U', '{email}', 'A', 0, 0, 1);"
            insert_queries.append(insert_query_individual)
            
            insert_query_address = f"INSERT INTO address (postcode, status, individual_id, address_type_id) VALUES (12345, 'A', (SELECT individual_id FROM individual WHERE email = '{email}'), 1);"
            insert_queries.append(insert_query_address)

            update_query_individual = f"UPDATE individual set address_id = (SELECT address_id FROM address WHERE individual_id = (SELECT individual_id FROM individual WHERE email = '{email}')) WHERE individual_id = (SELECT individual_id FROM individual WHERE email = '{email}');"
            insert_queries.append(update_query_individual)

            insert_query_user_access = f"INSERT INTO user_access (individual_id, password, access_type_id, is_locked, failed_login_attempts, system_access_type, password_salt) VALUES ((SELECT individual_id FROM individual where email = '{email}'), '$1$gb07UZD1$.vgTeiTeTe0fNzcan2rSi1', 1, 0, 0, 3, NULL);"
            insert_queries.append(insert_query_user_access)      


        elif sso == '0' or sso.lower() == 'no' or sso.lower() == 'n':
            insert_query_individual = f"INSERT INTO individual (individual_type_id, title, forename, surname, sex, email, status, all_locations, no_email, no_telephone) VALUES (2, '{access_type}', '{first_name}', '{last_name}', 'U', '{email}', 'A', 1, 0, 1);"
            insert_queries.append(insert_query_individual)
            
            insert_query_address = f"INSERT INTO address (postcode, status, individual_id, address_type_id) VALUES (12345, 'A', (SELECT individual_id FROM individual WHERE email = '{email}'), 1);"
            insert_queries.append(insert_query_address)

            update_query_individual = f"UPDATE individual set address_id = (SELECT address_id FROM address WHERE individual_id = (SELECT individual_id FROM individual WHERE email = '{email}')) WHERE individual_id = (SELECT individual_id FROM individual WHERE email = '{email}');"
            insert_queries.append(update_query_individual)

            insert_query_user_access = f"INSERT INTO user_access (individual_id, password, access_type_id, is_locked, failed_login_attempts, system_access_type, password_salt) VALUES ((SELECT individual_id FROM individual where email = '{email}'), '$1$gb07UZD1$.vgTeiTeTe0fNzcan2rSi1', (SELECT access_type_id from access_type WHERE access_type_name = '{access_type}'), 0, 0, 3, NULL);"
            insert_queries.append(insert_query_user_access)

   
        elif sso == '1' or sso.lower() == 'yes' or sso.lower() == 'y':
            insert_query_individual = f"INSERT INTO individual (individual_type_id, title, forename, surname, sex, email, status, all_locations, no_email, no_telephone) VALUES (2, '{access_type}', '{first_name}', '{last_name}', 'U', '{email}', 'A', 1, 0, 1);"
            insert_queries.append(insert_query_individual)

            insert_query_address = f"INSERT INTO address (postcode, status, individual_id, address_type_id) VALUES (12345, 'A', (SELECT individual_id FROM individual WHERE email = '{email}'), 1);"
            insert_queries.append(insert_query_address)

            update_query_individual = f"UPDATE individual set address_id = (SELECT address_id FROM address WHERE individual_id = (SELECT individual_id FROM individual WHERE email = '{email}')) WHERE individual_id = (SELECT individual_id FROM individual WHERE email = '{email}');"
            insert_queries.append(update_query_individual)

            insert_query_single_sign_on_user = f"INSERT INTO single_sign_on_user_individual_link (individual_id, single_sign_on_user) VALUES ((SELECT individual_id FROM individual WHERE email = '{email}'), {sso});"
            insert_queries.append(insert_query_single_sign_on_user)


    # Clear any existing content in sql_text widget
    sql_text.delete("1.0", "end")

    # Insert SQL queries into sql_text_widget from array
    sql_text.insert("1.0", "\n".join(insert_queries))

def copy_to_clipboard():
    sql_content = sql_text.get("1.0","end")
    pyperclip.copy(sql_content)
    

##############################################GUI##############################################

root = tk.Tk()
root.title("User Import")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill="both", expand=True)

csv_instructions = tk.Label(frame, text="Data must be in a CSV format, excluding column headers, and in the following order:\nFirst name, last name, email, access type name, and a 'Yes' or a 'No' or a number indicating if they are SSO or non SSO (1 = SSO, 0 = non-SSO)\nNon-SSO user's passwords will be set to 'Password1'")
csv_instructions.grid(row=0, column=0, padx=5, pady=5, sticky="w")

csv_label = tk.Label(frame, text="Paste CSV content here:")
csv_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

csv_text = tk.Text(frame, width=50, height=10)
csv_text.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

process_button = tk.Button(frame, text="Process CSV", command=process_csv)
process_button.grid(row=3, column=0, padx=5, pady=5)

sql_label = tk.Label(frame, text="Generated SQL queries:")
sql_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

sql_text = tk.Text(frame, width=50, height=10)
sql_text.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

copy_button = tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=6, column=0, padx=5, pady=5)

frame.rowconfigure(2, weight=1)
frame.rowconfigure(5, weight=1)
frame.columnconfigure(0, weight=1)

root.mainloop()
