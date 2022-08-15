from dataclasses import replace
import random
import string
import os.path
from tkinter import *


# create credentials global var
credentials_string = ""
credentials_list = []
credentials_website = ""
credentials_website_user = ""


# functions

# popup window
def open_popup(status):
    top = Toplevel(window)
    top.geometry("225x75")
    top.title("Message")
    msg = ""
    if status == "exists":
        msg = "A password for this website already exists\nWould you like to overwrite it?"
        yes_button = Button(
            top,
            text="Yes",
            command=overwrite,
        )
        yes_button.grid(column=0, row=1)
        # close popup on no button click
        no_button = Button(top, text="No", command=top.destroy)
        no_button.grid(column=1, row=1)
    elif status == "already in data":
        msg = "These credentials have already been saved"
    elif status == "saved":
        msg = "Your login credentials have been saved successfully"
    elif status == "missing":
        msg = "Please make sure all fields are filled"
    elif status == "website exists":
        msg = "There is already an entry for this site\nWould you like to overwrite or add a new entry?"
        overwrite_button = Button(top, text="Overwrite", command=overwrite)
        overwrite_button.grid(column=0, row=1)
        new_entry_button = Button(top, text="New Entry", command=save_new)
        new_entry_button.grid(column=1, row=1)
    status_message = Label(top, text=msg)
    status_message.grid(column=0, row=0, columnspan=2, sticky=EW)


# save different creds for already existing site
def save_new():
    with open("Password Manager GUI APP Tkinter/data.csv", "a") as data_file:
        data_file.write(credentials_string)


# WORKS WITH  BOTH OVERWRITE CONDITIONS
def overwrite():
    search_string = f"{credentials_list[0]}"
    replacement = credentials_string
    text = open("Password Manager GUI APP Tkinter/data.csv", "r")
    text_list = []
    for line in text:
        if search_string in line:
            search_string = line
        text_list.append(line)
    text = "".join(text_list)
    text = text.replace(search_string, replacement)
    x = open("Password Manager GUI APP Tkinter/data.csv", "w")  #
    x.writelines(text)
    x.close


# generate password
def generate_password():
    password = "".join(
        random.SystemRandom().choice(
            string.ascii_uppercase
            + string.digits
            + string.ascii_lowercase
            + string.punctuation
        )
        for _ in range(30)
    )
    password_entry.insert(0, password)


# UNFINISHED
# save password
def save_password():
    global credentials_string
    global credentials_list
    global credentials_website
    global credentials_website_user

    # get entires
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # credentials as string to save to data.csv
    credentials_string = f"{website},{username},{password}\n"
    credentials_list = credentials_string.split(",")
    credentials_website = credentials_list[0]
    credentials_website_user = f"{credentials_list[0]},{credentials_list[1]}"

    status = ""
    # check entries are valid (not empty, not already in data.csv)
    if len(website) > 0 and len(username) > 0 and len(password) > 0:
        # check if data file exists
        if os.path.exists("Password Manager GUI App Tkinter/data.csv"):
            with open("Password Manager GUI APP Tkinter/data.csv", "r+") as data_file:
                file_contents = data_file.readlines()
                if credentials_string in file_contents:
                    print("ITEM ALREADY IN DATA")
                    status = "already in data"
                    open_popup(status)
                    return
                for line in file_contents:
                    # check if website AND username exist in data file
                    # if true ask to overwrite entire line
                    if credentials_website_user in line:
                        print("WEBSITE AND USERNAME IN DATA")
                        status = "exists"
                        print("SENT TO OPEN POPUP EXISTS CONDITION")
                        open_popup(status)
                        return
                    # check if website exist in data file
                    # if true ask to overwrite or add new line
                    elif credentials_website in line:
                        status = "website exists"
                        print("SENT TO OPEN POPU WEBSITE EXISTS CONDITION")
                        open_popup(status)
                        return
                print("ADDED BRAND NEW CONDITION TO EXISTING FILE")
                data_file.write(credentials_string)
                status = "saved"
                open_popup(status)
                return
        else:
            with open("Password Manager GUI APP Tkinter/data.csv", "w") as data_file:
                print("ADDED BRAND NEW CONDITION TO NEW FILE")
                data_file.write("WEBSITE,USERNAME,PASSWORD\n")
                data_file.write(credentials_string)
                status = "saved"
                open_popup(status)
                return
    elif len(website) > 0 or len(username) > 0 or len(password) > 0:
        print("MISSING CREDS CONDITION")
        status = "missing"
        open_popup(status)


# UI
# window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
# make window start at size == working session window size
# window.geometry("350x325")
window.minsize(
    width=440, height=340
)  # minsize is 240 to account for the 20 padding on each side

# logo
# canvas (padlock image container)
canvas = Canvas(window, width=200, height=200)
canvas.configure(highlightthickness=0)  # highlight here is the boarder
logo_img = PhotoImage(file="Password Manager GUI App Tkinter/logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(window, text="Website:")
website_label.grid(column=0, row=1, sticky=E)

username_label = Label(window, text="Email/Username:")
username_label.grid(column=0, row=2, sticky=E)

password_label = Label(window, text="Password:")
password_label.grid(column=0, row=3, sticky=E)

# entries
website_entry = Entry(window, width=35)
website_entry.grid(column=1, row=1, columnspan=2, sticky=EW)
# focus website entry
website_entry.focus()

username_entry = Entry(window, width=35)
username_entry.grid(column=1, row=2, columnspan=2, sticky=EW)
username_entry.insert(0, "[EXAMPLE@EMAIL.COM]")


password_entry = Entry(window, width=21)
password_entry.grid(column=1, row=3, sticky=EW)

# buttons
generate_password_button = Button(
    window, text="Generate Password", command=generate_password
)
generate_password_button.grid(column=2, row=3, sticky=EW)

add_button = Button(window, text="Add", width=35, command=save_password)
add_button.grid(column=1, row=4, columnspan=2, sticky=EW)

# functions as a while loop to keep window open
window.mainloop()
