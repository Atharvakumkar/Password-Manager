from tkinter import *
from tkinter import messagebox

import customtkinter as ctk
import tkinter.font as ctkfont
from pymongo import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client.passwordManager
user_collection = db.userDetails

def signUp():
    userName = nameEntry.get().strip()
    userEmail = emailEntry.get()
    userPass = passwordEntry.get()
    userPassCheck = passwordEntry2.get()

    if userName == "" or userEmail == "":
        messagebox.showerror("Error","Please fill all the details!")
    elif userPass != userPassCheck:
        messagebox.showerror("Error", "Passwords don't match!")
    else:
        signUp_details = {
            'name' : userName,
            'email' : userEmail,
            'password' : userPass
        }

        try:
            user_collection.insert_one(signUp_details)
            messagebox.showinfo("Success", "Account Created Successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to sign up: {e}")


ctk.set_appearance_mode("dark")

mainWindow = ctk.CTk()

my_font_heading = ctk.CTkFont(family="Rubik", size = 42, weight = "bold")
my_font_subheading = ctk.CTkFont(family="Rubik", size = 28)
my_font_label1 = ctk.CTkFont(family="Rubik", size = 25, weight = "bold")
my_font_label2 = ctk.CTkFont(family="Rubik", size = 22)
my_font_button = ctk.CTkFont(family="Rubik", size = 18)
mainWindow.title("Login Page")
mainWindow.geometry("1080x720")
mainWindow.resizable("false", "false")

mainFrame = ctk.CTkFrame(master = mainWindow,
                         height = 720,
                         width = 1080,
                         fg_color = "#FAF7F3",
                         bg_color = "#FAF7F3")
mainFrame.place(x = 0, y = 0)

heading = ctk.CTkLabel(master = mainFrame,
                       text = "Password Manager",
                       font = my_font_heading,
                       text_color = "#AF8260")
heading.place(x = 345, y = 30)

subHeading = ctk.CTkLabel(master = mainFrame,
                       text = "Manage all your passwords at one place!",
                       font = my_font_subheading,
                       text_color = "#AF8260")
subHeading.place(x = 270, y = 90)

subFrame = ctk.CTkFrame(master = mainFrame,
                        height = 500,
                        width = 400,
                        fg_color = "#FFF2D7")
subFrame.place(x = 330, y = 160)

signUp_text = ctk.CTkLabel(master = subFrame,
                           text = "Sign-Up",
                           font = my_font_label1,
                           text_color = "#AF8260")
signUp_text.place(x = 140, y = 20)

nameEntry = ctk.CTkEntry(master = subFrame,
                          height = 50,
                          width = 360,
                          fg_color = "transparent",
                          border_width = 3,
                          border_color = "#AF8260",
                          placeholder_text = "Name",
                          placeholder_text_color = "#AF8260",
                          text_color = "#AF8260",
                          font = my_font_label2)
nameEntry.place(x = 20, y = 70)

emailEntry = ctk.CTkEntry(master = subFrame,
                          height = 50,
                          width = 360,
                          fg_color = "transparent",
                          border_width = 3,
                          border_color = "#AF8260",
                          placeholder_text = "Email",
                          placeholder_text_color = "#AF8260",
                          text_color = "#AF8260",
                          font = my_font_label2)
emailEntry.place(x = 20, y = 140)

passwordEntry = ctk.CTkEntry(master = subFrame,
                          height = 50,
                          width = 360,
                          fg_color = "transparent",
                          border_width = 3,
                          border_color = "#AF8260",
                          placeholder_text = "Password",
                          placeholder_text_color = "#AF8260",
                          text_color = "#AF8260",
                          font = my_font_label2,
                         show = ".")
passwordEntry.place(x = 20, y = 210)

passwordEntry2 = ctk.CTkEntry(master = subFrame,
                          height = 50,
                          width = 360,
                          fg_color = "transparent",
                          border_width = 3,
                          border_color = "#AF8260",
                          placeholder_text = "Confirm Password",
                          placeholder_text_color = "#AF8260",
                          text_color = "#AF8260",
                          font = my_font_label2,
                         show = ".")
passwordEntry2.place(x = 20, y = 280)

signUpSubmitButton = ctk.CTkButton(master = subFrame,
                             height = 40,
                             width = 150,
                             text = "Submit",
                             font = my_font_button,
                             fg_color = "#AF8260",
                             text_color = "white",
                             hover_color = "#AF8320",
                             command = signUp)
signUpSubmitButton.place(x = 120, y = 350)

alreadyLoginButton = ctk.CTkButton(master = subFrame,
                             height = 40,
                             width = 150,
                             text = "Already Signed Up? Login now",
                             font = my_font_button,
                             fg_color = "transparent",
                            text_color = "#AF8260",
                            hover_color = "white")
alreadyLoginButton.place(x = 68, y = 410)

mainWindow.mainloop()