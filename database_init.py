import customtkinter
from tkinter import *
import sqlite3


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')
main_window = customtkinter.CTk()
main_window.title("Passwords Database")
main_window.iconbitmap("darkModeV.ico")


# main functions

def update_listbox():
    """This function is used to update the listbox in real time"""
    update_db = sqlite3.connect("passwords.db")
    update_conn = update_db.cursor()
    convert_list = []

    for update_row in update_conn.execute("SELECT *, oid FROM passwords"):
        convert_list = list(update_row)

    new_data = convert_list[0]
    main_listbox.insert(0, new_data)
    update_db.close()


def show_selected():
    """This function is used to show the details of whatever the user clicks on"""
    main = main_listbox.get(ANCHOR)
    db = sqlite3.connect("passwords.db")
    conn = db.cursor()
    for rows in conn.execute("SELECT *, oid FROM passwords"):
        list_convert = list(rows)
        account_name = list_convert[0]
        username = list_convert[1]
        password = list_convert[2]
        if main == account_name:
            account_column_info.config(text='Account:\n' + account_name)
            username_column_info.config(text='Username/Email:\n' + username)
            password_column_info.config(text='Password:\n' + password)

    db.close()


def new_query():
    """This function is used to add a new data entry into the database"""

    def second_submit():
        new_entry = sqlite3.connect("passwords.db")
        n_conn = new_entry.cursor()
        new_account = new_account_entry.get()
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        n_conn.execute("INSERT INTO passwords (account, user_info, password) VALUES (?, ?, ?)",
                       (new_account, new_username, new_password))
        new_entry.commit()
        new_entry.close()
        update_listbox()

    new_query_window = customtkinter.CTk()
    new_query_window.title("Add New Query")
    new_query_window.iconbitmap("darkModeV.ico")
    # top frame
    top_frame_nq = customtkinter.CTkFrame(new_query_window, fg_color='#0000FF', height=10, width=300)
    top_frame_nq.grid(row=0, column=0, pady=10, padx=10, columnspan=3)
    new_line_label = customtkinter.CTkLabel(new_query_window, text='Adding New Data', text_font='Gerogia, 20')
    new_line_label.grid(row=1, column=1)
    # account entry and label
    new_account_label = customtkinter.CTkLabel(new_query_window, text='Account:', text_font='Gerogia 15')
    new_account_label.grid(row=2, column=1, sticky=W, padx=(10, 0), pady=(10, 0))
    new_account_entry = customtkinter.CTkEntry(new_query_window, width=200)
    new_account_entry.grid(row=3, column=1)
    # username/email entry and label
    new_username_label = customtkinter.CTkLabel(new_query_window, text='Username/Email:', text_font='Gerogia 15')
    new_username_label.grid(row=4, column=1, sticky=W, padx=(20, 0), pady=(10, 0))
    new_username_entry = customtkinter.CTkEntry(new_query_window, width=200)
    new_username_entry.grid(row=5, column=1)
    # password label and entry
    new_password_label = customtkinter.CTkLabel(new_query_window, text='Password:', text_font='Gerogia 15')
    new_password_label.grid(row=6, column=1, sticky=W, padx=(20, 0), pady=(10, 0))
    new_password_entry = customtkinter.CTkEntry(new_query_window, width=200)
    new_password_entry.grid(row=7, column=1, pady=(0, 10))
    # submit button
    new_submit_button = customtkinter.CTkButton(new_query_window, text='Submit', command=second_submit)
    new_submit_button.grid(row=8, column=1, pady=5)
    # bottom frame
    bottom_frame_nq = customtkinter.CTkFrame(new_query_window, fg_color='#0000FF', height=10, width=300)
    bottom_frame_nq.grid(row=9, column=0, pady=10, padx=10, columnspan=3)

    new_query_window.mainloop()


def edit_query():
    """This function is used to edit the selection the user wants to edit"""
    edit_main = main_listbox.get(ANCHOR)
    edit_db = sqlite3.connect("passwords.db")
    edit_conn = edit_db.cursor()

    def submit_edit():
        """function inside edit window"""
        inside_edit_db = sqlite3.connect("passwords.db")
        submit_edit_conn = inside_edit_db.cursor()

        for selected in submit_edit_conn.execute("SELECT *, oid FROM passwords"):
            if edit_main in selected:
                get_oid = selected[3]
                edit_account = edit_account_entry.get()
                edit_user = edit_username_entry.get()
                edit_password = edit_password_entry.get()

                submit_edit_conn.execute("UPDATE passwords SET account = ? WHERE oid = ?", (edit_account, get_oid))
                submit_edit_conn.execute("UPDATE passwords SET user_info = ? WHERE oid = ?", (edit_user, get_oid))
                submit_edit_conn.execute("UPDATE passwords SET password = ? WHERE oid = ?", (edit_password, get_oid))
        inside_edit_db.commit()
        inside_edit_db.close()

    for edit_rows in edit_conn.execute("SELECT *, oid FROM passwords"):
        list_convert = list(edit_rows)
        get_oid = list_convert[3]
        account_name = list_convert[0]
        username = list_convert[1]
        password = list_convert[2]

        if edit_main == account_name:
            edit_query_window = customtkinter.CTk()
            edit_query_window.title("Add New Query")
            edit_query_window.iconbitmap("darkModeV.ico")

            top_frame_eq = customtkinter.CTkFrame(edit_query_window, fg_color='#0000FF', height=10, width=300)
            top_frame_eq.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

            new_line_label = customtkinter.CTkLabel(edit_query_window, text='Editing Data', text_font='Gerogia, 20')
            new_line_label.grid(row=1, column=1)

            # account entry and label
            edit_account_label = customtkinter.CTkLabel(edit_query_window, text='Account:', text_font='Gerogia 15')
            edit_account_label.grid(row=2, column=1, sticky=W, padx=(10, 0), pady=(10, 0))

            edit_account_entry = customtkinter.CTkEntry(edit_query_window, width=200)
            edit_account_entry.insert(0, account_name)
            edit_account_entry.grid(row=3, column=1)

            # username/email entry and label
            edit_username_label = customtkinter.CTkLabel(edit_query_window, text='Username/Email:', text_font='Gerogia 15')
            edit_username_label.grid(row=4, column=1, sticky=W, padx=(20, 0), pady=(10, 0))

            edit_username_entry = customtkinter.CTkEntry(edit_query_window, width=200)
            edit_username_entry.insert(0, username)
            edit_username_entry.grid(row=5, column=1)

            # password label and entry
            edit_password_label = customtkinter.CTkLabel(edit_query_window, text='Password:', text_font='Gerogia 15')
            edit_password_label.grid(row=6, column=1, sticky=W, padx=(20, 0), pady=(10, 0))

            edit_password_entry = customtkinter.CTkEntry(edit_query_window, width=200)
            edit_password_entry.insert(0, password)
            edit_password_entry.grid(row=7, column=1, pady=(0, 10))

            edit_submit_button = customtkinter.CTkButton(edit_query_window, text='Submit', text_font='Gerogia, 15 bold',
                                                         width=100, hover_color='#00008B', command=submit_edit)
            edit_submit_button.grid(row=8, column=1, pady=5, ipadx=10)

            bottom_frame_eq = customtkinter.CTkFrame(edit_query_window, fg_color='#0000FF', height=10, width=300)
            bottom_frame_eq.grid(row=9, column=0, pady=10, padx=10, columnspan=3)

            edit_query_window.mainloop()


def delete_query():
    """And this function is to delete the selection the user wants"""
    sel = main_listbox.get(ANCHOR)
    delete_data = sqlite3.connect("passwords.db")
    d_db = delete_data.cursor()

    for to_be_del in d_db.execute("SELECT *, oid FROM passwords"):
        account_name = to_be_del[0]

        if sel == account_name:
            id_number = to_be_del[3]
            too_str = str(id_number)
            d_db.execute("DELETE from passwords WHERE oid =" + too_str)
        delete_data.commit()
    main_listbox.delete(ANCHOR)
    delete_data.close()


top_frame = customtkinter.CTkFrame(main_window, fg_color='#0000FF', height=10, width=300)
top_frame.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

accounts_label = customtkinter.CTkLabel(main_window, text='Accounts', text_font='Gerogia, 15')
accounts_label.grid(row=1, column=1)

db = sqlite3.connect("passwords.db")
conn = db.cursor()

# listbox and scrollbar frame
listbox_frame = customtkinter.CTkFrame(main_window)
listbox_frame.grid(row=2, column=1)
main_scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
main_listbox = Listbox(listbox_frame, yscrollcommand=main_scrollbar.set)
main_scrollbar.config(command=main_listbox.yview)
main_scrollbar.grid(row=0, column=1, sticky='ns')
main_listbox.grid(row=0, column=0)

for row in conn.execute("SELECT * FROM passwords"):
    main_listbox.insert(0, row[0])

show_button = customtkinter.CTkButton(main_window, text='Show Details', command=show_selected, hover_color='navy',
                                      text_font='Arial, 13 bold')
show_button.grid(row=3, column=1, pady=(5, 0))
account_name = 'Null'
username = "Null"
password = 'Null'
account_column_info = customtkinter.CTkLabel(main_window, text='Account:\n' + account_name)
account_column_info.grid(row=4, column=1, pady=7)
username_column_info = customtkinter.CTkLabel(main_window, text='Username:\n' + username)
username_column_info.grid(row=5, column=1, pady=7)
password_column_info = customtkinter.CTkLabel(main_window, text='Password:\n' + password)
password_column_info.grid(row=6, column=1, pady=7)

new_button = customtkinter.CTkButton(main_window, text='New', text_font='Arial, 10 bold', width=7,
                                     command=new_query, hover_color='lime')
new_button.grid(row=7, column=1, sticky=W, pady=(7, 0))

edit_button = customtkinter.CTkButton(main_window, text='Edit', text_font='Arial, 10 bold', width=7,
                                      command=edit_query, hover_color='midnightblue')
edit_button.grid(row=7, column=1, pady=(7, 0))


delete_button = customtkinter.CTkButton(main_window, text='Delete', text_font='Arial, 10 bold', width=7,
                                        command=delete_query, hover_color='maroon')
delete_button.grid(row=7, column=1, sticky=E, pady=(7, 0))

bottom_frame = customtkinter.CTkFrame(main_window, fg_color='#0000FF', height=10, width=300)
bottom_frame.grid(row=8, column=0, pady=10, padx=10, columnspan=3)


db.close()
main_window.mainloop()